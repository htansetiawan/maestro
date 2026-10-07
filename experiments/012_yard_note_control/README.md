# 012 — A 25-second note-controlled vocal over the original piano

This experiment separates writing the vocal melody from rendering its voice.
A short line was composed against audio-derived timing anchors from the original
Color Purple piano recording. SoulX-Singer renders explicit notes, English
phonemes and durations. The original piano excerpt is mixed back unchanged.
No sheet music or previous YuE2 score was imported.

## Listen

- [Piano + synthesized singing, 25 seconds](https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/012_yard_note_control/audio/mix.mp3)
- [Singing alone](https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/012_yard_note_control/audio/vocal.mp3)
- [Piano + deterministic note guide](https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/012_yard_note_control/audio/note-guide.mp3) — synthesized tones, not singing
- [Original piano excerpt](https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/012_yard_note_control/audio/piano.mp3)
- [Interactive piano-roll page](index.html) · [Editable score JSON](inputs/score.json) · [MIDI with lyrics](inputs/vocal.mid)

Only MP3 audio is retained and published for this trial. Temporary lossless arrays
are removed after evaluation and successful MP3 validation. Original user sources
and older experiment files are untouched.

## Design

The excerpt covers **1.70–26.70 seconds** of the original 3:30 recording. Eight
phrase anchors were chosen from its onset/CQT evidence. The vocal has 27 notes,
F3–D4, four short lyric lines and explicit phrase-end breathing spaces. Chord
labels are tentative harmonic interpretations of the audio: an F-centered pedal
with major/minor upper-voice changes. They are not a verified chord transcription.
The intermediate note onsets are composed subdivisions between anchors, not a
claim of measured beat-by-beat alignment.

```
Red brick walls hold the light
Old trees shade our dreams at night
Friends we found will walk with us
Here our love will live and last
```

English pronunciations come from CMUdict 1.1.1 (one-syllable `our` selected).
The compiled native SoulX metadata supplies word phonemes, MIDI pitches, note
classes and durations on a 20 ms grid. All words here are assigned one syllable
and one note. The syllable map is an actual model input in this experiment.
MIDI uses 120 BPM solely as a seconds-to-ticks carrier; the source's performed
phrase timing is represented by the event timestamps, not a fixed 120 BPM pulse.

## Singer and inference

[SoulX-Singer](https://github.com/Soul-AILab/SoulX-Singer) is used in **score** mode,
with automatic transposition disabled, pitch shift 0, 32 steps, CFG 3 and seed
20261007. A 9.02-second excerpt of experiment 011's synthetic ACE voice provides
timbre conditioning. Its approximate word times come from Whisper-base.en and
word pitches from pYIN; no real singer reference was imported. The reference
annotation is imperfect and may affect output quality.

The model receives this synthetic voice reference and the explicit vocal score.
It does not receive the piano waveform; the designed score carries the intended
musical relationship to the accompaniment. There is no vocal time warping after
synthesis. The native output is exactly 600,000 samples at 24 kHz, or 25 seconds.
It is resampled to 48 kHz to mix with the original stereo piano excerpt.

Model revision `40493ad90286056c7a9095035164434a79daa8c9`, code revision `81aeb3ae772c70093c3de74dc23c92d983801ae4`;
weight SHA256 `447eaf41f91a6b6659d55e9ec3c9b809221724fb8592aebaec35a23751a5b500`. Model and vocoder share the official 2.8 GB
checkpoint, retained in the model cache, never Git. The isolated runtime keeps
upstream Transformers 4.41.2 with existing Torch 2.10/CUDA 12.8 for Blackwell;
this differs from the upstream Torch 2.2/Python 3.10 setup and is recorded.
Inference including loading: 12.6 seconds; peak CUDA allocation
2.63 GiB. No candidate/seed search was performed.

## Measured results and limits

- pYIN estimated all **27/27** notes' median absolute pitch errors within 50 cents.
- Median absolute error over 1705 voiced inner-note frames: **9.2 cents**;
  95.1% of these frames are within 50 cents.
- The estimator excludes 120 ms at note edges and can make voicing/octave errors.
  This is pitch evidence, not measured phoneme synchronization or a musical-fit score.
- One-pass ASR: "Red brick walls hold the light Oh, tree's shade, our dreams at night Friends we've found, we'll walk with us Here our love will live and last".
  It recovers the four lines with errors; it is not verified lyric ground truth.
- Mix = `piano + 0.386316061 × vocal`; overall gain 1.0.
  Piano timing and level are preserved. Pre-MP3 subtraction recovers the piano
  within 5.96e-08; MP3 adds lossy encoding.
- Mix peak 0.7795. Vocal-only preview gain 0.9230 prevents export clipping.
- Musical fit, phrasing and voice quality require listening. No auditory quality
  acceptance or successful piano alignment is claimed from these measurements.

## Inspect or reproduce

[Target metadata](inputs/target-metadata.json), [prompt provenance](record/prompt-provenance.json),
[pitch measurements](record/pitch-check.json), [ASR diagnostic](record/lyric-check.json),
[run request](record/request.json), [generation record](record/generation.json).

The scripts in `record/` prepare audio evidence, reference voice and score, run
inference, evaluate pitch/lyrics and build the page. Use the installed
`/tmp/maestro-soulx-env/bin/python` for score preparation and synthesis; the
existing YuE2 Python environment for Whisper diagnostics. The 25-second piano
and synthetic voice source files from prior experiments must remain available.
`prepare_prompt.py` recreates the temporary reference array;
`generate.py` refuses an existing mix; use a new experiment directory for reruns.
Regenerate before evaluating pitch, because the temporary generated array is
removed after the completed experiment's validation. The score JSON/MIDI and
native target metadata are the editable, persistent representation.

| Syllable | Note | Start in excerpt (s) | Duration (s) |
|---|---|---:|---:|
| Red | A3 | 0.22 | 0.74 |
| brick | C4 | 0.96 | 0.74 |
| walls | A3 | 1.70 | 1.44 |
| hold | G3 | 3.18 | 0.70 |
| the | B♭3 | 3.88 | 0.70 |
| light | D4 | 4.58 | 1.24 |
| Old | F3 | 5.96 | 0.76 |
| trees | B♭3 | 6.72 | 0.78 |
| shade | D4 | 7.50 | 1.48 |
| our | C♯4 | 9.02 | 0.68 |
| dreams | C4 | 9.70 | 0.68 |
| at | B♭3 | 10.38 | 0.68 |
| night | F3 | 11.06 | 1.22 |
| Friends | A3 | 12.42 | 0.68 |
| we | C4 | 13.10 | 0.66 |
| found | A3 | 13.76 | 1.28 |
| will | G3 | 15.08 | 0.52 |
| walk | B♭3 | 15.60 | 0.52 |
| with | C4 | 16.12 | 0.52 |
| us | D4 | 16.64 | 0.90 |
| Here | F3 | 17.68 | 0.76 |
| our | B♭3 | 18.44 | 0.74 |
| love | D4 | 19.18 | 1.48 |
| will | C♯4 | 20.70 | 0.80 |
| live | C4 | 21.50 | 0.80 |
| and | B♭3 | 22.30 | 0.80 |
| last | F3 | 23.10 | 1.46 |
