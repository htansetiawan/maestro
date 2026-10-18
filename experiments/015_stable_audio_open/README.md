# 015 — Stable Audio Open over the same piano

[Open the listening page](index.html) for the seven clips, the source excerpt
and the similarity table.

## Question

Stable Audio Open 1.0 is a text-to-audio latent diffusion model (47 s, 44.1 kHz
stereo) with no symbolic input. Beside the YuE2 trials it answers two things:
what it produces for the same solo-piano prompt with no score, and how much of
the original recording survives when that recording is the starting point,
including a LEGO-style request to add an orchestra.

| Condition | Input | Noise level σ |
|---|---|---|
| `t2a-piano-2026101{7,8}` | Prompt only, two seeds | — |
| `a2a-piano-sigma{0.5,2,8}` | First 47 s of the recording plus the piano prompt | 0.5, 2, 8 |
| `a2a-orchestra-sigma{2,8}` | Same excerpt plus "piano with string orchestra and woodwinds" | 2, 8 |

Audio-to-audio encodes the source, adds noise at the given k-diffusion sigma and
samples from there; lower keeps more of the source. The three levels are a first
sweep, not tuned values. All runs: 100 steps, CFG 7, `dpmpp-3m-sde`, fixed seed,
one normalized 256 kbit/s MP3 kept per condition.

## Runtime

`stabilityai/stable-audio-open-1.0` (gated; the license had to be accepted on
the account first), stable-audio-tools 0.0.19 on Python 3.11 with torch 2.10,
torchvision 0.25 and torchaudio 2.10 from the same CUDA 12.8 build. The package
would not install on Python 3.12 (its `pathtools` dependency imports the removed
`imp` module), and two mismatched wheels pulled in by its dependency tree had to
be pinned back. Weights download took 498 s; each clip rendered in about 20 s
with a peak allocation of 10 GiB.

## Measurement

`record/measure.py` computes chroma similarity between the source excerpt and
each output (mean frame-wise cosine of CQT chroma after a small lag search) and
reuses experiment 014's top-line measurement: both clips are transcribed with
the ByteDance piano model, the highest note at each attack is aligned, and
recall is the share of the source's top-line notes that reappear. The source
against an MP3 of itself gives the ceiling. These grade note content, not sound.

| Clip | Chroma similarity | Source top line kept | In the right octave | Precision |
|---|---|---|---|---|
| Source vs its own MP3 (ceiling) | 1.00 | 99% | 99% | 99% |
| Text only, seed A | 0.43 | 35% | 2% | 30% |
| Text only, seed B | 0.41 | 37% | 5% | 51% |
| Recording → piano, σ 0.5 | 0.99 | 71% | 51% | 66% |
| Recording → piano, σ 2 | 0.92 | 76% | 55% | 46% |
| Recording → piano, σ 8 | 0.54 | 43% | 21% | 47% |
| Recording → orchestra, σ 2 | 0.93 | 74% | 53% | 47% |
| Recording → orchestra, σ 8 | 0.56 | 48% | 16% | 48% |

## Reading

- With no score, the model's piano shares about a third of the source's
  top-line pitch classes in order and almost none in the right octave. That is
  the floor this method gives to unrelated music in the same key and style.
- The lightest audio-to-audio pass keeps the harmony almost exactly (0.99) yet
  returns only half the top-line notes in their octave. The autoencoder round
  trip and the sampler already blur the melody's register; this is a cost that
  exists before any musical change is requested.
- σ = 2 keeps the harmony under either prompt (0.92 and 0.93). σ = 8 mostly
  regenerates the piece. Whether the orchestra prompt adds orchestral parts or
  simply a different piano needs listening; the numbers only say the harmony
  stayed.
- Unlike YuE2, nothing here can be told which notes to keep. Preservation is a
  side effect of the noise level, not a control.

## Reproduce

```bash
~/maestro-runtime/sao-venv/bin/python record/generate.py
MEASURE_DEVICE=cuda ~/maestro-runtime/yue2-venv/bin/python record/measure.py
python3 record/build_page.py
```

`generate.py` exits 3 while the weights are gated and retains existing attempts.
The source excerpt is the local, gitignored copy of the recording used by
experiments 005 and 014.
