# 006 — YuE2 score control evaluation

[Open the listening comparison](index.html). Hear the simple motif guide first,
then the supplied-score and model-composed candidates. MP3 and lossless FLAC
outputs are retained, together with the exact score, request, configuration,
timings, and weight hashes.

## Question and design

Can YuE2 generate coherent piano-accompanied singing and follow an explicit
vocal melody? This is a small local pilot, not a reproduction of the authors'
benchmark or an A/B comparison against ACE-Step or Suno.

The four initial candidates use two seeds, each with the same lyrics, style,
and `cot="melody"` mode. The intervention is a supplied melody versus a melody
composed by YuE2. No candidates are discarded or selected by an evaluator.

The supplied melody is the user's two scale-degree phrases, repeated once:

```text
5_ 1 3 6_ 1 4 2 3
5_ 1 3 6_ 1 4 6 5
```

Assumptions: C major, `1=C4`, underscore lowers an octave, 90 BPM, 4/4,
every token one quarter note. There are 32 notes over eight bars (21.33 seconds).
Four original eight-syllable lyric lines concern memories of Harvard Yard.
The intended one-syllable-per-note mapping is not a forced alignment input.
The guide is deterministic additive synthesis, not a YuE2 output.

The original piano recording is not used. YuE2 generates the complete recording;
this experiment does not test keeping a source waveform and adding a stem.

## Observations

Initial rendering completed for all four candidates. Technical checks verify
finite, non-silent 48 kHz stereo audio and saved-artifact integrity. Supplied
scores match the input exactly in the saved files. These checks do not measure
the notes sung in the audio.

| Candidate | Audio length | Model end token | Score tempo | Nominal score length |
|---|---:|---|---:|---:|
| Supplied motif, seed 20261005 | 49.96 s | Yes | 90 BPM | 21.33 s |
| Supplied motif, seed 20261006 | 24.32 s | Yes | 90 BPM | 21.33 s |
| Model-composed, seed 20261005 | 72.00 s | No; initial token cap | 72 BPM | 80.42 s |
| Model-composed, seed 20261006 | 49.96 s | Yes | 65 BPM | 55.38 s |

Both composed scores depart from the requested 90 BPM. Total waveform duration
includes introductions, endings, and potential repeats, so a duration difference
alone is not a vocal-alignment measurement. Whisper's independent lyric diagnostic
suggests an extra repeat in the first supplied-score candidate; verify by ear.
ASR also confuses some words and is not a melody or pronunciation ground truth.

The initial generation cap was 1,800 semantic tokens. Because it truncated the
80.42-second model-composed plan, `extend_limit.py` rerenders that exact saved
plan with the same seed and a 3,500-token cap. The original remains in the comparison.
This addresses a test-budget limitation, not a choice of the best musical sample.
The extended attempt finished at 79.96 seconds without truncation.
See [checks.json](record/checks.json) for all measurements.

**Musical assessment remains pending.** Judge vocal realism, piano–voice coherence,
melody/register accuracy, rhythm, lyric placement, extra repeats, and usability
separately. A valid symbolic plan is not proof of control over the rendered audio.

## Runtime and reproducibility

- YuE source: `3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10`.
- Model: `m-a-p/YuE2-3B`, revision `c044757a011169583f363168348ae380946efff8`.
- Listening decoder: `m-a-p/YuE2-Vae`, revision `152733a19ad43aa67e367f9b5503ef8075bb5126`.
- BF16 model, FP32 decoder, default 32-step midpoint acoustic synthesis.
- Torch backend, no quantization, AR offloading, 512-frame decoder chunks,
  17 GiB configured memory budget. Initial peak allocated memory: 7.54 GiB or less.
- Existing RTX PRO 5000 Blackwell; another GPU workload was left running.
- Python 3.12 environment under `/tmp/maestro-yue2/.venv`, reusing the existing
  ACE environment's PyTorch 2.10.0 CUDA 12.8 installation through a `.pth` file.
  YuE2 dependencies are overlaid in the new environment; the ACE environment
  is unchanged. Full versions and all requests are in [protocol.json](record/protocol.json).

```bash
/tmp/maestro-yue2/.venv/bin/python record/run.py
/tmp/maestro-yue2/.venv/bin/python record/extend_limit.py
/tmp/maestro-yue2/.venv/bin/python record/check.py
/tmp/maestro-yue2/.venv/bin/python record/transcribe.py
/tmp/maestro-yue2/.venv/bin/python record/build_listening.py
```

Run these from this experiment directory. `run.py` retains existing attempts;
the extension refuses to overwrite its directory. Checkpoints remain in the
local Hugging Face cache. Large latent/token arrays remain local and ignored;
the original full artifact manifests include their hashes, so full verification
requires those arrays or a fresh reproduction, not just a Git checkout.

## Sources and next step

- [Official generation guide](https://github.com/multimodal-art-projection/YuE/blob/3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10/docs/generation.md).
- [Official cover workflow](https://github.com/multimodal-art-projection/YuE/blob/3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10/docs/covers.md).
- [Audio-to-Score research discussion](../../journal/entries/2026-10-05.md).

After listening, evaluate audio-to-score separately against reviewed notation.
Converting a prediction into YuE2's ABC input is an additional representation
conversion test; a plausible regenerated song cannot certify the transcription.
