# 001 — ACE audio personalization

Question: Does adapting ACE-Step 1.5 to Henry's original piano, violin, and duet
performances improve useful musical output over the unmodified model? Does offline
human or AI preference training add value beyond SFT?

This experiment follows AI Kitchen's scoped configs, separate checkpoints, held-out
evaluation, and matched conditions. It uses ACE's audio/flow model, so the text-model
`SFTTrainer` and `GRPOTrainer` from Gandalf are **not** reused. The feedback stage is
an **experimental offline flow-DPO surrogate**, not PPO, GRPO, or a proven ACE recipe.
Human ranking is the primary feedback signal; CLAP ranking only tests prompt/audio
match and is a weak RLAIF baseline. Do not infer “musical quality” from its score.

## Open the work

- **Run the experiment:** [CLI and training guide](https://github.com/henryatharvard/maestro/tree/main/experiments/001_ace_audio_personalization), [training loop](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/src/maestro_ace/train.py), [frozen config](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/configs/piano_violin.toml).
- **Inspect the evidence:** [public results index](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/results/README.md), [September 12 synthetic smoke record](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/results/smoke-2026-09-12.md), and [two informal ACE Music Playground baselines](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/results/ace-music-playground-2026-09-12.md).
- **Prepare recordings:** [manifest example](https://github.com/henryatharvard/maestro/blob/main/experiments/001_ace_audio_personalization/examples/recordings.jsonl) and the [recording intake guide](#recording-intake). No real piano audio is public yet.
- **Understand ACE:** [ACE-Step 1.5 paper](https://arxiv.org/abs/2602.00744), [official interactive demo](https://huggingface.co/spaces/ACE-Step/Ace-Step-v1.5), and [upstream source](https://github.com/ace-step/ACE-Step-1.5).

## Layout

```text
configs/piano_violin.toml       frozen experiment settings
data/audio/                     your original WAV/FLAC recordings (ignored)
data/recordings.jsonl           your annotated recording manifest (ignored)
prompts/feedback.jsonl          prompts used to make preference candidates
prompts/eval.jsonl              frozen, separate evaluation prompts
artifacts/prepared/             validated split, staged audio, hashes (ignored)
artifacts/tensors/              ACE preprocessed tensors (ignored)
artifacts/checkpoints/          SFT, human, AI adapter branches (ignored)
artifacts/generations/          seeded feedback and evaluation audio (ignored)
artifacts/preferences/          ballots, pairs, AI scores (ignored)
artifacts/reports/              matched-seed listening index (ignored)
```

## Recording intake

Record original music as lossless WAV or FLAC, ideally 48 kHz stereo for piano
and duet, mono or stereo for violin. Keep aligned piano, violin, and duet exports
under one `composition_id`; they must all be in the same train/validation split.
Start with distinct 60–120 second pieces. The code accepts 10–180 seconds as
configured, rejects near-silent or clipped files, hashes exact audio bytes, and
does not quantize or normalize your recordings. Keep MIDI separately if captured;
ACE LoRA consumes audio, not MIDI. Example rows are in
`examples/recordings.jsonl`. Captions describe what is audible, not an artist name.
Set `provenance` to document authorship and the right to train on each take.

Copy the example rows into `data/recordings.jsonl`, update paths/captions, and
put the matching files under `data/audio/`. The example is a schema, not a real
dataset. At least two distinct compositions are required for a held-out split;
20–30 is a sensible pilot before claiming any style improvement. Once prepared,
the inputs and split are frozen under this experiment ID; changes require a new ID.

## External sources: YouTube audio and video

Your own takes are the training set. Recordings of other artists are still useful:
as listening references beside your own generations, as analysis material, and as
audio conditions for ACE's cover/layer tasks. The `fetch` and `segment` stages bring
YouTube material into the same manifest format without deciding the rights question
for you.

```bash
uv sync --extra youtube                      # adds yt-dlp; ffmpeg must be on PATH
uv run --extra youtube maestro-ace fetch "https://www.youtube.com/watch?v=VIDEO_ID"
uv run --extra youtube maestro-ace fetch VIDEO_ID --keep-video       # also keep an mp4
uv run --extra youtube maestro-ace segment VIDEO_ID --clip-seconds 90 --instruments piano,strings
uv run --extra youtube maestro-ace segment VIDEO_ID --chapters       # one clip per chapter
uv run --extra youtube maestro-ace segment VIDEO_ID --tracks         # split a compilation at gaps
uv run --extra youtube maestro-ace segment VIDEO_ID --tracks --role train --merge
uv run --extra youtube maestro-ace sources                            # what has been fetched
uv run --extra youtube maestro-ace pending                            # clips still captioned TODO
uv run --extra youtube maestro-ace caption yt-VIDEO_ID-001 \
    --text "Pop ballad duet, male and female vocals, piano, strings, soft drums." \
    --bpm 72 --keyscale "Db major" --instruments vocals,piano,strings,drums
```

`fetch` writes `data/sources/youtube/<id>/audio.wav` (48 kHz stereo) and a `source.json`
sidecar with the URL, title, uploader, upload date, the licence YouTube reports, the
downloader version, the fetch time, chapters, and the audible span. Compilations are
sometimes muted part-way through by rights claims; `fetch` warns when a large part of the
file is digital silence and `segment` skips those windows.

`segment` trims leading and trailing silence, cuts fixed windows (default 90 s, with
optional overlap or per-chapter cuts), drops windows that are mostly silent, applies
20 ms fades at the cut points, and writes `clips/manifest.jsonl`. Every row carries
`source_url`, `source_id`, `source_start` and `source_end`, and inherits provenance.

By default all clips of a video share one `composition_id`, so a single performance never
straddles the train/validation split. For a compilation of several songs use `--tracks`:
the source is split where the level drops below `--gap-db` (default 35 dB under the peak)
for at least `--min-gap-seconds` (0.3 s), pieces shorter than `--min-track-seconds` (90 s)
are merged into their neighbour, and each track becomes its own composition
(`yt-<id>-t01`, `t02`, ...). Check the printed track boundaries against the video before
trusting them; crossfaded compilations do not split cleanly.

`caption` edits one manifest row in place (caption, BPM, key, time signature, instruments,
role), and `pending` lists the clips whose captions are still `TODO`, with their source
offsets so you can listen at the right place in the video.

Two fields govern how those rows are used, and both are enforced by `prepare`:

- `role`: `reference` (default) stages the clips under `artifacts/prepared/audio/` and
  lists them in `reference.json`, but keeps them out of the train and validation
  splits. `train` puts them in the split.
- `rights`: `unverified` for anything fetched from YouTube unless the platform reports a
  Creative Commons licence (`cc`). A `train` row with unverified rights is rejected until
  `allow_unverified_rights = true` is set in the frozen config. That opt-in is a recorded
  decision, not a default.

Captions of fetched clips start with `TODO`; a `train` row keeps failing validation until
the caption describes what is actually audible. Do not write the artist's name into the
caption: the model should learn from the sound, and the prompt vocabulary should stay
usable for your own material.

yt-dlp works better with a JavaScript runtime available (`deno` is its default); without
one it warns that some formats may be missing. Downloaded material stays in the ignored
`data/` tree and is never committed or uploaded by these commands.

## Local albums: `import`

Files you already own (MP3, FLAC, WAV, M4A) enter the same source tree:

```bash
uv run --extra youtube maestro-ace import ~/git/datasets/maestro/david_foster_musics \
    --segment --clip-seconds 90 --role train --instruments piano --merge
```

Each file is decoded once to 48 kHz stereo WAV under `data/sources/local/<slug>/` with a
sidecar carrying its tags (title, artist, album, year) and original path; byte-identical
duplicates are skipped. One file is one composition, so the split never puts two clips of
the same song on different sides. Rights are recorded as `unverified`, as for YouTube.

## Whole songs as the training unit

`data.max_seconds` is 360, and both `import --segment --clip-seconds 360` and
`segment --tracks --clip-seconds 360` produce one clip per song. Complete pieces carry
real intros, entrances and endings, which fixed 90-second windows cut through, and the
labeling shrinks to one caption per song. If the first GPU run shows that the longest
tracks do not fit in memory, cut those with `segment --clip-seconds 120` and re-caption
only them.

## Auto-label: `autolabel`

Drafts the caption, BPM, key, time signature and instrument list for every clip whose
caption is still `TODO`, from the audio alone:

```bash
uv sync --extra label            # librosa, transformers, torch
uv run --extra label maestro-ace autolabel                 # every TODO row
uv run --extra label maestro-ace autolabel --ids loc-01-jelinda-s-theme-001
uv run --extra label maestro-ace autolabel --no-clap       # tempo/key/structure only
```

Tempo comes from beat tracking with a ballad-leaning prior (double-time estimates are
halved and noted); key from Krumhansl-Schmuckler profiles over the mean chroma, with the
runner-up kept; sections from agglomerative segmentation of smoothed MFCC and chroma with
a loudness label each; instruments from zero-shot CLAP scores on a fixed vocabulary over
10-second windows, listed only when they persist across a quarter of the song. A
deterministic template turns that into the draft, so the same evidence always produces
the same words. The per-clip analysis lands in `data/analysis/<clip_id>.json` and the
workbench shows it as a timeline under the player.

Drafts are written as `TODO: <draft>` and keep failing the training gate until someone
listens, corrects and saves. Human captions are never overwritten unless `--force` is
given. Expect the drafts to be right about tempo range, loud and quiet sections and
whether there is singing, and to be wrong sometimes about which pad-like instrument is
playing; that is the part the listener fixes.

## Dataset workbench: `web`

A small web UI for the human part of the job: listen to each clip, write the caption, tap
the tempo, pick key, time signature and instruments, mark a clip as reference or remove
it, and run fetch / import / segment / prepare as background jobs with visible logs.

```bash
uv sync --extra web --extra youtube
MAESTRO_WEB_TOKEN=$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')
export MAESTRO_WEB_TOKEN
uv run --extra web --extra youtube maestro-ace web --host 127.0.0.1 --port 8090
# open http://127.0.0.1:8090/?token=$MAESTRO_WEB_TOKEN once; the browser keeps a cookie
```

The server binds to loopback. Every request must carry the token cookie; without the
environment variable it refuses non-loopback binds. Clips stream from `data/` on this
machine and never leave it except to the browser that holds the cookie.

**Public hostname.** `maestro.enrica.ai` is a CNAME to the `blacksmith` Cloudflare
Tunnel that already serves the other enrica.ai hostnames from this box. The tunnel's
ingress lives in `/etc/cloudflared/config.yml` (root); add, before the final
`http_status:404` rule:

```yaml
  - hostname: maestro.enrica.ai
    service: http://localhost:8090
```

then `sudo systemctl restart cloudflared`. `deploy/maestro-web.service` is a user unit
that keeps the workbench running across logins and reboots (user lingering is already on):

```bash
cp deploy/maestro-web.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now maestro-web.service
```

It reads the token from `~/.config/maestro/web.env` (`MAESTRO_WEB_TOKEN=...`, mode 600).
Consider also putting the hostname behind Cloudflare Access so the token is a second lock.

## Environment and checkpoints

Run from this directory. `uv` manages the experiment's own Python 3.12 environment.
The light environment supports intake without ACE or a GPU:

```bash
uv sync
uv run maestro-ace doctor
uv run maestro-ace prepare
```

To check that the entire pipeline is wired up before recordings or checkpoints
exist, run the synthetic CPU smoke test:

```bash
uv sync --extra smoke
uv run --extra smoke maestro-ace smoke
```

It creates a unique ignored `artifacts/smoke/run-*/` directory with synthetic
48 kHz audio, fake preprocessed tensors, a tiny trainable stand-in decoder,
one SFT step, human and AI preference branches, candidate files, and a
four-variant listening report. The AI smoke scorer uses audio energy, **not
CLAP**. The command prints the artifact path and fails on a broken stage.
This tests orchestration and real PyTorch loss/backprop/optimizer paths; it
does **not** load ACE weights, run ACE's preprocessor or generator, validate
adapter compatibility, or measure music quality.

On the Linux CUDA machine, install a **separate ACE checkout at the revision in
`configs/piano_violin.toml`**, and install it into this experiment environment:

```bash
git clone https://github.com/ace-step/ACE-Step-1.5.git /path/to/ACE-Step-1.5
git -C /path/to/ACE-Step-1.5 checkout ca1e85fe9430179831e6bc6be790c332190a3866
uv pip install -e /path/to/ACE-Step-1.5
ACE_ROOT=/path/to/ACE-Step-1.5
ACE_CKPT=/path/to/ACE-Step-1.5/checkpoints
```

ACE's package includes CUDA-specific PyTorch and model dependencies. Use ACE's
documented downloader to populate a checkpoint directory containing `vae/`,
`Qwen3-Embedding-0.6B/`, and the selected `acestep-v15-base/` DiT checkpoint.
After installation, download only the main bundle and base DiT:

```bash
.venv/bin/acestep-download --model main --dir "$ACE_CKPT"
.venv/bin/acestep-download --model acestep-v15-base --dir "$ACE_CKPT"
```

The pinned **base** model supports subsequent layer/extract/complete tasks for
Maestro Studio. To switch variants, edit the config and fetch the corresponding
checkpoint. The adapter belongs to the exact base variant and revision.

After `uv pip install -e`, call `.venv/bin/maestro-ace` directly so a fresh
`uv sync` does not remove the editable ACE install. Keep the path variables in
your shell for the commands below.

## Run the stages

```bash
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" preprocess
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" sft
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split feedback --model sft
```

SFT uses ACE's preprocessed tensors, DiT LoRA injection, continuous ACE timestep
sampling, flow-matching velocity loss and CFG dropout. It trains **exactly**
`sft.steps` optimizer steps, records metrics, saves interval/final adapters, and
compares seeded held-out flow loss before and after. Training never touches the
held-out composition's tensors.

For human feedback, listen to each two-seed pair in
`artifacts/generations/feedback/sft/`. Record a chosen and rejected ID, reviewer
and concrete reason in a private JSONL file like `examples/human_ballots.jsonl`.
The example ballot is illustrative; listen before using a real ballot.

```bash
.venv/bin/maestro-ace rank --source human --ballots /path/to/my-ballots.jsonl
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" preprocess-pairs --source human
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" preference --source human
```

For the separate AI-feedback branch, install the ML environment first and run
`.venv/bin/maestro-ace rank --source ai`. It uses a frozen CLAP model to compare candidates under the
same prompt; score margins below `judge.min_margin` are rejected. Then run
`preprocess-pairs --source ai` and `preference --source ai`. Both branches reload
the same SFT adapter and use a frozen copy of that adapter as reference.
No cross-branch continuation occurs.

For evaluation, generate the **same prompts and seeds** for the base model,
SFT adapter, and available feedback adapters, then build the listening index:

```bash
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split eval --model base
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split eval --model sft
.venv/bin/maestro-ace --ace-root "$ACE_ROOT" --checkpoints "$ACE_CKPT" generate --split eval --model human
.venv/bin/maestro-ace report
```

The report copies generated audio to anonymous take names and writes a separate
`artifacts/reports/answer_key.json`; keep the key closed until ratings are done.
Rate which take you would keep, phrasing, instrumentation, and artifacts.
A lower flow loss or higher CLAP score alone is not evidence of
better composition. Track copy/memorization concerns by comparing outputs with
the training recordings before sharing a model.

## Current verification boundary

The synthetic CPU smoke has run through every pipeline stage, including one
PyTorch optimizer step for SFT and for each preference branch. It passed in
September 2026. **No ACE weights, GPU training, CLAP inference, or listening
study has been run for this experiment yet.** Real model integration still
requires the pinned upstream checkout and checkpoint bundle on your RTX PRO
5000/C3 environment. The smoke command does not call a cloud API or upload
recordings.
