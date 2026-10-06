"""Preprocess or train with the pinned ACE-Step corrected flow-matching trainer."""
import argparse
from dataclasses import asdict
import json
import logging
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
ACE = Path("/tmp/maestro-ace-step")


def diagnostic(module):
    """Compare identical noise/timesteps on eight training clips, not a test set."""
    import torch
    files = sorted((ROOT / "data/tensors").glob("*.pt"))[::5]
    was_training, cfg_ratio = module.model.decoder.training, module._cfg_ratio
    previous_loss = module.last_training_loss
    losses = []
    module.model.decoder.eval()
    module._cfg_ratio = 0
    try:
        with torch.random.fork_rng(devices=[0]), torch.no_grad():
            for i, path in enumerate(files):
                torch.manual_seed(91000+i)
                tensors = torch.load(path, map_location="cpu", weights_only=False)
                batch = {k: v.unsqueeze(0) for k, v in tensors.items()
                         if isinstance(v, torch.Tensor)}
                losses.append(float(module.training_step(batch)))
    finally:
        module._cfg_ratio = cfg_ratio
        module.model.decoder.train(was_training)
        module.last_training_loss = previous_loss
    return dict(mean_loss=sum(losses)/len(losses), losses=losses,
                files=[p.name for p in files], noise_seeds=list(range(91000, 91000+len(files))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["preprocess", "train"])
    args = parser.parse_args()
    os.chdir(ROOT)
    os.environ.update(HF_HOME="/tmp/maestro-hf-cache", HF_HUB_OFFLINE="1",
                      TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
    logging.basicConfig(level=logging.INFO)
    import torch
    torch.cuda.set_per_process_memory_fraction(0.34)
    torch.set_float32_matmul_precision("medium")
    if args.stage == "preprocess":
        from acestep.training_v2.preprocess import preprocess_audio_files
        result = preprocess_audio_files(
            audio_dir=str(ROOT / "data/clips"), output_dir=str(ROOT / "data/tensors"),
            checkpoint_dir=str(ACE / "checkpoints"), variant="xl_base", max_duration=30,
            dataset_json=str(ROOT / "data/dataset.json"), device="cuda", precision="bf16")
        (ROOT / "record/preprocess.json").write_text(json.dumps(result, indent=2))
        if result["failed"] or result["processed"] != 40:
            raise RuntimeError(result)
        for path in (ROOT / "data/tensors").glob("*.pt"):
            tensors = torch.load(path, map_location="cpu", weights_only=False)
            for key, value in tensors.items():
                if isinstance(value, torch.Tensor) and not torch.isfinite(value).all():
                    raise RuntimeError(f"Nonfinite {path}: {key}")
        return
    from acestep.training_v2.configs import LoRAConfigV2, TrainingConfigV2
    from acestep.training_v2.model_loader import load_decoder_for_training
    from acestep.training_v2.trainer_fixed import FixedLoRATrainer
    output = ROOT / "artifacts/adapter"
    if (output / "final").exists():
        raise FileExistsError(output / "final")
    adapter = LoRAConfigV2(r=16, alpha=32, dropout=0.0)
    cfg = TrainingConfigV2(
        checkpoint_dir=str(ACE / "checkpoints"), model_variant="xl_base",
        dataset_dir=str(ROOT / "data/tensors"), output_dir=str(output),
        device="cuda", precision="bf16", batch_size=1, gradient_accumulation_steps=1,
        max_epochs=10, learning_rate=1e-4, warmup_steps=20, save_every_n_epochs=5,
        gradient_checkpointing=True, offload_encoder=True, num_workers=0,
        persistent_workers=False, pin_memory=False, seed=20261005,
        shift=1.0, num_inference_steps=50, log_every=10, log_heavy_every=100)
    record = dict(status="initializing", adapter=asdict(adapter), training=asdict(cfg),
                  ace_revision=subprocess.check_output(
                      ["git", "-C", str(ACE), "rev-parse", "HEAD"], text=True).strip())
    (ROOT / "record/training.json").write_text(json.dumps(record, indent=2))
    start = time.monotonic()
    model = load_decoder_for_training(str(ACE / "checkpoints"), "xl_base", "cuda", "bf16")
    trainer = FixedLoRATrainer(model, adapter, cfg)
    steps = 0
    before = None
    with (ROOT / "record/metrics.jsonl").open("w") as log:
        for update in trainer.train():
            if before is None and trainer.module is not None:
                before = diagnostic(trainer.module)
                print(f"Fixed-noise training diagnostic before: {before}", flush=True)
            print(update, flush=True)
            log.write(json.dumps(asdict(update)) + "\n")
            log.flush()
            steps = max(steps, update.step)
            if update.kind == "fail":
                raise RuntimeError(update.msg)
    if not (output / "final/adapter_model.safetensors").exists() or steps != 400:
        raise RuntimeError(f"Training verification failed: steps={steps}")
    record.update(status="complete", optimizer_steps=steps, elapsed_seconds=time.monotonic()-start,
                  peak_torch_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,
                  training_diagnostic_before=before,
                  training_diagnostic_after=diagnostic(trainer.module))
    (ROOT / "record/training.json").write_text(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
