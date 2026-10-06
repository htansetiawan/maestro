"""Add strings, woodwinds, and brass to the source through sequential LEGO calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
ACE = Path("/tmp/maestro-ace-step")
LAYERS = [
    ("strings", -6.0,
     "Acoustic orchestral string section only: lyrical violins, warm violas, cellos "
     "and double basses. Accompany the existing piano with spacious legato harmony, "
     "gentle swells and occasional melodic answers in its phrase gaps. Follow its "
     "harmonic changes, tempo and expressive timing; leave the piano melody prominent."),
    ("woodwinds", -12.0,
     "Acoustic orchestral woodwind section only: delicate flute, lyrical oboe, mellow "
     "clarinet and bassoon. Sparse warm countermelodies and short answering phrases "
     "around the existing piano and strings. Match their harmonic movement and "
     "phrase timing, with rests between responses; leave room for the piano melody."),
    ("brass", -14.0,
     "Acoustic orchestral brass section only: warm French horns and restrained "
     "trombones, soft sustained chord tones and gentle crescendos at musical peaks. "
     "Support the existing piano, strings and woodwinds, following their harmony and "
     "phrasing. A tender cinematic ballad with spacious dynamics and long rests."),
]


def digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("/tmp/theme_from_the_color_purple.mp3"))
    args = parser.parse_args()
    source_original = args.source.resolve(strict=True)
    if (ROOT / "record/generation.json").exists():
        raise FileExistsError("A run already exists; preserve it and use another experiment directory")
    for folder in ("audio", "data", "raw", "record"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
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
    source = ROOT / "data/source.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(source_original),
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", str(source)], check=True)
    piano, sr = sf.read(source, dtype="float32", always_2d=True)
    duration = len(piano) / sr
    piano_rms = float(np.sqrt(np.mean(piano**2)))
    assert sr == 48000 and piano_rms > 1e-5 and np.isfinite(piano).all()
    record = dict(status="initializing", source=str(source_original), source_sha256=digest(source_original),
                  decoded_source_sha256=digest(source), model="acestep-v15-xl-base", adapter=None,
                  ace_revision=subprocess.check_output(["git", "-C", str(ACE), "rev-parse", "HEAD"],
                                                       text=True).strip(),
                  duration_seconds=duration, piano_rms=piano_rms, layers=[], outputs={})
    record_path = ROOT / "record/generation.json"

    def save_record():
        record_path.write_text(json.dumps(record, indent=2) + "\n")

    def export(label, samples):
        wav, mp3 = ROOT / f"audio/{label}.wav", ROOT / f"audio/{label}.mp3"
        sf.write(wav, samples, sr, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(wav),
                        "-c:a", "libmp3lame", "-b:a", "256k", str(mp3)], check=True)
        record["outputs"][label] = dict(duration_seconds=len(samples)/sr,
            rms=float(np.sqrt(np.mean(samples**2))), peak=float(np.abs(samples).max()),
            wav_sha256=digest(wav), mp3_sha256=digest(mp3))

    save_record()
    started = time.monotonic()
    handler = AceStepHandler()
    status, ok = handler.initialize_service(
        project_root=str(ACE), config_path="acestep-v15-xl-base", device="cuda",
        use_flash_attention=False, compile_model=False, offload_to_cpu=True,
        offload_dit_to_cpu=False, quantization=None, prefer_source="huggingface")
    if not ok:
        raise RuntimeError(status)
    mix = piano.copy()
    orchestra = np.zeros_like(piano)
    context = source
    config = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[20261005], audio_format="wav32")
    for name, relative_db, caption in LAYERS:
        params = GenerationParams(
            task_type="lego", instruction=f"Generate the {name.upper()} track based on the audio context:",
            src_audio=str(context), caption=caption + " Purely instrumental accompaniment; no singing.",
            lyrics="[Instrumental]", instrumental=True, vocal_language="unknown", duration=duration,
            inference_steps=50, guidance_scale=7.0, seed=20261005,
            repainting_start=0.0, repainting_end=-1.0, thinking=False, use_cot_metas=False,
            use_cot_caption=False, use_cot_language=False, use_cot_lyrics=False,
            audio_codes="", enable_normalization=False)
        entry = dict(track=name, parameters=params.to_dict(), config=config.to_dict(),
                     context_sha256=digest(context), relative_rms_db=relative_db)
        record.update(status=f"generating_{name}")
        record["layers"].append(entry)
        save_record()
        stage_start = time.monotonic()
        result = generate_music(handler, None, params, config, save_dir=str(ROOT / "raw" / name))
        if not result.success or len(result.audios) != 1:
            raise RuntimeError(result.error)
        stem, stem_sr = sf.read(result.audios[0]["path"], dtype="float32", always_2d=True)
        assert stem_sr == sr and np.isfinite(stem).all()
        entry["raw_duration_seconds"] = len(stem)/sr
        stem = np.pad(stem, ((0, max(0, len(piano)-len(stem))), (0, 0)))[:len(piano)]
        assert stem.shape == piano.shape
        rms = float(np.sqrt(np.mean(stem**2)))
        assert rms > 1e-5
        gain = piano_rms / rms * 10**(relative_db/20)
        orchestra += stem * gain
        mix += stem * gain
        context_gain = min(1.0, .95 / float(np.abs(mix).max()))
        context = ROOT / f"data/context-after-{name}.wav"
        sf.write(context, mix * context_gain, sr, subtype="FLOAT")
        entry.update(status="complete", stem_gain=gain, context_gain=context_gain,
                     elapsed_seconds=time.monotonic()-stage_start)
        export(name, stem)
        if name == "strings":
            export("piano-and-strings", mix * context_gain)
        save_record()
        print(f"Completed {name}", flush=True)
    mix_gain = min(1.0, .95 / float(np.abs(mix).max()))
    orchestra_gain = min(1.0, .95 / float(np.abs(orchestra).max()))
    export("piano-and-orchestra", mix * mix_gain)
    export("orchestra-only", orchestra * orchestra_gain)
    record.update(status="complete", mix_gain=mix_gain, orchestra_gain=orchestra_gain,
                  elapsed_seconds=time.monotonic()-started,
                  peak_torch_allocated_gib=torch.cuda.max_memory_allocated()/1024**3)
    save_record()
    print(f"Saved orchestral additions to {ROOT / 'audio'}", flush=True)


if __name__ == "__main__":
    main()
