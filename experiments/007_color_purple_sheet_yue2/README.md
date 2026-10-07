# Experiment 007 — printed score → YuE2 instrumental

**Status: completed; see the local listening page and outputs.**

The queued run finished on 2026-10-06 at 00:41 PDT. It produced 339.20 seconds
(5:39) of stereo audio, with neither ABC nor semantic generation truncated.
The saved input score matches the prepared ABC; artifact verification and audio
sanity checks passed. Audio-to-score adherence and musical quality remain unassessed.
Its duration is longer than the score's nominal 3:49; this alone does not identify
whether it slowed down, repeated passages, or added material.

The initial watcher incorrectly treated the truncation-flags dictionary as a
boolean, labeling the result truncated despite both flags being false. The watcher
and displayed status have been corrected; the original audio/result are unchanged.

The supplied five-page *Theme from The Color Purple* piano score has been manually
reduced to an upper melody plus printed chord symbols. This is the actual supplied
sheet, not experiment 006's short user-supplied motif.

The user authorized automatic generation when GPU memory becomes available.
The user service `maestro-yue2-sheet-007` polls `nvidia-smi` every 30 seconds and
starts once GPU 0 has at least 17 GiB free for two successive checks. It runs one
attempt, retains failures, and does not terminate other jobs. Runtime status is in
`record/gpu-wait-status.json`; generation output is logged to `record/generation.log`.
Check or cancel the queue with `systemctl --user status maestro-yue2-sheet-007`
or `systemctl --user stop maestro-yue2-sheet-007`. The transient service survives
this chat turn, but is not configured to resume after a machine reboot.

Open [the inspection page](index.html) to hear a deterministic melody guide and
seek to individual measures. That guide is synthesized directly from note events;
it is **not YuE2-generated music** or a piano performance of the entire arrangement.

## Prepared input

- [Editable transcription](inputs/transcription.tsv): all five pages, 87 numbered
  measures plus the pickup, with source page/system/bar and printed Intro/A–G labels.
- [Exact rational events](inputs/source-events.json) and [lead MIDI](inputs/melody-exact.mid).
- [Native ABC](prepared/score.abc), [native MIDI](inputs/melody-native.mid),
  [request](prepared/request.json), and [notation checks](prepared/score-check.json).
- [Reduction/timing report](prepared/repair-report.json) and
  [source provenance](inputs/source.json), including the source PDF hash.

F major; printed tempo approximately quarter = 88; 4/4 with a one-quarter pickup,
then 3/4 from measure 75. At constant tempo, 336 quarter beats take 229.09 seconds
(3:49). A performance with rubato need not match that duration or the earlier MP3.

The printed composition credits are Quincy Jones, Rod Temperton and Jeremy
Lubbock; piano arrangement by Shiori Aoyama. David Foster is the album association
on this sheet. The original PDF is retained locally in the ignored `source-private/`
directory. The Dropbox URL credentials and original PDF are not copied into git.

## What the reduction changes

YuE2 receives a monophonic `Ins` melody. `Vocal` contains rests and chord symbols;
lyrics are empty and the style requests solo grand piano. `cot=full` preserves
external melody plus harmony conditioning. The model does not read the PDF directly.

The lower right-hand chord tones and written left-hand arpeggios are not encoded
note for note. Accompaniment remains a generation task. This experiment therefore
tests following the lead line and harmonic progression, not exact reproduction of
the printed piano arrangement.

Triplets remain exact fractions in the source/MIDI, but native ABC rounds their
endpoints to a 1/32-quarter grid (maximum endpoint shift 7.11 ms). Grace groups in
measures 50, 82 and 86 receive an explicit editorial timing of 1/16 quarter per
grace, taken from the following note. The E7+5 label in measure 22 becomes E7;
the melody's C remains. Rolled chords, lower voices, dynamics, articulation and
pedaling are omitted. Final ritardando and fermata remain source annotations;
native timing uses constant 88 BPM. All reductions are recorded.

Each bar has been visually read and checked for duration; native events round-trip
through the compiler/parser without changing their pitches or quantized times.
**These checks do not independently prove the manual transcription correct.**
Human musical proofreading and comparison against the original recording remain
useful before attributing a future wrong note to YuE2.

## Rebuild and generate later

From the repository root, using the YuE2 runtime already installed for experiment 006:

```bash
python experiments/007_color_purple_sheet_yue2/record/prepare.py
/tmp/maestro-yue2/.venv/bin/python experiments/007_color_purple_sheet_yue2/record/preview.py
HF_HUB_OFFLINE=1 /tmp/maestro-yue2/.venv/bin/python experiments/007_color_purple_sheet_yue2/record/run.py
```

`prepare.py` expects the PDF in this experiment's ignored `source-private/` directory
for hashing; `--source-pdf` and `--skill-dir` override the default locations.
The final command validates hashes, the native tokenizer and context length on
CPU. It does not load the model or start GPU inference.

When generation is requested and at least 17 GiB of GPU memory is free:

```bash
HF_HUB_OFFLINE=1 OMP_NUM_THREADS=4 /tmp/maestro-yue2/.venv/bin/python experiments/007_color_purple_sheet_yue2/record/run.py --generate
```

One predeclared seed, 20261005; supplied ABC; solo piano; empty lyrics; full harmony
conditioning. Semantic limit 9000 tokens, default 32 midpoint steps, no quantization,
17 GiB memory budget, AR offload, tiled VAE decoding. A run preserves its request,
runtime/model revisions, failure or result, and full lossless audio plus MP3.
It refuses to overwrite an existing attempt or stop other GPU jobs.

The runner reuses the verified 0.1.6 runtime/checkpoint pins from experiment 006,
instead of the older 0.1.5 release recipe bundled with the instrumental skill.
CPU preparation does not establish that this longer inference fits GPU memory.
Native result arrays remain local; a complete result-manifest verification needs
those arrays as well as the published files.

After generation, assess melody pitch/order, note onsets, chord changes, transitions,
and instrumental purity against the score. File integrity and preserved ABC alone
do not establish audible score following.
