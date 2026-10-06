---
base_model: ACE-Step/acestep-v15-xl-base
library_name: peft
tags:
- music-generation
- acestep
- lora
- research
---

# Maestro: Foster style LoRA pilot

An experimental decoder-attention LoRA for **ACE-Step 1.5 XL-base**, trained in
Maestro experiment 004. This repository contains an adapter, not a standalone
music-generation model. Use it with `ACE-Step/acestep-v15-xl-base`.

## Contents

- `adapter_model.safetensors`: 20,971,520 adapter parameters, bf16.
- `adapter_config.json`: PEFT adapter configuration.
- `training_summary.json`: configuration, diagnostic results, and weight hash.

## Training

Trained October 5, 2026 using ACE-Step checkout
`ca1e85fe9430179831e6bc6be790c332190a3866` and XL-base checkpoint revision
`220c1166efbdd9583eafcb12eb160594bbfcb241`.

The local David Foster recording corpus supplied 40 excerpts from 20 recordings:
30 seconds each, 20 minutes total. Excerpts begin 30 and 120 seconds into imported
WAV files. The Color Purple evaluation composition, alternate encodes, and YouTube
compilation segments were excluded. Training recordings are not included here.

Each clip uses the caption “Music from a David Foster recording.” Lyrics are
unknown and use empty conditioning. Instrumentation, tempo, key, and lyric timing
were not verified or used as labels. The corpus includes vocal and instrumental
recordings. Its source manifest records training rights as unverified.

- LoRA rank 16, alpha 32, dropout 0; self/cross attention Q/K/V/O projections.
- Corrected upstream continuous-time flow-matching trainer; CFG dropout 0.15.
- AdamW, learning rate 1e-4, cosine schedule, 20 warmup steps, gradient clipping 1.
- Batch size 1, accumulation 1, ten epochs: 400 optimizer steps.
- Seed 20261005; bf16; gradient checkpointing; original model weights frozen.

## Evaluation and limitations

Fixed-noise mean training loss on eight clips decreased from **2.2111 to 0.7931**.
All eight clips improved. These are training-set diagnostics, not held-out
generalization or perceptual quality measurements.

Matched base/adapter inference experiments generated a vocal stem over the entire
Color Purple accompaniment, and a piano/orchestra/vocal continuation after a
30-second piano seed. Technical checks passed: finite weights, nonzero updates,
matched generation settings, correct durations, and preserved source prefixes.
Style resemblance, musical coherence, lyric accuracy, and vocal alignment have
not been established through a listening evaluation.

This adapter was trained on full mixes, without paired accompaniment/vocal stems,
note targets, or lyric timestamps. Improved training fit does not establish better
LEGO vocal alignment. Overfitting and regressions in singing are possible.

## Use

Initialize the pinned ACE-Step handler with `config_path="acestep-v15-xl-base"`,
download this repository with an authorized Hugging Face account, then load:

```python
status = handler.load_lora("/path/to/downloaded/maestro-acestep-foster-lora")
print(status)
print(handler.set_use_lora(True))
print(handler.set_lora_scale(1.0))
```

The matched experiment used 50 diffusion steps, guidance 7, seed 20261005, and
disabled LM planning. Load this adapter through the ACE-Step handler because PEFT
weights target its decoder submodule, not the entire condition-generation model.

Code, listening comparisons, and reproduction instructions:
[Maestro experiment 004](https://github.com/htansetiawan/maestro/tree/main/experiments/004_foster_lora_continuation).
