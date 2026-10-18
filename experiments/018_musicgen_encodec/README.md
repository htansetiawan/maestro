# 018 — MusicGen-melody and EnCodec on the same melodies

[Open the listening page](index.html) for the four MusicGen clips and the
six codec round trips.

## What these models are

| Model | Year | What it is | Input | Output | Used here |
|---|---|---|---|---|---|
| EnCodec | 2022 | Neural audio codec: a convolutional encoder, residual vector quantization into 2–32 codebooks at 75 Hz (24 kHz model) or 50 Hz (32 kHz model), a decoder | Waveform | Discrete tokens, and waveform back | Round trips at 1.5–24 kbps; MusicGen's own 32 kHz codec |
| MusicGen | 2023 | Transformer language model over EnCodec tokens, trained on 20k hours of licensed instrumental music; the `melody` variant adds a chromagram of a reference recording as a condition | Text, optional reference audio | Up to 30 s of 32 kHz audio | `facebook/musicgen-melody`, 1.5B parameters |
| AudioGen | 2023 | Same architecture, trained on sound effects and environmental audio (AudioSet, AudioCaps and others) | Text | Up to 10 s of 16 kHz sound | Not run: it generates sounds, not music, and has no melody input |

MusicGen has no symbolic input. A melody reaches it as sound, reduced to a
12-bin chromagram per frame, so it sees pitch classes, not octaves, and
nothing about chord voicings.

## Runs

`record/generate.py`, transformers 5.20.1, torch 2.10.0+cu128, one seed
(20261018), guidance 3.0, 1,500 tokens (29.9 s each), 35–44 s per clip,
8.5 GiB peak. Prompt for all four: "solo acoustic grand piano, expressive
ballad, no vocals".

| Condition | Melody reference (first 30 s) |
|---|---|
| cp-guide | synthesized guide of the 17-bar *Color Purple* lead line (014) |
| cp-recording | the pianist's recording (005) |
| cp-text-only | none (control) |
| she-guide | synthesized guide of the transcribed *She* vocal line (016) |

EnCodec round trips encode and decode the first 46 s of the Color Purple
recording with `facebook/encodec_24khz` at 1.5, 3, 6, 12 and 24 kbps and with
MusicGen's 32 kHz codec (4 codebooks). MP3 only is kept.

## Measurement

Top line: the 014 method (piano transcription on the GPU, skyline, global
pitch alignment to the written melody, truncated to the notes that fall in the
first 30 s: 35 for Color Purple, 51 for She). Harmony: the 015 chroma
similarity to the audio each clip was conditioned on (`record/chroma.py`).

## Results

| Clip | Chroma vs its reference | Written notes in order | In the written octave | Longest exact run | Top-line precision | Tempo |
|---|---|---|---|---|---|---|
| cp-guide | 0.74 | 89% | 57% | 7 | 15% | 0.98× |
| cp-recording | 0.85 | 89% | 49% | 8 | 14% | 1.10× |
| cp-text-only (floor) | 0.37 | 60% | 37% | 4 | 10% | 0.93× |
| she-guide | 0.72 | 96% | 75% | 18 | 29% | 0.99× |

For scale, the synthesized guide and the recording themselves have chroma
similarity 0.51 to each other (one is a monophonic line, the other a full
arrangement).

| Codec round trip of the recording | Chroma vs recording | Top-line recall | In octave | Longest run | Precision |
|---|---|---|---|---|---|
| EnCodec 24 kHz, 1.5 kbps (2 codebooks) | 0.97 | 96% | 73% | 12 | 12% |
| 3 kbps (4) | 0.99 | 94% | 61% | 5 | 12% |
| 6 kbps (8) | 0.99 | 92% | 69% | 10 | 13% |
| 12 kbps (16) | 1.00 | 94% | 55% | 9 | 16% |
| 24 kbps (32) | 1.00 | 92% | 69% | 9 | 33% |
| MusicGen's 32 kHz codec, 4 codebooks | 0.99 | 96% | 75% | 10 | 13% |
| The recording itself (014) | 1 | 96% | 84% | 13 | 38% |

## Reading

1. **MusicGen-melody follows a melody given as sound.** With the written line
   as its reference it keeps the Color Purple contour at tempo (89% of notes
   in order against a 60% floor, chroma 0.74 against 0.37) and the She line
   closely (96%, 75% in octave, an 18-note exact run). This is the strongest
   melody following measured in this journal so far, from a model with no
   notation input at all, and at 30 s it is also the shortest.
2. **The recording is a better reference than the guide for harmony** (0.85
   against 0.74): the chromagram carries the accompaniment's pitch classes
   too, which the monophonic guide lacks.
3. **The codec is not where melody is lost.** Even at 1.5 kbps the round trip
   keeps the harmony (0.97) and the top line (96%). What low bitrates add is
   pitched artefacts that the transcriber reads as extra notes: top-line
   precision falls from 38% on the recording to 12%, and only the 24 kbps
   setting (33%) is near transparent to the transcriber. The generators'
   losses in 014 and 015 happen in the model, not in the tokens.
4. **The recall metric saturates on dense output.** MusicGen's piano is busy
   (200 top-line notes in 30 s against 35 written), so unrelated piano already
   scores 60%. Chroma similarity and the exact run carry the comparison.
5. **AudioGen is the same recipe for sound effects**; it has no place in a
   melody test and was not run.

## Files

`record/generate.py`, `record/measure.sh`, `record/chroma.py`,
`record/build_page.py`, `record/generation-log.json`; `inputs/*-events.json`
(written lines, with their first-30 s subsets); `outputs/<condition>/audio.mp3`
and `generation.json`; `outputs/measure-*.json`, `outputs/chroma.json`.
