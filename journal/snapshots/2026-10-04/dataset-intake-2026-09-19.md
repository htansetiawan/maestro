# September 19, 2026 — YouTube source intake tools

**Outcome:** `fetch`, `segment`, `sources`, `caption` and `pending` stages added to
`maestro-ace`, with unit tests for the segmenter, track splitting, the reference/train
roles, caption editing and the rights gate (13 tests pass). No model was trained and no
listening evaluation was run.

## What the tools do

- `fetch URL` downloads a YouTube video's audio as 48 kHz stereo WAV under the ignored
  `data/sources/youtube/<id>/` directory and writes a `source.json` sidecar: URL, title,
  uploader, upload date, platform-reported licence, downloader version, fetch time,
  chapters, and the audible span. `--keep-video` also stores an mp4.
- `segment ID` trims silence, cuts fixed or per-chapter windows inside the configured
  10–180 s range, drops mostly silent windows, and writes manifest rows with
  `role = "reference"`, `rights = "unverified"`, source offsets and a `TODO` caption.
  `--tracks` splits a compilation at quiet gaps so each song is its own composition.
- `caption ID --text ...` fills in a row; `pending` lists rows still marked `TODO`.
- `prepare` now stages reference rows separately (`reference.json`) and keeps them out
  of the train/validation split. A `train` row with unverified rights is refused unless
  `allow_unverified_rights = true` is set in the frozen config.

## First source

The first fetched source was a fan-uploaded compilation titled "David Foster Greatest
Hits Full Album - Best Duets Male and Female Songs" (video `q-73jqLVu3Y`, 50 min 42 s,
no chapters, no licence stated). Both the Opus and the AAC audio streams are digital
silence from about 19 minutes onward, which is consistent with a partial rights mute
on the platform. Track splitting found five songs in the audible part (boundaries near
221, 474, 681 and 884 s; 3.3–4.3 min each) and produced 15 clips of 25–90 s as
`train` rows, one composition per song. The material is vocal duets with band and
orchestra, not solo piano.

## Decision recorded

Henry chose to use this material for the first ACE fine-tuning trial. The config now
sets `allow_unverified_rights = true`; the rows keep `rights = "unverified"` and their
full YouTube provenance, so the adapter's training data can be audited. Any adapter
trained on it is a private experiment; it is not to be published or shared without
clearing the rights to the underlying recordings. Captions were still `TODO` at the
time of writing, and `prepare` refuses to freeze the split until they are written.

## Not public

The downloaded audio, the clips, and any adapter trained on them stay on Henry's machine.

## Later the same day: local albums and the workbench

Two albums Henry owns (24 MP3s, 102 minutes; catalogue in
`~/git/datasets/maestro/david_foster_musics/CATALOG.md`) were imported with the new
`import` stage: 23 sources after one byte-identical duplicate was skipped, decoded to
48 kHz WAV, cut into 74 clips of 90 s as `train` rows, one composition per song. With the
YouTube clips the manifest holds 89 clips in 28 training compositions, all captions
still `TODO`. A web workbench (`maestro-ace web`) now serves the clips for listening and
captioning behind a token cookie; the hostname `maestro.enrica.ai` was created as a CNAME
to the existing tunnel. Tests: 15 pass.

## Whole-song units and auto-label (evening)

The 90-second windows were dropped in favour of one clip per song: `data.max_seconds`
went to 360, and the 23 album tracks plus the 5 YouTube tracks became 28 clips of 196 to
328 s in 28 compositions. Reason: complete pieces carry real intros, entrances and
endings, and one caption per song is a third of the labeling. An `autolabel` stage now
drafts caption, BPM, key and instruments from the audio (librosa tempo and
Krumhansl-Schmuckler key, z-scored MFCC/chroma/loudness segmentation with 12 s minimum
sections, CLAP zero-shot instrument tags on 10 s windows kept only when persistent).
Drafts stay `TODO:`-prefixed until a listener confirms them in the workbench, which now
shows the section and instrument timeline under the player. Tests: 19 pass.
