# 002 — Piano with an ACE vocal layer

First local ACE-Step GPU generation, recorded October 4, 2026: add a sung voice to
a supplied solo piano performance, with original lyrics about the Yard and its
red brick buildings.

## Listen

- [Piano and voice — MP3](audio/yard-piano-and-voice.mp3)
- [Piano and voice — 24-bit WAV](audio/yard-piano-and-voice.wav)
- [Generated vocal stem — float32 WAV](audio/vocals.wav)
- [Original lyrics](lyrics.txt)

The mix is 94.976 seconds, 48 kHz stereo. The requested voice is a warm, intimate
male tenor. The piano samples were extracted from the supplied
`st_elmo_fire.m4a` audio track and mixed directly with the generated vocal stem.
There was no time stretching or piano regeneration. The input file also contained
video; this experiment used its audio track only.

## Generation record

| Setting | Value |
|---|---|
| Model | `acestep-v15-xl-base` |
| Task | `lego` — generate the `VOCALS` track from source audio |
| Seed | `20261004` |
| Diffusion steps | 50 |
| Guidance scale | 7.0 |
| Language | English |
| LM planning and all CoT flags | Disabled |
| Precision | bf16; no quantization |
| GPU | NVIDIA RTX PRO 5000 Blackwell, 48 GB |
| Generation time after initialization | 15.30 seconds, including export and mixing |

The [settings record](record/generation.json) includes the complete prompt, input
hash, pinned code and model revisions, and mix gains. The
[generation log](record/generation.log) confirms that ACE skipped the LM and
processed the source audio. Disabling planning avoids the source-conditioning
problem reported in [upstream issue #1286](https://github.com/ace-step/ACE-Step-1.5/issues/1286).

The vocal stem was multiplied by `0.58892416759623` and added to the extracted
piano. Overall mix gain was `1.0`; the mix peak was approximately −1.10 dBFS.
ACE's raw vocal export is 94.96 seconds; 16 ms of silence was appended for mixing
to match the source length.

## Checks and limits

The generated audio is finite and non-silent, and the final mix has no clipped
peaks. A local Whisper `base.en` [transcription](record/transcription.json)
recognizes both verses and the chorus, including the red brick lines, with some
recognition errors and repetitions. This checks the presence of the lyrics; it
does not establish naturalness, melodic fit, or musical quality. The final outro
line is not present in the transcription. Listening remains necessary.

This is one generated take, not a model comparison or a personalization training
result. No SFT or preference training was performed. The exact files published
here are listed in [SHA256SUMS](SHA256SUMS).

## Reproduction evidence

[generate_vocals.py](record/generate_vocals.py) and
[check_lyrics.py](record/check_lyrics.py) are the scripts executed for this take.
They preserve the original local paths under `/tmp/maestro-yard-vocals` and
`/tmp/maestro-ace-step`; edit those paths when rerunning elsewhere. The original
input file and model weights must be supplied separately. The
[model revisions](record/model_revisions.json) and ACE code revision in the settings
record identify the exact downloads. ACE was installed in its own Python 3.12
environment with `uv sync`.

See the official [ACE inference guide](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md)
for the Lego task and [model guide](https://github.com/ace-step/ACE-Step-1.5)
for XL Base setup. This experiment is separate from
[001 — ACE audio personalization](../001_ace_audio_personalization/README.md).
