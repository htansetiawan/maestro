"""Verify the trained adapter, matched rendering controls, and audio preservation."""
import json
from pathlib import Path

import numpy as np
from safetensors.torch import load_file
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / "003_color_purple_yard_vocals"


def main():
    training = json.loads((ROOT / "record/training.json").read_text())
    assert training["status"] == "complete" and training["optimizer_steps"] == 400
    tensors = {k: v.float().numpy() for k, v in load_file(
        ROOT / "artifacts/adapter/final/adapter_model.safetensors").items()}
    assert tensors and all(np.isfinite(v).all() for v in tensors.values())
    b_weights = [v for k, v in tensors.items() if "lora_B" in k]
    assert b_weights and all(np.count_nonzero(v) > 0 for v in b_weights)
    baseline = json.loads((BASE / "record/generation.json").read_text())
    lego = json.loads((ROOT / "record/lego-foster.json").read_text())
    assert lego["status"] == "complete"
    assert lego["parameters"] == baseline["parameters"]
    assert lego["config"] == baseline["config"]
    backing, sr = sf.read(BASE / "data/source.wav", dtype="float32", always_2d=True)
    vocal, vsr = sf.read(ROOT / "audio/lego-foster/vocals.wav", dtype="float32", always_2d=True)
    mixed, msr = sf.read(ROOT / "audio/lego-foster/mix.wav", dtype="float32", always_2d=True)
    assert sr == vsr == msr
    expected = (backing + vocal * lego["vocal_gain"]) * lego["mix_gain"]
    mix_error = float(np.abs(mixed - expected).max())
    assert mix_error < 1e-6
    continuations = {}
    records = []
    for variant in ("base", "foster"):
        record = json.loads((ROOT / f"record/continuation-{variant}.json").read_text())
        assert record["status"] == "complete"
        records.append(record)
        audio, rate = sf.read(ROOT / f"audio/continuation-{variant}/continuation.wav",
                              dtype="float32", always_2d=True)
        assert rate == sr and len(audio) == 210 * sr and np.isfinite(audio).all()
        assert np.array_equal(audio[:30*sr], backing[:30*sr])
        assert np.sqrt(np.mean(audio[30*sr:]**2)) > 1e-5
        continuations[variant] = audio
    assert records[0]["parameters"] == records[1]["parameters"]
    assert records[0]["config"] == records[1]["config"]
    assert records[0]["source_sha256"] == records[1]["source_sha256"]
    assert not np.array_equal(continuations["base"][30*sr:], continuations["foster"][30*sr:])
    original, _ = sf.read(BASE / "audio/vocals.wav", dtype="float32", always_2d=True)
    n = min(len(original), len(vocal))
    vocal_difference_rms = float(np.sqrt(np.mean((original[:n]-vocal[:n])**2)))
    assert vocal_difference_rms > 1e-5
    report = dict(status="passed", adapter_tensors=len(tensors),
                  adapter_parameters=sum(v.size for v in tensors.values()),
                  lora_B_tensors_nonzero=len(b_weights), mix_reconstruction_max_error=mix_error,
                  matched_lego_parameters=True, matched_continuation_parameters=True,
                  prefix_preserved_exactly_in_both_float_wavs=True,
                  vocal_difference_rms=vocal_difference_rms,
                  listening_needed=["style", "lyric accuracy", "piano/vocal alignment",
                                    "orchestration", "30-second transition"])
    (ROOT / "record/checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
