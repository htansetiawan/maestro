# Experiments

The new [ACE audio personalization experiment](001_ace_audio_personalization/README.md)
is experiment-scoped and uses `uv`. It prepares original piano/violin recordings,
trains an ACE-Step LoRA, collects human or AI audio preferences, branches into
an experimental offline preference update, and builds a matched-seed listening
index. No ACE GPU run has been completed yet; see its README for exact setup.

The files below are the older **symbolic AMT** experiment scaffold. They are
independent of ACE-Step and are not part of the audio training pipeline.

Scaffold for the first Maestro experiments. Order matters.

| File | What it does | Tested? |
|---|---|---|
| `rewards.py` | Programmatic annotation-compliance rewards + build log | **yes**, unit-tested locally |
| `01_smoke_test.py` | Load AMT, generate, infill around a pinned melody, score it | written against the verified API, not run on GPU |
| `requirements.txt` | Deps | — |

## Why not Music Transformer

Music Transformer (2018) is the right *idea* and the wrong *starting codebase*. The
reference implementation lives in `tensor2tensor` (TensorFlow 1), which is effectively
unmaintained; the community PyTorch ports are unvalidated re-implementations. The paper
also never reports a parameter count — from the published config (6 layers, d_model 512,
8 heads, L=2048, 388-event vocabulary) it works out to roughly 20–40M depending on the
feed-forward width. That is **smaller than a single layer's worth of a modern 3B LLM**.

Start from the **Anticipatory Music Transformer** instead: Apache 2.0, PyTorch, on the
Hub, trained on Lakh MIDI (CC-BY), and — decisively — its anticipation mechanism gives
you *infilling with arbitrary pinned material* out of the box, which is exactly the
primitive the compose → annotate → compile loop needs.

| Checkpoint | Params |
|---|---|
| `stanford-crfm/music-small-800k` | 128M |
| `stanford-crfm/music-medium-800k` | 360M — best model in the paper |
| `stanford-crfm/music-large-800k` | larger, extra training data |

On a 48 GB card, none of this is compute-bound. A full fine-tune of the 360M model fits
comfortably in bf16 with room for a large batch. **Your constraint is data and problem
choice, not VRAM.** Resist the urge to reach for a bigger model.

## The reward module is the research, not the plumbing

GRPO needs a reward it can trust. "Is this good music?" is not that. "Did the model
honour the composer's marks?" is — and `rewards.py` computes it: chord-tone compliance
weighted by duration, key, register, density, leap size, and one hard multiplicative
constraint, `frozen_intact`, which zeroes the entire reward if the model overwrote
material the human pinned.

That last one is the point. A compile that silently rewrites the composer's own notes has
failed no matter how pretty the result, and no existing symbolic model is trained against
that objective.

```
$ python -c "..."   # see the test in the commit message
--- HONOURS the annotations
compiled 8 notes over 8 beats — reward 0.886
  [FAIL] chord    0.750  2 sustained non-chord tone(s): pitch 65 over Ebmaj7 for 1.0b
  [ok  ] frozen   1.000  all pinned notes intact
--- IGNORES them
compiled 4 notes over 8 beats — reward 0.000
  [FAIL] frozen   0.000  DESTROYED 2/2 pinned note(s)
```

**Known limitation, and the first thing to fix:** strict chord-tone membership penalises
9ths, 11ths and passing tones — note the 0.750 above, where an F over Ebmaj7 is scored as
a miss when it is really a colour tone. Lush extended harmony is precisely the idiom this
project cares about, so the reward needs a tiered scheme (chord tone / colour tone /
avoid note), weighted by metrical position. Getting that tier right *is* a contribution.

## Sequence

1. Run `01_smoke_test.py`. Confirm you can infill around pinned material.
2. Build a personal corpus — your own Nord captures. See the note on style below.
3. Supervised fine-tune on that corpus; measure whether infills move toward your idiom.
4. Only then GRPO, with `rewards.py` as the verifier.

Step 3 before step 4, always. If SFT alone gets you most of the way, that is a result
worth reporting, and it tells you how much headroom RL actually has.
