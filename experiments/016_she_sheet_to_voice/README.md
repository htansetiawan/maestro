# 016 — She: from a scanned song sheet to a singer

[Open the listening page](index.html) for the transcribed line, the YuE2
render, the separated voice and the tables.

## Question

Experiment 013 measured how much of a printed piano score three open OMR engines
recover; experiment 014 measured how much of a written melody YuE2 keeps. This
experiment chains the two on a song: *She* (Aznavour and Kretzmer, 1974), a
three-page piano-vocal score. How much of the vocal line does OMR read, and
when the line, its chord symbols and the printed lyrics go to YuE2 as a lead
sheet, does the singer sing it?

## Inputs

The PDF and its page crops are in `source-private/` (in copyright, not
published). A manual transcription of the vocal staff is the reference:
33 printed bars, 195 notes, both lyric lines, chord symbols
(`inputs/vocal-transcription.json`). Three bars carry a mark of uncertainty
(15, 22, 33). The song form was linearized as intro, verse, verse, bridge,
verse with the second lyric, coda: 40 bars, 248 melody notes, about 134 s at
70 BPM (`inputs/linearized-events.json`, `inputs/melody.mid`,
`inputs/melody-guide.mp3`).

## Step 1: the three engines read the vocal staff

`record/run_omr.sh` ran homr 0.7 (three pages), oemer 0.1.8 (two pages; the
third produced no score) and Audiveris 5.11 (which split pages into separate
"movements"). `record/vocal_lines.py` takes each engine's first part as the
vocal line; `record/compare_vocal.py` aligns it to the transcription.

| Engine | Notes in its first part | Melody recall (any octave) | Exact octave | Precision | Longest exact run |
|---|---|---|---|---|---|
| homr 0.7 | 253 | 79% | 74% | 61% | 43 |
| oemer 0.1.8 | 178 | 45% | 42% | 49% | 9 |
| Audiveris 5.11 | 125 | 44% | 42% | 69% | 14 |

All three engines misread the opening of each verse in the same way: the
descending sequence of bars 1–6 (the phrase stated on E5, then C5, then A4)
comes back with bars 3, 5, 12 and 14 collapsed onto the C5 version. homr read
the bridge and the coda almost perfectly (a 43-note exact run). No engine
returned the chord symbols or the lyrics; both were typed from the sheet.

## Step 2: YuE2 sings the transcribed line

`record/prepare.py` writes the request: `Vocal` voice carries the 248-note
line with 58 chord symbols, `Ins` voice rests, lyrics tagged `[Verse]`,
`[Verse]`, `[Bridge]`, `[Verse]`, `[Outro]`, `cot=full`, seed 20261018,
style "English, classic pop ballad, warm expressive male baritone, piano
accompaniment". `record/generate.py` renders with the 014 runtime (YuE2-3B
pinned revision, BF16, 4,500-token semantic cap).

| | |
|---|---|
| Render | 58 s, peak 7.8 GiB |
| Audio | 180 s, stopped by the token cap (lead sheet is 134 s) |
| Kept | `outputs/she-vocal-20261018/audio.mp3`, `vocals.mp3` (Demucs stem), request, plan, ABC |

## Step 3: does the singer follow the line?

`record/measure_vocal.py`: Demucs htdemucs separates the voice, pYIN tracks
its pitch, runs of stable pitch of at least 80 ms become notes, and the note
sequence is aligned to the written line with the 014 alignment.

Calibration first. On the synthesized guide (no separation needed) the tracker
returns 176 notes, all correct: 71% of the 248 written notes, because repeated
pitches merge into one segment. 71% is therefore the ceiling of this measurement.

| | YuE2 render |
|---|---|
| Sung notes found | 187 |
| Written notes sung in order, any octave | 37% (ceiling 71%) |
| Written notes in the written octave | 8% |
| Longest exact run | 6 |
| Tempo | 1.27× slower than 70 BPM |

The singer's median pitch is E3 against a written median of G4: the baritone
sings the treble-clef line an octave down, as a male singer would, so most of
the matches are octave matches and "exact octave" is not a meaningful column
here. Within the ceiling, YuE2 sang about half of the line in order, with
short exact runs; the voice is continuous (97% voiced) and the render runs
long past the lead sheet. Rerunning the alignment on the MP3 copy of the stem
instead of the lossless one moved recall by about ten points, so treat the
figure as approximate.

## Reading

OMR reaches 79% of a printed vocal line on a clean commercial engraving (homr),
and the remaining fifth is systematic (sequence bars collapsed), not random.
Downstream, YuE2 treats the line as a suggestion: the song is sung, in the
right register and roughly the right contour, but not the written notes in
the written order. The singer-following gap is larger than the reading gap.

## Files

`record/` scripts and `record/vocal-adherence.json`; `outputs/vocal-recall.json`
and `outputs/vocal-agreement.json` (OMR grading); `prepared/score.abc` and
`prepared/request.json` (what YuE2 received). Engine MusicXML, the PDF and the
lyrics are local only.
