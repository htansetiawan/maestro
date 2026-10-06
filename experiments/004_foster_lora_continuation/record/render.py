"""Matched LEGO rendering or 30-second seed / 180-second continuation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / "003_color_purple_yard_vocals"
ACE = Path("/tmp/maestro-ace-step")


def digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["lego", "continuation"])
    parser.add_argument("--adapter", action="store_true")
    args = parser.parse_args()
    name = f"{args.task}-{'foster' if args.adapter else 'base'}"
    audio = ROOT / "audio" / name
    if audio.exists():
        raise FileExistsError(audio)
    audio.mkdir(parents=True)
    os.chdir(ROOT)
    os.environ.update(ACESTEP_CHECKPOINTS_DIR=str(ACE / "checkpoints"),
                      HF_HOME="/tmp/maestro-hf-cache", HF_HUB_OFFLINE="1",
                      TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false",
                      ACESTEP_GENERATION_TIMEOUT="1200")
    import numpy as np
    import soundfile as sf
    import torch
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationConfig, GenerationParams, generate_music
    torch.cuda.set_per_process_memory_fraction(0.34)
    baseline = json.loads((BASE / "record/generation.json").read_text())
    params = GenerationParams(**baseline["parameters"])
    source = BASE / "data/source.wav"
    if digest(source) != baseline["decoded_source_sha256"]:
        raise RuntimeError("Baseline source changed")
    params.src_audio = str(source)
    backing, sr = sf.read(source, dtype="float32", always_2d=True)
    if args.task == "continuation":
        prefix = backing[:30*sr].copy()
        seed_audio = np.zeros((210*sr, 2), dtype="float32")
        seed_audio[:len(prefix)] = prefix
        seed_path = ROOT / "data/prefix-30s-padded-210s.wav"
        if not seed_path.exists():
            sf.write(seed_path, seed_audio, sr, subtype="FLOAT")
        check, check_sr = sf.read(seed_path, dtype="float32", always_2d=True)
        assert check_sr == sr and np.array_equal(check, seed_audio)
        params.src_audio = str(seed_path)
        params.task_type = "repaint"
        params.instruction = "Repaint the mask area based on the given conditions:"
        params.duration = 210
        params.repainting_start = 30
        params.repainting_end = 210
        params.chunk_mask_mode = "explicit"
        params.repaint_wav_crossfade_sec = 0.0
        params.caption = (
            "A nostalgic cinematic piano ballad about Harvard Yard, college friendship "
            "and memories. Begin with the supplied solo piano introduction, then continue "
            "its musical theme with expressive piano, a lush acoustic orchestra of strings, "
            "warm horns and woodwinds, and a warm expressive male tenor singing clear English. "
            "Tender verses, a soaring melodic chorus, rich harmonic movement, restrained "
            "percussion, natural breathing spaces, an orchestral interlude and a gentle ending. "
            "Full arrangement with piano, orchestra, and vocals.")
    config = GenerationConfig(**baseline["config"])
    adapter = ROOT / "artifacts/adapter/final"
    record = dict(status="initializing", parameters=params.to_dict(), config=config.to_dict(),
                  source_sha256=digest(params.src_audio), adapter_scale=1.0 if args.adapter else None,
                  baseline_record=str(BASE / "record/generation.json"),
                  adapter_sha256=digest(adapter / "adapter_model.safetensors") if args.adapter else None)
    record_path = ROOT / "record" / f"{name}.json"
    record_path.write_text(json.dumps(record, indent=2))
    start = time.monotonic()
    handler = AceStepHandler()
    status, ok = handler.initialize_service(
        project_root=str(ACE), config_path="acestep-v15-xl-base", device="cuda",
        use_flash_attention=False, compile_model=False, offload_to_cpu=True,
        offload_dit_to_cpu=False, quantization=None, prefer_source="huggingface")
    if not ok:
        raise RuntimeError(status)
    if args.adapter:
        for status in (handler.load_lora(str(adapter)), handler.set_use_lora(True),
                       handler.set_lora_scale(1.0)):
            print(status, flush=True)
            if not status.startswith("✅"):
                raise RuntimeError(status)
    result = generate_music(handler, None, params, config, save_dir=str(ROOT / "raw" / name))
    if not result.success or len(result.audios) != 1:
        raise RuntimeError(result.error)
    generated, gen_sr = sf.read(result.audios[0]["path"], dtype="float32", always_2d=True)
    assert sr == gen_sr and np.isfinite(generated).all()
    record["raw_duration_seconds"] = len(generated)/sr
    expected = len(backing) if args.task == "lego" else 210*sr
    generated = np.pad(generated, ((0, max(0, expected-len(generated))), (0, 0)))[:expected]
    exports = {}
    if args.task == "lego":
        rms = float(np.sqrt(np.mean(generated**2)))
        assert rms > 1e-5
        gain = float(np.sqrt(np.mean(backing**2))) / rms * 10**(2/20)
        mix = backing + gain*generated
        mix_gain = min(1, .95 / float(np.abs(mix).max()))
        exports = {"vocals": generated, "mix": mix * mix_gain}
        record.update(vocal_gain=gain, mix_gain=mix_gain)
    else:
        record["raw_prefix_max_error"] = float(np.max(np.abs(generated[:len(prefix)]-prefix)))
        generated[:len(prefix)] = prefix  # Exact original samples in float WAV.
        assert np.array_equal(generated[:len(prefix)], prefix)
        assert float(np.sqrt(np.mean(generated[len(prefix):]**2))) > 1e-5
        exports = {"continuation": generated}
        record.update(preserved_prefix_seconds=30, generated_seconds=180,
                      prefix_exact=True, supplied_audio_after_30_seconds="zeros")
    record["outputs"] = {}
    for label, samples in exports.items():
        wav = audio / f"{label}.wav"
        sf.write(wav, samples, sr, subtype="FLOAT")
        mp3 = audio / f"{label}.mp3"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(wav),
                        "-c:a", "libmp3lame", "-b:a", "256k", str(mp3)], check=True)
        record["outputs"][label] = dict(duration_seconds=len(samples)/sr,
            rms=float(np.sqrt(np.mean(samples**2))), peak=float(np.abs(samples).max()),
            wav_sha256=digest(wav), mp3_sha256=digest(mp3))
    record.update(status="complete", elapsed_seconds=time.monotonic()-start,
                  peak_torch_allocated_gib=torch.cuda.max_memory_allocated()/1024**3)
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(f"Saved {audio}", flush=True)


if __name__ == "__main__":
    main()
