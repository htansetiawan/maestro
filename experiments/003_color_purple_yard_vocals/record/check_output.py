"""Check exported audio and transcribe the generated stem as a lyric spot-check."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

os.environ["HF_HOME"] = "/tmp/maestro-hf-cache"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import numpy as np
import soundfile as sf
import torch
from transformers import pipeline


def main() -> None:
    """Validate duration, samples and mixing, then save a local ASR transcript."""
    root = Path(__file__).resolve().parents[1]
    record = root / "record"
    manifest = json.loads((record / "generation.json").read_text())
    quality = {"files": {}, "alignment_assessed": False}
    for name in ("vocals.wav", "the-yard-remembers-mix.wav"):
        samples, sr = sf.read(root / "audio" / name, dtype="float32", always_2d=True)
        finite = bool(np.isfinite(samples).all())
        peak = float(np.max(np.abs(samples)))
        rms = float(np.sqrt(np.mean(samples ** 2)))
        quality["files"][name] = {
            "seconds": len(samples) / sr, "sample_rate": sr, "channels": samples.shape[1],
            "finite": finite, "peak": peak, "rms": rms,
            "samples_at_or_above_full_scale": int((np.abs(samples) >= 1).sum()),
        }
        if not finite or rms < 1e-5:
            raise RuntimeError(f"Invalid or silent output: {name}")
    source, sr = sf.read(root / "data/source.wav", dtype="float32", always_2d=True)
    vocal, _ = sf.read(root / "audio/vocals.wav", dtype="float32", always_2d=True)
    mix, _ = sf.read(root / "audio/the-yard-remembers-mix.wav", dtype="float32", always_2d=True)
    vocal = np.pad(vocal, ((0, max(0, len(source) - len(vocal))), (0, 0)))[:len(source)]
    expected = (source + vocal * manifest["vocal_gain"]) * manifest["mix_gain"]
    mix_error = float(np.max(np.abs(expected - mix)))
    if len(mix) != len(source) or mix_error > 2e-7 or np.max(np.abs(mix)) >= 1:
        raise RuntimeError("Exported mix failed duration, sample-preservation or peak check")
    quality["mix_reconstruction_max_error"] = mix_error
    quality["note"] = "ASR checks recognizable words; musical fit requires listening."
    (record / "quality.json").write_text(json.dumps(quality, indent=2) + "\n")
    asr_path = root / "data/vocals-asr.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i",
                    str(root / "audio/vocals.wav"), "-ar", "16000", "-ac", "1",
                    str(asr_path)], check=True)
    samples, sr = sf.read(asr_path, dtype="float32")
    recognizer = pipeline("automatic-speech-recognition", model="openai/whisper-base.en",
                          device=0, torch_dtype=torch.float16)
    result = recognizer({"raw": samples, "sampling_rate": sr}, chunk_length_s=30,
                        stride_length_s=5, return_timestamps=True)
    (record / "transcription.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["text"], flush=True)


if __name__ == "__main__":
    main()
