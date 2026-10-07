# Experiment 008 — two ways to add a voice

The user requested both workflows sequentially: a newly generated YuE2 piano-and-vocal
performance, then singing layered over the existing experiment 007 piano recording.

## Listen

| Version | Audio | What happened |
|---|---|---|
| A — new piano and singing, 6:12 | [MP3](outputs/new-piano-vocal-extended/audio.mp3) · [FLAC](outputs/new-piano-vocal-extended/audio.flac) | YuE2 regenerated piano and singing together from a vocal adaptation of the sheet score and Harvard Yard lyrics. |
| B — original piano plus singing, 5:39 | [MP3](outputs/existing-piano-vocal/audio.mp3) · [FLAC](outputs/existing-piano-vocal/audio.flac) | The vocal isolated from A was adjusted in time and mixed over the unchanged decoded piano from experiment 007. |
| B's isolated, aligned vocal | [MP3](outputs/existing-piano-vocal/vocals-aligned.mp3) · [FLAC](outputs/existing-piano-vocal/vocals-aligned.flac) | Diagnostic stem, before its mixing gain; useful for hearing separation and timing artifacts. |

[Listening page](index.html) · [Actual lyrics](inputs/lyrics.txt) · [Actual score](inputs/vocal.abc)

Neither version uses ACE-Step. B reuses A's generated singer; it is not a second,
independently sampled singer and does not use a native YuE2 waveform-inpainting API.

## Score and lyrics

The source is experiment 007's manual melody/chord reduction of the supplied
five-page sheet. Its limitations and possible transcription errors remain.
All 298 merged lead events retain onset, duration and pitch class. The original
87 measures plus pickup, F-major key, 88 BPM, meter changes and harmonic boundaries
are retained. 178 events move to `Vocal`; 120 remain in `Ins` for piano passages.
Each sung phrase gets a consistent documented octave shift into A2–G4. Absolute
pitches therefore change; this is a baritone adaptation, not an exact-register copy.

The original Harvard Yard lyrics are shortened and adapted to the available
phrases. [The edit manifest](inputs/edit_manifest.json) records wording and octave
changes. [The syllable map](inputs/lyric-note-map.json) covers every intended vocal
note. This is a design sidecar, not a hard alignment input or measured transcript.
YuE2 receives only its supported style, lyrics, ABC, cot and seed request fields.

A separate [score review](record/score-review.json) checked the raw before/after
notation and request, then reconciled the change record. Three awkward syllable
placements were revised before generation. Remaining musical cautions include
range extremes and a long continuous passage whose breathing is left to performance.

## Version A — generation

YuE2 runtime 0.1.6, pinned source/model/decoder revisions inherited from experiments
006–007. Full score/harmony conditioning, seed 20261006, one warm male baritone and
solo grand piano. Default 32 midpoint synthesis steps, no quantization, 24 GiB
memory budget, AR offload and 1024-frame tiled VAE decoding. The actual request,
configuration, hashes and runtime measurements accompany each native output.

The first take hit the default 9000 semantic-token limit at 6:00. It is retained
in [new-piano-vocal](outputs/new-piano-vocal/), including its audio and truncation
record. The same request and seed were rerendered with a 15000-token allowance;
the second take reached a natural ending at 372.16 seconds, without truncation.
That is the delivered A. No seed search or quality-based candidate selection occurred.

The initial semantic prefix differs between these two runs despite the shared seed
and request; [the token comparison](record/token-continuation-check.json) records
this. The second take is a rerender with a larger allowance, not an exact continuation.
The native audio and manifests are retained unchanged. The first capped take has
a small fraction of full-scale samples; delivered A has none.

## Version B — isolate, align, mix

After YuE2 completed, [HTDemucs](https://github.com/facebookresearch/demucs) separated
the generated mixture into a vocal estimate and accompaniment. Demucs 4.0.1,
official `htdemucs` checkpoint, one shift, seed 20261006, overlap 0.25. Its weight
hash and source hash are in [separation.json](outputs/separated/separation.json).
Weights stay in the local cache, outside git.

The accompaniment and the existing piano were compared using CENS chroma and
global dynamic time warping with constrained steps. Both timelines were first
normalized by duration; a monotonic source-to-target timing map was sampled every
1.5 seconds. [Alignment evidence](outputs/existing-piano-vocal/alignment.json)
includes the complete map and harmonic-feature diagnostics.

[Rubber Band](https://breakfastquay.com/rubberband/) R3, via its offline key-frame
API, applied this time map to the vocal only, with pitch scale 1.0. A synthetic
timing/pitch check is in [stretch-check.json](record/stretch-check.json). No padding
or trimming was required to reach the target length. The vocal's local duration
ratios range from 0.456 to 1.823; substantial local timing changes can sound unnatural.

The base is the exact published experiment 007 `audio.mp3`, decoded by ffmpeg to
48 kHz stereo. It was not regenerated, shifted in time, stretched or filtered.
The mix uses `piano + 0.5701696 × aligned_vocal`; overall gain is 1.0. Subtracting
the added vocal from the lossless mixed output recovers the decoded piano with
maximum error 8.94e-8 (PCM/float rounding). Its 16,281,536 samples and 339.20-second
duration are unchanged. The [mix record](outputs/existing-piano-vocal/mix.json)
contains all gains, hashes and verification results. MP3 previews add ordinary
lossy encoding; use FLAC to inspect the mixing arithmetic.

## What these checks establish

Both requested outputs exist, are finite/non-silent, and have playable MP3 and
lossless FLAC versions. A preserves the supplied score in its saved input and ends
normally. B preserves the underlying decoded piano and aligns a vocal estimate
using harmonic features. The mean feature similarity improves from 0.837 to 0.902;
this is an algorithm diagnostic, not a perceptual alignment score.

Separation may retain piano leakage, DTW can mismatch repeated passages, and
time stretching can damage vocal naturalness. No phoneme-to-note alignment is
enforced. No human listening claim or Suno-quality claim is made. Whisper-base.en
transcripts, when present in `record/transcript-*.json`, are one-pass lyric
diagnostics and can omit or hallucinate sung words.

The A transcript recognizes many adapted lyric lines, including the red-brick
walls, books on the grass, friendship and returning-to-the-Yard passages. It also
contains extensive unexpected/repeated text. This diagnostic does not confirm
clean delivery of every lyric or establish that those unexpected words were
actually sung; the audio needs a listening review.

## Reproduction

Scripts in `record/` reproduce preparation, generation, separation, alignment,
mixing and the listening page. Generation/separation refuse existing output
directories. Preserve attempts and choose a fresh output directory for a rerun.

```bash
python experiments/008_color_purple_two_vocal_versions/record/prepare_vocal.py
HF_HUB_OFFLINE=1 OMP_NUM_THREADS=4 /tmp/maestro-yue2/.venv/bin/python experiments/008_color_purple_two_vocal_versions/record/generate.py --output-name new-piano-vocal-extended --max-tokens 15000
TORCH_HOME=/tmp/maestro-demucs-cache OMP_NUM_THREADS=4 /tmp/maestro-vocal-tools/bin/python experiments/008_color_purple_two_vocal_versions/record/separate_vocals.py
OPENBLAS_NUM_THREADS=4 /tmp/maestro-vocal-tools/bin/python experiments/008_color_purple_two_vocal_versions/record/align_and_mix.py
python experiments/008_color_purple_two_vocal_versions/record/build_listening.py
```

The isolated vocal-tools environment shares the existing Torch runtime and adds
Demucs, librosa and small dependencies; it does not modify the YuE2 environment.
Native token and latent arrays remain local and ignored; full native manifest
verification requires those arrays. Original generated audio is never replaced by
its separated or mixed derivatives.
