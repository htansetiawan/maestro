"""Check source preservation through mixing and sequential LEGO context integrity."""
import hashlib
import json
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main():
    record = json.loads((ROOT / "record/generation.json").read_text())
    assert record["status"] == "complete" and record["adapter"] is None
    source = ROOT / "data/source.wav"
    assert digest(source) == record["decoded_source_sha256"]
    piano, sr = sf.read(source, dtype="float32", always_2d=True)
    expected_mix = piano.copy()
    expected_orchestra = np.zeros_like(piano)
    outputs = {}
    for name, metadata in record["outputs"].items():
        wav = ROOT / f"audio/{name}.wav"
        assert digest(wav) == metadata["wav_sha256"]
        audio, rate = sf.read(wav, dtype="float32", always_2d=True)
        assert rate == sr and audio.shape == piano.shape
        assert np.isfinite(audio).all() and np.sqrt(np.mean(audio**2)) > 1e-5
        outputs[name] = audio
    assert [entry["track"] for entry in record["layers"]] == ["strings", "woodwinds", "brass"]
    context = source
    context_errors = {}
    for entry in record["layers"]:
        name = entry["track"]
        assert entry["status"] == "complete"
        assert entry["context_sha256"] == digest(context)
        params = entry["parameters"]
        assert Path(params["src_audio"]) == context
        assert params["task_type"] == "lego" and params["instrumental"]
        assert params["lyrics"] == "[Instrumental]" and not params["thinking"]
        scaled = outputs[name] * entry["stem_gain"]
        expected_mix += scaled
        expected_orchestra += scaled
        context = ROOT / f"data/context-after-{name}.wav"
        actual_context, _ = sf.read(context, dtype="float32", always_2d=True)
        error = float(np.max(np.abs(actual_context-expected_mix*entry["context_gain"])))
        context_errors[name] = error
        assert error < 1e-6
        if name == "strings":
            assert np.array_equal(actual_context, outputs["piano-and-strings"])
    mix_error = float(np.max(np.abs(outputs["piano-and-orchestra"]-expected_mix*record["mix_gain"])))
    orchestra_error = float(np.max(np.abs(outputs["orchestra-only"]-expected_orchestra*record["orchestra_gain"])))
    assert mix_error < 1e-6 and orchestra_error < 1e-6
    report = dict(status="passed", duration_seconds=len(piano)/sr, sample_rate=sr,
                  output_count=len(outputs), mix_reconstruction_max_error=mix_error,
                  orchestra_reconstruction_max_error=orchestra_error,
                  sequential_context_max_errors=context_errors,
                  original_piano_preserved_up_to_constant_mix_gain=True,
                  all_outputs_finite_and_non_silent=True,
                  perceptual_evaluation="Not performed; test harmony, phrasing, separation and unwanted vocals by ear.")
    (ROOT / "record/checks.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
