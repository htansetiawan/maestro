# 014 — What YuE2 keeps of a score: a 17-bar ablation

[Open the listening page](index.html) for the five clips, the written-melody
guide, the adherence table and the singing diagnostic.

## Question

Experiment 007 fed YuE2 a lead-line reduction of *Theme from The Color Purple*
and produced 5:39 of piano whose score following was never measured. This
experiment takes the first 17 bars of the same reduction (pickup, intro and
section A; 51 melody notes, 17 chord symbols, 44 s at 88 BPM) and varies only
what the score interface carries. Style prompt (solo acoustic grand piano, no
vocals), empty lyrics, runtime and decoder are shared.

| Condition | `Ins` voice | `Vocal` voice | `cot` | Seeds |
|---|---|---|---|---|
| melody-only | melody | rests | melody | 20261017 |
| melody-chords (the 007 recipe) | melody | rests + chord symbols | full | 20261017, 20261018 |
| melody-chords-bass | melody | chord-root bass line (one held note per chord, F2–E3) + chord symbols | full | 20261017 |
| model-composed | none: YuE2 plans its own score | | full | 20261017 |

The bass condition probes whether the second voice can smuggle a left-hand
line into an interface that is otherwise melody and labels. `record/abc_two_voice.py`
writes both voices; for the melody-chords condition its output is identical to
the official skill compiler, and every score passes the official parser.

## Runtime

YuE2-3B at the pinned revision, YuE2-Vae decoder, BF16, 17 GiB budget with AR
offloading, 3,500-token semantic cap. One model load, five renders, 40 to 115 s
each, peak allocation under 8 GiB. Only the 256 kbit/s MP3 and the small
records are kept, per the MP3-only policy.

Four of the five clips ran to the 3,500-token cap (140 s) instead of ending
near the 44-second score; only the bass condition ended on its own, at 85 s.
Supplying a 17-bar score does not make the model stop after 17 bars.

## Measurement

Each clip is transcribed with the ByteDance piano transcription model (GPU),
the highest note at each attack is taken as the top line, and that sequence is
globally aligned to the written melody (`record/measure.py`). Melody recall
counts written notes found in order in any octave; "written octave" requires
the register on the page; top-line precision is the share of top-line attacks
that are melody notes; the longest exact run counts consecutive written notes
reproduced in order and octave; tempo is the fitted time stretch of matched
notes relative to 88 BPM. The first 60 s of each clip is the fair window.

The same measurement on the human recording sets the ceiling:

| Reference | Melody recall | Written octave | Precision | Longest run | Tempo |
|---|---|---|---|---|---|
| Recording, first 52 s, bars 0–16 | 96% | 84% | 38% | 13 | 1.09× |
| Recording, 3:30, all 87 bars | 79% | 45% | 40% | 18 | 0.92× |
| Experiment 007 output, 5:39, all 87 bars | 63% | 18% | 38% | 7 | 1.53× |

Precision is low even for the pianist because accompaniment attacks also reach
the top line when the melody rests. The 007 row is last week's result graded
for the first time: pitch classes are present but mostly in the wrong octave,
in short runs, and stretched 1.53×, which matches its 5:39 against a 3:49 score.

## Results, first 60 seconds

| Condition | Melody recall | Written octave | Precision | Longest run | Tempo |
|---|---|---|---|---|---|
| melody-only | **80%** | **63%** | 33% | **10** | 1.33× |
| melody-chords, seed 20261017 | 67% | 14% | 26% | 2 | 0.96× |
| melody-chords, seed 20261018 | 67% | 39% | 37% | 5 | 1.28× |
| melody-chords-bass | 75% | 45% | 19% | 7 | 1.10× |
| model-composed | 53% | 35% | 14% | 4 | 1.18× |

Over whole clips the recall figures rise (92% for melody-only and for the first
melody-chords seed) while the fitted tempo climbs to 2.3–3.6×, which means the
melody's pitches recur across the 140 s rather than being played once in time.
The 60-second figures are the ones to read.

## Reading

- The melody-only score was followed best: four of five written notes in the
  first minute, ten in a row in the written octave, at a tempo about a third
  slower than marked. That is a real but loose imitation.
- Adding chord symbols, the 007 recipe, made following worse in both seeds
  (longest runs of 2 and 5). With `cot=full` the model seems to treat the lead
  line more freely. Two seeds disagree by 25 points on the octave figure, so
  this is a direction, not a ranking.
- The bass probe scored between the two, but Whisper transcribes a long run
  of sung "ah" syllables from it despite the no-vocals prompt: notes in the
  `Vocal` voice are sung. The second voice cannot carry an instrumental bass.
  Whisper also returns syllable-like text for the model-composed clip, which
  needs listening to confirm.
- The model-composed clip, with no score, still shares 53% of the melody's
  pitch classes in order, which is the floor this method gives to any F-major
  (or here G-major) piano music. Its plan was in G major at 87 BPM although
  the prompt asked for F major at 88, so the style prompt did not fix the key.

Together with experiment 013, the loss is located: about a third of the printed
notes can be expressed in YuE2's score input, and of the melody that is sent,
roughly two thirds to four fifths comes back audibly in the first minute, loosely
timed, and less when chord symbols are added. The accompaniment is the model's
own throughout.

## Reproduce

```bash
python3 record/prepare.py                                              # builds prepared/<condition>/
~/maestro-runtime/yue2-venv/bin/python record/generate.py             # GPU, 17 GiB free required
MEASURE_DEVICE=cuda ~/maestro-runtime/yue2-venv/bin/python record/measure.py \
  --events inputs/excerpt-events.json --audio outputs/*/audio.mp3 --output record/adherence-outputs-full.json
python3 record/build_page.py
```

`generate.py` refuses to overwrite an existing attempt. Inputs come from
`experiments/007_color_purple_sheet_yue2/inputs/source-events.json`; the
excerpt and both reference guides are in `inputs/`.
