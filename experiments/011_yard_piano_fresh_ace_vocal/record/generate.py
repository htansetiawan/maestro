"""Run a reproducible LEGO vocal take and mix it with the supplied recording."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time


def sha256(path: Path) -> str:
    """Hash a local input without loading the entire file into memory."""
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main() -> None:
    """Generate one vocal stem with explicit source conditioning and export a mix."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("/tmp/theme_from_the_color_purple.mp3"))
    parser.add_argument("--ace-root", type=Path, default=Path("/tmp/maestro-ace-step"))
    parser.add_argument("--seed", type=int, default=20261007)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    audio, data, record = root / "audio", root / "data", root / "record"
    if (audio / "vocals.wav").exists():
        raise FileExistsError("This take already exists; use a separate experiment for another take")
    for folder in (audio, data, record):
        folder.mkdir(parents=True, exist_ok=True)
    source_original = args.source.resolve(strict=True)
    args.ace_root = args.ace_root.resolve(strict=True)
    request = json.loads((root / 'inputs/request.json').read_text())
    assert args.seed == request['seed']
    assert sha256(source_original) == request['source_sha256']
    assert subprocess.check_output(['git','-C',str(args.ace_root),'rev-parse','HEAD'],text=True).strip() == 'ca1e85fe9430179831e6bc6be790c332190a3866'
    os.chdir(root)
    os.environ["ACESTEP_CHECKPOINTS_DIR"] = str(args.ace_root / "checkpoints")
    os.environ["HF_HOME"] = "/tmp/maestro-hf-cache"
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["ACESTEP_GENERATION_TIMEOUT"] = "1200"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    import numpy as np
    import soundfile as sf
    import torch
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationConfig, GenerationParams, generate_music

    source = data / "source.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(source_original),
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", str(source)], check=True)
    duration = sf.info(source).duration
    caption = request['caption']
    torch.set_num_threads(4)
    if torch.cuda.mem_get_info()[0] < 17 * 2**30:
        raise RuntimeError('Need at least 17 GiB of free GPU memory')
    params = GenerationParams(
        task_type="lego", instruction="Generate the VOCALS track based on the audio context:",
        src_audio=str(source), caption=caption, lyrics=(root / "inputs/lyrics.txt").read_text(),
        instrumental=False, vocal_language="en", duration=duration,
        inference_steps=50, guidance_scale=7.0, seed=args.seed,
        repainting_start=0.0, repainting_end=-1.0,
        thinking=False, use_cot_metas=False, use_cot_caption=False,
        use_cot_language=False, use_cot_lyrics=False, audio_codes="",
        enable_normalization=False,
    )
    config = GenerationConfig(batch_size=1, use_random_seed=False,
                              seeds=[args.seed], audio_format="wav32")
    # Keep the validated LEGO runtime memory limit from experiment 003.
    torch.cuda.set_per_process_memory_fraction(0.34, device=0)
    manifest = {
        "status": "initializing", "title": request["title"],
        "ace_revision": subprocess.check_output(
            ["git", "-C", str(args.ace_root), "rev-parse", "HEAD"], text=True).strip(),
        "model": "acestep-v15-xl-base", "adapter": None,
        "source_file": str(source_original), "source_sha256": sha256(source_original),
        "decoded_source_sha256": sha256(source), "lyrics_sha256": sha256(root / "inputs/lyrics.txt"),
        "parameters": params.to_dict(), "config": config.to_dict(),
        "gpu": torch.cuda.get_device_name(0), "gpu_memory_fraction": 0.34,
        "cpu_offload": True, "source_duration_seconds": duration,
        "model_config_sha256": sha256(args.ace_root / "checkpoints/acestep-v15-xl-base/config.json"),
    }
    previous_revisions = Path("/tmp/maestro-yard-vocals/model_revisions.json")
    if previous_revisions.is_file():
        manifest["download_revisions_record"] = json.loads(previous_revisions.read_text())
    manifest_file = record / "generation-private.json"

    def save_record() -> None:
        manifest_file.write_text(json.dumps(manifest, indent=2) + "\n")

    save_record()
    started = time.monotonic()
    dit = AceStepHandler()
    status, success = dit.initialize_service(
        project_root=str(args.ace_root), config_path="acestep-v15-xl-base", device="cuda",
        use_flash_attention=False, compile_model=False, offload_to_cpu=True,
        offload_dit_to_cpu=False, quantization=None, prefer_source="huggingface")
    print(status, flush=True)
    if not success:
        manifest.update(status="failed_initialization", error=status)
        save_record()
        raise RuntimeError(status)
    generation_started = time.monotonic()
    result = generate_music(dit, None, params, config, save_dir=str(root / "raw"))
    if not result.success or len(result.audios) != 1:
        manifest.update(status="failed_generation", error=str(result.error))
        save_record()
        raise RuntimeError(f"ACE generation failed: {result.error}")
    manifest["generation_seconds"] = time.monotonic() - generation_started
    shutil.copyfile(result.audios[0]["path"], audio / "vocals.wav")
    backing, sr = sf.read(source, always_2d=True, dtype="float32")
    vocal, vocal_sr = sf.read(audio / "vocals.wav", always_2d=True, dtype="float32")
    if sr != vocal_sr or not np.isfinite(vocal).all():
        raise RuntimeError("Generated audio has a sample-rate mismatch or nonfinite values")
    raw_vocal_duration = len(vocal) / sr
    vocal = np.pad(vocal, ((0, max(0, len(backing) - len(vocal))), (0, 0)))[:len(backing)]
    if vocal.shape[1] == 1:
        vocal = np.repeat(vocal, 2, axis=1)
    backing_rms = float(np.sqrt(np.mean(backing ** 2)))
    vocal_rms = float(np.sqrt(np.mean(vocal ** 2)))
    if vocal_rms < 1e-5:
        raise RuntimeError("Generated vocal stem is silent")
    vocal_gain = backing_rms / vocal_rms * 10 ** (2 / 20)
    mix = backing + vocal * vocal_gain
    mix_gain = min(1.0, 0.95 / max(float(np.max(np.abs(mix))), 1e-8))
    mix_path = audio / "the-yard-remembers-mix.wav"
    sf.write(mix_path, mix * mix_gain, sr, subtype="PCM_24")
    mix_flac = audio / "mix.flac"
    sf.write(mix_flac, mix * mix_gain, sr, subtype="PCM_24")
    vocal_delivery_gain = min(1.0, 0.95 / max(float(np.max(np.abs(vocal))), 1e-8))
    sf.write(audio / "vocals.flac", vocal * vocal_delivery_gain, sr, subtype="PCM_24")
    for name in ("mix", "vocals"):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(audio / (name+".flac")),
                        "-c:a", "libmp3lame", "-b:a", "256k", str(audio / (name+".mp3"))], check=True)
    saved_mix, _ = sf.read(mix_flac, dtype="float32", always_2d=True)
    error = float(np.max(np.abs(saved_mix - mix * mix_gain)))
    recovered_backing = saved_mix / mix_gain - vocal * vocal_gain
    piano_error = float(np.max(np.abs(recovered_backing - backing)))
    assert error < 2e-7 and piano_error < 2e-6
    assert np.isfinite(saved_mix).all() and np.max(np.abs(saved_mix)) < 1
    assert len(saved_mix) == len(backing)
    quality = dict(mix_reconstruction_max_error=error,
                   recovered_piano_max_error=piano_error,
                   piano_time_stretched=False, piano_regenerated=False,
                   piano_gain=mix_gain, vocal_gain=vocal_gain,
                   vocal_delivery_gain=vocal_delivery_gain,
                   sample_rate=sr, channels=2, samples=len(backing),
                   duration_seconds=len(backing)/sr,
                   raw_vocal_duration_seconds=raw_vocal_duration,
                   vocal_padding_or_trimming_samples=len(backing)-round(raw_vocal_duration*sr),
                   peak=float(np.max(np.abs(saved_mix))),
                   clipped_samples=int((np.abs(saved_mix)>=1).sum()),
                   musical_alignment_evaluated=False, lyric_accuracy_evaluated=False)
    (record / "quality.json").write_text(json.dumps(quality,indent=2)+"\n")
    manifest.update(
        status="complete", elapsed_seconds=time.monotonic() - started,
        raw_vocal_duration_seconds=raw_vocal_duration, mix_duration_seconds=len(backing) / sr,
        vocal_gain=vocal_gain, mix_gain=mix_gain, backing_rms=backing_rms, vocal_rms=vocal_rms,
        mix_peak=float(np.max(np.abs(mix * mix_gain))),
        peak_torch_allocated_gib=torch.cuda.max_memory_allocated() / 1024 ** 3,
        outputs={p.name: sha256(p) for p in sorted(audio.iterdir()) if p.is_file()},
    )
    save_record()
    public = dict(manifest)
    public['source_file'] = source_original.name
    public['parameters'] = dict(manifest['parameters'], src_audio='data/source.wav')
    public['metadata_export'] = 'Public copy with source paths replaced; native runtime record retained locally.'
    public.pop('download_revisions_record',None)
    public['outputs'] = {p.name:sha256(p) for p in sorted(audio.iterdir()) if p.suffix in ('.mp3','.flac')}
    public['lyrics_source'] = 'experiments/009_yard_original_song/inputs/lyrics.txt'
    public['vocal_delivery_gain'] = vocal_delivery_gain
    (record / 'generation.json').write_text(json.dumps(public,indent=2)+'\n')
    print(f"Saved {audio / 'mix.mp3'}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        import traceback
        failure = Path(__file__).resolve().parent / 'failure-private.json'
        failure.write_text(json.dumps(dict(error=str(error), traceback=traceback.format_exc()),indent=2)+'\n')
        raise
