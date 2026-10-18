# 017 — OMR against exact ground truth

[Open the results page](index.html) for the three page conditions and the
full per-staff tables.

## Question

Experiments 013 and 016 graded OMR engines against a manual lead line, which
measures the melody and nothing else. This experiment asks how much of a whole
two-staff piano page an open engine gives back when every note has a known
answer: both hands, chord tones, durations, measure count. It also asks how
fast the answer decays as the page gets worse, because the printed scores in
013 and 016 were commercial engravings, not renderings.

## Material

| Piece | Source | Measures | Right hand | Left hand |
|---|---|---|---|---|
| Mozart, Sonata in C, K. 545, first movement | KernScores `**kern` (CCARH), `source/k545-1.krn` | 74 incl. pickup | 585 attacks, 600 notes | 593 attacks, 678 notes |
| Beethoven, Ode to Joy theme, easy arrangement | Encoded here with music21, `source/ode-to-joy.musicxml` | 16 | 62 attacks (melody) | 32 attacks, 64 notes (root–fifth dyads) |

Both were rendered to pages by Verovio at 300 dpi (`record/prepare.py`), then
copied into three conditions:

- **clean**: the rendering as is;
- **degraded**: 0.5° skew, 1.1 px Gaussian blur, noise, hard threshold at 150 (a photocopy);
- **harsh**: half resolution (about 150 dpi), 1.5° skew, lighting falling to 62% across the page, blur, sensor noise, JPEG at quality 40 (a phone photograph; `record/prepare_harsh.py`).

Engines: homr 0.7, oemer 0.1.8 (`--without-deskew`), Audiveris 5.11, each
given the page images and nothing else (`record/run_omr.sh`,
`record/run_omr_harsh.sh`). Grading (`record/compare.py`) aligns each staff's
attack sequence to the truth with the 014 alignment and reports exact recall,
recall counting every pitch in the truth including chord tones, longest exact
run, duration agreement among matched notes, and precision.

## Results

### Mozart K. 545, first movement (74 measures)

| Pages | Engine | Measures | RH attacks exact | RH notes incl. chord tones | RH longest run | RH durations right | LH attacks exact | LH notes incl. chord tones | LH precision |
|---|---|---|---|---|---|---|---|---|---|
| clean | homr 0.7 | 73 | 100% | 100% | 585 | 99% | 100% | 100% | 100% |
| clean | oemer 0.1.8 | 73 | 99% | 99% | 260 | 96% | 99% | 99% | 99% |
| clean | Audiveris 5.11 | 73 | 100% | 100% | 585 | 100% | 91% | 92% | 96% |
| degraded | homr 0.7 | 73 | 100% | 100% | 585 | 99% | 100% | 100% | 100% |
| degraded | oemer 0.1.8 | 69 | 98% | 98% | 172 | 89% | 99% | 99% | 99% |
| degraded | Audiveris 5.11 | 73 | 99% | 99% | 404 | 100% | 91% | 91% | 96% |
| harsh | homr 0.7 | 73 | 100% | 100% | 359 | 99% | 100% | 100% | 100% |
| harsh | oemer 0.1.8 | 66 | 74% | 74% | 80 | 95% | 89% | 88% | 82% |
| harsh | Audiveris 5.11 | 49 | 36% | 37% | 20 | 23% | 31% | 32% | 87% |

The missing measure in every row is the pickup, which the grader counts and
the engines fold into the first bar. Audiveris lost page 3 of the harsh set
to an export crash (null measure in clef lookup), hence 49 measures.

### Ode to Joy, easy arrangement (16 measures)

| Pages | Engine | Measures | RH attacks exact | RH notes incl. chord tones | RH longest run | RH durations right | LH attacks exact | LH notes incl. chord tones | LH precision |
|---|---|---|---|---|---|---|---|---|---|
| clean | homr 0.7 | 16 | 100% | 100% | 62 | 100% | 100% | 100% | 100% |
| clean | oemer 0.1.8 | 16 | 100% | 100% | 62 | 100% | 100% | 100% | 100% |
| clean | Audiveris 5.11 | 16 | 100% | 100% | 62 | 100% | 100% | 100% | 100% |
| degraded | homr 0.7 | 16 | 100% | 100% | 62 | 100% | 100% | 100% | 100% |
| degraded | oemer 0.1.8 | 16 | 100% | 100% | 62 | 97% | 100% | 100% | 100% |
| degraded | Audiveris 5.11 | 16 | 100% | 100% | 62 | 100% | 100% | 100% | 100% |
| harsh | homr 0.7 | 16 | 100% | 100% | 62 | 100% | 100% | 100% | 100% |
| harsh | oemer 0.1.8 | 16 | 63% | 63% | 21 | 85% | 78% | 78% | 53% |
| harsh | Audiveris 5.11 | 16 | 100% | 100% | 62 | 97% | 81% | 81% | 81% |

## Reading

1. **On a clean modern engraving, open OMR is essentially solved for notes.**
   All three engines return every pitch of both hands of K. 545 (homr: 585 of
   585 right-hand attacks in one unbroken run, every left-hand note, 99% of
   durations). The chord tones in the left hand, which 013 could not grade,
   are read as well as single notes.
2. **The photocopy condition changes almost nothing.** Skew of half a degree,
   blur and a hard threshold cost oemer four measures and a few durations;
   homr and Audiveris are unchanged.
3. **The phone-photo condition separates the engines.** homr still reads
   everything (its longest run drops from 585 to 359 because of one slip).
   oemer falls to 74% on the Mozart right hand and 63% on the simpler piece.
   Audiveris, which is built for scans, loses a page to a crash and half of
   what remains.
4. **The gap in 013 and 016 is therefore not note recognition.** The same homr
   that reads 100% here read 86% of the Color Purple melody and 79% of the She
   vocal line. What those pages have and these do not: a three-staff
   piano-vocal layout, lyrics between staves, chord symbols, older engraving
   fonts, and real scan artefacts. The next benchmark should add those one at
   a time, starting with lyrics under the staff and a vocal-plus-piano system.
5. **Chord symbols and text remain unread by every engine in every condition**
   (none are present on these pages, but 013 showed zero of 98 on a page that
   had them), so a lead sheet still cannot be read end to end by open tools.

## Files

`source/` encodings and `*-truth.json`; `inputs-manifest.json`; `record/`
scripts; `outputs/comparison.json`; `preview/` page thumbnails. Page images
and engine outputs are regenerated by `record/prepare.py`,
`record/prepare_harsh.py` and the run scripts and are not committed.
