# 003 — The Yard Remembers

An ACE-Step LEGO vocal experiment using the supplied
`/tmp/theme_from_the_color_purple.mp3` as accompaniment, with original lyrics about
Harvard Yard: red brick buildings, trees, college friendships, and memories across
generations of students.

## Listen

- [Accompaniment and generated singing — MP3](audio/the-yard-remembers-mix.mp3)
- [Accompaniment and generated singing — 24-bit WAV](audio/the-yard-remembers-mix.wav)
- [Generated singing alone — MP3](audio/vocals.mp3)
- [Generated singing alone — float32 WAV](audio/vocals.wav)
- [Original lyrics: The Yard Remembers](lyrics.txt)

Generated MP3 and WAV outputs are included in the repository. Source data and
runtime records remain local and gitignored. The source MP3 is decoded to
48 kHz stereo. The decoded accompaniment is mixed directly with the
new vocal stem, with a constant overall gain for peak headroom. There is no time
stretching or regeneration of the accompaniment.

Completed locally on October 5, 2026: 210.35 seconds of audio, 67.4 seconds of
generation after initialization, and 12.04 GiB peak Torch allocation. Audio is
finite and non-silent; the mix peaks at 0.95 and reconstructs from the original
accompaniment plus the vocal stem to within float/PCM rounding. Whisper recognizes
the opening verse and chorus but becomes unreliable later. This is not evidence
that all lyrics were sung correctly; listening must establish phrasing and fit.

## Experiment settings

| Setting | Value |
|---|---|
| Model | `acestep-v15-xl-base` |
| ACE revision | `ca1e85fe9430179831e6bc6be790c332190a3866` |
| Task | `lego`: generate the `VOCALS` track from source audio |
| Voice prompt | Warm, expressive male tenor; clear English; restrained vibrato |
| Alignment prompt | Follow the source lead melody and phrase contours; leave breathing spaces |
| Seed | `20261005` |
| Diffusion steps | 50 |
| Guidance scale | 7.0 |
| LM planning and CoT | Disabled; source audio supplies the musical context |
| Fine-tuning / LoRA | None; this is an inference experiment |
| Runtime | CUDA, bf16, SDPA, CPU offload for auxiliary models |

The lyric structure contains an intro, two verses, two choruses, an instrumental
break, a bridge, and an outro. These section labels and the alignment caption are
soft instructions; they do not prescribe vocal notes or exact syllable timestamps.

## Evidence and reproduction

- [Generation script](record/generate_vocals.py)
- [Generation settings, hashes, timings, and mixing gains](record/generation.json)
- [Generation log](record/generation.log)
- [Audio validation and lyric-check script](record/check_output.py)
- [Audio checks](record/quality.json)
- [Local Whisper transcription](record/transcription.json)

Run from the Maestro repository using the existing ACE environment:

```bash
/tmp/maestro-ace-step/.venv/bin/python \
  experiments/003_color_purple_yard_vocals/record/generate_vocals.py
/tmp/maestro-ace-step/.venv/bin/python \
  experiments/003_color_purple_yard_vocals/record/check_output.py
```

The generation script refuses to replace an existing vocal take. For another
take, use a separate experiment directory and preserve this run's files.

The checks cover finite audio, duration, mixing arithmetic, peak headroom, and
recognizable lyrics. They do not establish melodic fit or good phrasing. Compare
the vocal-only and mixed files by ear, especially entrances, sustained notes,
phrase endings, and the placement of words against the accompaniment.
