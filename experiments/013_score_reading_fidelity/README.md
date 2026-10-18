# 013 — Reading the printed score: three OMR engines against the manual lead line

[Open the inspection page](index.html) to hear each engine's two-staff reading
and compare the agreement table.

## Question

Experiment 007 conditioned YuE2 on a hand-made reduction of the five scanned
pages of *Theme from The Color Purple* (Shiori Aoyama's solo-piano arrangement).
Before asking whether the model follows a score, this experiment asks whether
software can read the score at all, and how much of the printed arrangement
could reach YuE2's score input even if reading were perfect.

## Method

The scan (five CCITT bitmaps at about 300 dpi) was rendered to PNG pages and
read by three optical music recognition engines on CPU:

| Engine | Version | Kind | Run |
|---|---|---|---|
| Audiveris | 5.11.0, Ubuntu 24.04 package unpacked without installation | Rule-based, Java 21 | One book per page; the whole-PDF book crashed on page 4 and refused to export |
| homr | 0.7.0 | Vision transformer with ONNX Runtime 1.24 | One page per call |
| oemer | 0.1.8 | U-Net segmentation plus classifiers | Needs ONNX Runtime 1.16; a separate Python 3.11 environment |

Each engine writes MusicXML. `record/compare.py` parses it with music21,
takes the highest note at each right-hand attack as the engine's top line, and
aligns that sequence globally to the 298 notes of the manual lead line with the
same pitch-sequence alignment used for audio in experiment 014. Recall is the
share of manual notes found (any octave), exact recall requires the written
octave, and precision is the share of top-line attacks that belong to the
melody. Measure counts are compared page by page against the manual table
(12, 17, 19, 20 and 20 measures). The script also counts every note the engine
read on both staves, which is the basis of the loss ledger below.

The page images, the engines' MusicXML, their Audiveris book files and the
derived MIDI are kept out of git because they reproduce a copyrighted
arrangement in editable form. The comparison summaries and the synthesized
MP3 renderings of each reading are published.

## Results

| Engine | Measures found (of 88) | Melody recall | Exact octave | Top-line precision | Chord symbols read (of 98) |
|---|---|---|---|---|---|
| Audiveris 5.11 | 77 | 50% | 45% | 89% | 0 |
| homr 0.7 | 83 | 86% | 85% | 92% | 0 |
| oemer 0.1.8 | 84 | 73% | 69% | 84% | 0 |

homr found every measure on pages 1, 2, 3 and 5 and 15 of 20 on page 4; its
misses are concentrated there. oemer found 84 measures but read fewer of the
melody notes correctly. Audiveris lost two measures on each of pages 1 and 2
and six on page 4, and its rhythm pass threw exceptions on several systems.
No engine produced a chord symbol: Audiveris reported that its Tesseract OCR
had no language data, and the other two do not read text. The manual table
remains the only source of the 98 chord symbols.

No engine reproduced the printed measure grid exactly, so the per-measure
identity count on the page is not computed. The alignment-based recall is the
reliable figure.

## What the page holds versus what YuE2 can take

From homr's reading of both staves (the most complete):

| Layer | Notes | Reaches YuE2's score input? |
|---|---|---|
| Top of the right hand (lead melody) | 276 attacks | Yes, as the `Ins` voice, after rounding 35 tuplet events to a 1/32-quarter grid |
| Right-hand chord tones under the melody | 189 | No; only the chord label survives |
| Left hand (bass and arpeggios) | 373 | No; only a slash bass in the label |
| Chord symbols | 98 (manual) | Yes, except E7+5, which is outside the fifteen native qualities |
| Grace notes, dynamics, pedal, ritardando, fermata | 7 graces and the marks | No |

About a third of the sounding notes on the page can be expressed in the model's
input. The rest is regenerated from chord labels and the style prompt. This is
a property of the interface, not of any OMR engine.

## Reproduce

```bash
# Audiveris, one book per page image (chord names need Tesseract language data, absent here)
~/maestro-runtime/audiveris/extracted/opt/audiveris/bin/Audiveris -batch -export \
  -output outputs/audiveris-pages source-private/pages/page-{1,2,3,4,5}.png
record/run_homr_oemer.sh                                   # homr (analysis venv); oemer needs its own venv
~/maestro-runtime/analysis-venv/bin/python record/compare.py
~/maestro-runtime/analysis-venv/bin/python record/render_midi.py outputs/homr/two-hands.mid outputs/homr/two-hands.mp3
python3 record/build_page.py
```

Engines and environments live under `~/maestro-runtime` (see the repository
notes). The manual reference is `experiments/007_color_purple_sheet_yue2/inputs/source-events.json`.
