# 004 — Foster LoRA and a 30-second piano seed

This local pilot tests whether an ACE-Step adapter trained on the existing David
Foster corpus changes two outputs: a vocal stem conditioned on the entire supplied
piano recording, and a full arrangement continued from only its first 30 seconds.

## Listening comparisons

| Task | Original XL-base | Foster adapter, scale 1.0 |
|---|---|---|
| Singing over the full recording | [Baseline mix](../003_color_purple_yard_vocals/audio/the-yard-remembers-mix.mp3) | [Adapted mix](audio/lego-foster/mix.mp3) |
| Vocal stem alone | [Baseline singing](../003_color_purple_yard_vocals/audio/vocals.mp3) | [Adapted singing](audio/lego-foster/vocals.mp3) |
| 30-second seed, then piano + orchestra + vocals | [Base continuation](audio/continuation-base/continuation.mp3) | [Adapted continuation](audio/continuation-foster/continuation.mp3) |

Both tasks use the original [The Yard Remembers lyrics](../003_color_purple_yard_vocals/lyrics.txt).
Generated MP3 and WAV files are included in this repository. Training data,
checkpoints, and runtime logs are gitignored. The final adapter is hosted in the
private Hugging Face repository
[henryatharvard/maestro-acestep-foster-lora](https://huggingface.co/henryatharvard/maestro-acestep-foster-lora);
access requires an authorized Hugging Face account. See the [model card](MODEL_CARD.md).
All three new renders completed on October 5, 2026;
each has a `status: complete` runtime record.

The [verification script](record/check.py) passed: all 512 adapter tensors are
finite, all 256 LoRA B matrices are nonzero, LEGO settings match the baseline,
continuation settings match each other, and both continuation float WAVs preserve
the first 30 seconds exactly. The adapted LEGO mix reconstructs exactly from the
source plus its vocal stem. Outputs differ between the original and adapted models;
these checks establish a functioning experiment, not a perceptual improvement.

| Render | Duration | Runtime including initialization | Peak Torch allocation |
|---|---:|---:|---:|
| Adapted LEGO vocal and mix | 210.35 s | 145.3 s | 12.08 GiB |
| Base continuation | 210.00 s | 97.9 s | 12.04 GiB |
| Adapted continuation | 210.00 s | 149.2 s | 12.08 GiB |

User listening feedback on October 5, 2026: both temporal continuations sounded
poor, and LEGO-Foster sounded generally similar to the unfine-tuned experiment 003.
The user also reported that a previous Suno result provided a much more convincing
singer-over-piano performance. That is a subjective comparison, not a controlled
cross-system benchmark. This pilot demonstrated training fit but did not establish
useful style transfer or improved vocal alignment. Machine-readable technical
checks are in `record/checks.json`; they do not override this listening result.

## Training design

Completed locally on October 5, 2026: **400 optimizer steps**, 264 seconds including
model loading and the initial diagnostic, and 9.65 GiB peak Torch allocation.
The adapter contains 20,971,520 trained parameters. Fixed-noise mean training loss
on eight clips fell from **2.2111 to 0.7931** (64.1%); all eight improved. Average
epoch loss fell from 1.6129 to 0.8371. These are training-fit measurements, not
held-out quality, style-recognition, or vocal-alignment scores.

- Model: `acestep-v15-xl-base`, ACE checkout `ca1e85fe9430179831e6bc6be790c332190a3866`.
- Data: 40 excerpts, each 30 seconds, from 20 local recordings already imported
  into experiment 001. Excerpts start at 30 and 120 seconds of each imported WAV.
- Exclude the Color Purple evaluation composition, two alternate encodes, and the
  five YouTube compilation segments. Sources and offsets are recorded in
  `data/dataset.json`; original audio remains untouched.
- Caption: “Music from a David Foster recording.” No unverified BPM, key,
  instrumentation, or draft captions are promoted to ground truth.
- Lyrics are unknown and encoded as an empty string. `is_instrumental: false`
  prevents a default instrumental label; it does not assert every clip has vocals.
- Decoder attention LoRA: rank 16, alpha 32, dropout 0, self and cross attention
  Q/K/V/O projections. The original model weights remain frozen.
- Corrected upstream flow-matching trainer, continuous timestep sampling, CFG
  dropout 0.15, AdamW at 1e-4, cosine schedule, 20 warmup steps, gradient clipping 1.
- Ten epochs × 40 clips, batch size 1, accumulation 1: **400 optimizer steps**.
- bf16, gradient checkpointing, auxiliary encoder offload, GPU allocation cap 34%.
- Adapter checkpoints at epochs 5 and 10, plus a final inference adapter.

The fixed-noise diagnostic compares eight training clips before and after training
with identical random seeds and CFG dropout disabled. A lower loss shows improved
fit on those clips. It does not demonstrate generalization or better musicality.

This is full-recording style training, without paired accompaniment/vocal stems,
verified lyric timestamps, or note targets. The LEGO render deliberately tests
transfer to a task that was not directly trained. Stronger style and tighter vocal
alignment are separate outcomes, and vocal intelligibility may regress.

## Rendering controls

The adapted LEGO render copies all generation parameters from experiment 003:
same entire source recording, lyrics, caption, seed `20261005`, 50 diffusion steps,
guidance 7, and no LM planning. Only the adapter changes. Its stem is mixed with the
original accompaniment using the same RMS balancing method. Mix gains can differ.

The continuation supplies exactly 30 seconds of the decoded source followed by
180 seconds of zeros. It uses `repaint` with an explicit generation interval
`[30, 210]`, a full-arrangement caption, and the same seed for the base and adapted
runs. No part of the original recording after 30 seconds is passed to the model.
The resulting music after 30 seconds is newly generated, not the remainder of the
original composition. Piano, orchestra, and singing are requested through the
caption; successful instrumentation still needs listening verification.

For a precise preservation guarantee, the original first 30 seconds are restored
sample-for-sample in the float WAV export. MP3 is lossy. The splice is a hard cut
at 30 seconds with latent boundary blending inside ACE; check the transition by ear.
Original and adapted continuations use identical splice behavior.

## Reproduce

Run from the repository root with the installed environment and GPU access:

```bash
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/prepare.py
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/train.py preprocess
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/train.py train
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/render.py lego --adapter
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/render.py continuation
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/render.py continuation --adapter
/tmp/maestro-ace-step/.venv/bin/python experiments/004_foster_lora_continuation/record/check.py
```

Preparation and rendering refuse to overwrite existing takes. Use a separate
experiment directory for another run. Runtime evidence is in `record/training.json`,
`record/metrics.jsonl`, and `record/{lego-foster,continuation-base,continuation-foster}.json`.
