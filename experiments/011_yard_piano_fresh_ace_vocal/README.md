# 011 — Original piano with a fresh ACE-Step vocal

The user selected a fresh ACE-Step LEGO take conditioned on the original
3:30 *Theme from The Color Purple* recording, after preferring experiment 009's
unconditioned YuE2 song to the sheet-conditioned versions.

- [Piano + new vocal — 3:30](https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/011_yard_piano_fresh_ace_vocal/audio/mix.mp3)
- [Isolated generated voice — 3:30](https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/011_yard_piano_fresh_ace_vocal/audio/vocals.mp3)
- [Mix FLAC](audio/mix.flac) · [Vocal FLAC](audio/vocals.flac)
- [Listening page](index.html) · [Exact lyrics](inputs/lyrics.txt)

## What this run does

ACE-Step `acestep-v15-xl-base` receives the original piano waveform through
`src_audio`, the LEGO instruction `Generate the VOCALS track based on the audio context:`,
a caption and the full lyrics from experiment 009. It generates a vocal stem,
which is then mixed with the decoded original recording. No sheet, MIDI, ABC,
YuE2-generated audio, LoRA or fine-tuning is used. This is a fresh stochastic take,
not evidence that the alignment limitations reported in earlier LEGO runs are fixed.

Compared with experiment 003: the same source, base checkpoint, 50 steps, guidance
7.0 and disabled LM/CoT; new lyrics, a revised baritone caption and seed 20261007.
Several inputs change, so this is not a controlled single-variable comparison.

## Actual result and preservation check

- Duration: 210.346667 seconds; 48 kHz stereo.
- Original piano is neither regenerated nor time-stretched.
- Mix formula: `(decoded_piano + 0.763167788 * generated_vocal) * 0.833538176`.
- Maximum reconstruction error from the saved lossless mix: 5.96e-08.
- Recovering the decoded piano after undoing gains and subtracting the added vocal
  gives a maximum error of 1.79e-07 (PCM/float rounding).
- Mix peak: 0.950000; full-scale/clipped samples: 0.
- Vocal length adjustment for mixing: 1280 samples
  (positive means silence padded at the end; negative means trimmed at the end).
- Vocal-only delivery gain: 0.950000000; native float32 output
  remains unchanged locally. MP3s are 256 kbps conversions of the delivered FLACs.
- Generation after initialization: 34.1 seconds;
  peak Torch allocation: 12.04 GiB.

These checks establish sample preservation and export integrity, not musical fit.
Lyric completeness, vocal isolation and alignment require listening. The generated
stem may contain accompaniment leakage; no cleanup or time warping is applied.
No ASR or perceptual quality score is claimed.

## Exact caption

English, warm expressive male baritone singing a nostalgic and hopeful pop ballad about Harvard Yard, red brick buildings, sheltering trees, friendship and memories. Create a singable vocal melody that fits the source piano harmony, pulse, rubato and phrase boundaries. Let the piano establish the introduction before singing. Intimate clear storytelling in the verses, warm lyrical choruses, legato delivery, restrained vibrato, natural breaths and instrumental spaces. Generate the solo lead vocal track only.

## Records and reproduction

[Input request](inputs/request.json) · [Actual runtime settings and output hashes](record/generation.json) ·
[Mix checks](record/quality.json) · [Generator](record/generate.py)

ACE code revision `ca1e85fe9430179831e6bc6be790c332190a3866`. Existing local checkpoint cache; its
configuration SHA256 is `174cf8c4afc2c41212546b4dca9afb11e7958f8b1e1a770d7cd009a82d72a6f1`.
Source filename `theme_from_the_color_purple.mp3`; SHA256 `1a6ab9f251f1bc1ef278583b976c582aee39a67cde57536757b9bd4c1b0824a7`.
The public runtime record replaces local source paths and excludes private logs;
the full runtime record, decoded source and native float32 WAV stay local and ignored.
The model weights are not included in Git.

```sh
/tmp/maestro-ace-step/.venv/bin/python experiments/011_yard_piano_fresh_ace_vocal/record/generate.py
python3 experiments/011_yard_piano_fresh_ace_vocal/record/build_delivery.py
```

The generator refuses to overwrite an existing take; use a separate experiment
folder for another run. CUDA free-memory preflight requires 17 GiB, and the same
0.34 per-process memory fraction as experiment 003 is retained.
