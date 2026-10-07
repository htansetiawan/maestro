# 010 — The Yard, conditioned on the sheet music

**Generated without token-limit truncation. Duration **6:11**. Audio and lyric fidelity await listening.**

[Listening page](index.html) · [Actual lyrics](inputs/lyrics.txt) ·
[Actual conditioning score](inputs/vocal.abc) · [Request](inputs/request.json)

The supplied five-page *Theme from The Color Purple* PDF is represented by
experiment 007's manual upper-melody/chord reduction and experiment 008's reviewed
vocal adaptation. Its 298 lead events preserve rhythm and pitch class; 178 are sung
with phrase-wise octave shifts into A2–G4, and 120 remain instrumental. The key is
F major, tempo 88 BPM, with 87 measures plus pickup and a late 3/4 change.

The written left-hand accompaniment, lower chord tones, dynamics and pedal are
not encoded note for note. Tuplets/graces use the previously documented timing
reduction. This tests melody/chord conditioning, not full piano-score reproduction.
The model receives ABC notation, not the PDF itself. No piano recording or other
audio is an input. The accompaniment and voice are synthesized together.

The score and score-adapted Yard lyrics are unchanged from experiment 008; all
reviewed input hashes were rechecked. The orchestral style and seed come from 009,
with tempo, key and phrasing instructions adjusted to the supplied score. The
lyrics therefore differ from 009's longer original song. This is not a controlled
one-variable comparison. Experiment 008 version A also used this score, but
requested only piano and voice; version B subsequently mixed vocals over an
existing recording. This run performs no separation, time stretching or mixing.

## Exact prompt

English, cinematic orchestral pop ballad, warm expressive male baritone lead vocal, clear intimate storytelling in the verses, soaring lyrical chorus following the supplied Vocal melody, nostalgic and hopeful, serene autumn atmosphere, acoustic grand piano, lush legato strings, warm acoustic bass, gentle restrained drums, subtle French horn swells in the final chorus, spacious polished studio production, F major, 88 BPM, follow the supplied meter changes, instrumental introduction, gradual emotional build, tender resolved ending Follow the supplied melody and chord progression. Sing the Vocal part; piano and orchestra play the Ins passages and accompaniment. Natural legato phrasing and clear diction, with breathing between phrases.

## Provenance and verification

[Provenance](inputs/provenance.json) · [Symbolic inspection](record/score-inspection.json) ·
[Prior independent score review](../008_color_purple_two_vocal_versions/record/score-review.json) ·
[Original transcription limitations](../007_color_purple_sheet_yue2/README.md)

The original source PDF SHA256 is
`4fff8e8f669eeaede7506398a22203d4353b14a2ddd5ba9db0b1e752df08fbbc`.
A matching local PDF was verified during preparation. The copy supplied to the
model is `inputs/vocal.abc`; its saved output must match byte for byte.

YuE2 runtime 0.1.6, the same pinned model and listening VAE as 009, `cot=full`,
seed 20261007, semantic ceiling 15,000 tokens, default synthesis settings,
24 GiB memory budget, AR offload, 1,024-frame tiled decoding. Full effective
configuration and weight hashes are saved with the output. Native token arrays
and latents stay local and ignored; audio and readable manifests are published.
File integrity, score-input equality and non-silent audio do not prove audible
score adherence, lyric accuracy or musical quality.


Run measurements:

```json
{
  "elapsed_seconds": 128.24141481192783,
  "audio_seconds": 370.75866666666667,
  "peak": 0.693731427192688,
  "rms": 0.07388661422849878,
  "clipped_fraction": 0.0,
  "truncated": {
    "abc": false,
    "semantic": false
  },
  "manifest_verified": true,
  "external_score_supplied": true,
  "saved_score_matches_input": true,
  "peak_cuda_gib": 8.890914916992188,
  "auditory_quality_evaluated": false,
  "lyric_accuracy_evaluated": false
}
```

## Queue and reproduction

The user service `maestro-yue2-sheet-orchestral-010` checks GPU 0 every 30 seconds
and starts after two checks show at least 24 GiB free. It never stops other jobs.
It runs one generation, builds the listening page and attempts an ordinary push
of this experiment only. It refuses a changed request, duplicate output, a branch
other than main, or an unexpected origin. It does not force-push or retry a failed
inference. Local live status: `record/queue-status.json`; logs: `record/*.log`.
The transient service survives the chat turn, but not a system reboot.

```sh
systemctl --user status maestro-yue2-sheet-orchestral-010
# Cancel a waiting run:
systemctl --user stop maestro-yue2-sheet-orchestral-010
# Manual generation into a fresh folder:
/tmp/maestro-yue2/.venv/bin/python experiments/010_yard_sheet_orchestral/record/generate.py --output-name another-run
```
