"""Build the delivery page from the completed audio-conditioned vocal take."""
from pathlib import Path
import html
import json
ROOT = Path(__file__).resolve().parents[1]
r = json.loads((ROOT/'inputs/request.json').read_text())
g = json.loads((ROOT/'record/generation.json').read_text())
q = json.loads((ROOT/'record/quality.json').read_text())
assert g['status'] == 'complete'
seconds = round(q['duration_seconds'])
duration = f'{seconds//60}:{seconds%60:02d}'
base = 'https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/011_yard_piano_fresh_ace_vocal/audio/'
(ROOT/'README.md').write_text(f'''# 011 — Original piano with a fresh ACE-Step vocal

The user selected a fresh ACE-Step LEGO take conditioned on the original
3:30 *Theme from The Color Purple* recording, after preferring experiment 009's
unconditioned YuE2 song to the sheet-conditioned versions.

- [Piano + new vocal — {duration}]({base}mix.mp3)
- [Isolated generated voice — {duration}]({base}vocals.mp3)
- [Mix FLAC](audio/mix.flac) · [Vocal FLAC](audio/vocals.flac)
- [Listening page](index.html) · [Exact lyrics](inputs/lyrics.txt)

## What this run does

ACE-Step `acestep-v15-xl-base` receives the original piano waveform through
`src_audio`, the LEGO instruction `Generate the VOCALS track based on the audio context:`,
a caption and the full lyrics from experiment 009. It generates a vocal stem,
which is then mixed with the decoded original recording. No sheet, MIDI, ABC,
YuE2-generated audio, LoRA or fine-tuning is used. This is a fresh stochastic take,
not evidence that the alignment limitations reported in earlier LEGO runs are fixed.

Compared with experiment 003: the same source, base checkpoint, 50 steps, guidance
7.0 and disabled LM/CoT; new lyrics, a revised baritone caption and seed 20261007.
Several inputs change, so this is not a controlled single-variable comparison.

## Actual result and preservation check

- Duration: {q['duration_seconds']:.6f} seconds; 48 kHz stereo.
- Original piano is neither regenerated nor time-stretched.
- Mix formula: `(decoded_piano + {q['vocal_gain']:.9f} * generated_vocal) * {q['piano_gain']:.9f}`.
- Maximum reconstruction error from the saved lossless mix: {q['mix_reconstruction_max_error']:.3g}.
- Recovering the decoded piano after undoing gains and subtracting the added vocal
  gives a maximum error of {q['recovered_piano_max_error']:.3g} (PCM/float rounding).
- Mix peak: {q['peak']:.6f}; full-scale/clipped samples: {q['clipped_samples']}.
- Vocal length adjustment for mixing: {q['vocal_padding_or_trimming_samples']} samples
  (positive means silence padded at the end; negative means trimmed at the end).
- Vocal-only delivery gain: {q['vocal_delivery_gain']:.9f}; native float32 output
  remains unchanged locally. MP3s are 256 kbps conversions of the delivered FLACs.
- Generation after initialization: {g['generation_seconds']:.1f} seconds;
  peak Torch allocation: {g['peak_torch_allocated_gib']:.2f} GiB.

These checks establish sample preservation and export integrity, not musical fit.
Lyric completeness, vocal isolation and alignment require listening. The generated
stem may contain accompaniment leakage; no cleanup or time warping is applied.
No ASR or perceptual quality score is claimed.

## Exact caption

{r['caption']}

## Records and reproduction

[Input request](inputs/request.json) · [Actual runtime settings and output hashes](record/generation.json) ·
[Mix checks](record/quality.json) · [Generator](record/generate.py)

ACE code revision `{g['ace_revision']}`. Existing local checkpoint cache; its
configuration SHA256 is `{g['model_config_sha256']}`.
Source filename `{r['source_filename']}`; SHA256 `{r['source_sha256']}`.
The public runtime record replaces local source paths and excludes private logs;
the full runtime record, decoded source and native float32 WAV stay local and ignored.
The model weights are not included in Git.

```sh
/tmp/maestro-ace-step/.venv/bin/python experiments/011_yard_piano_fresh_ace_vocal/record/generate.py
python3 experiments/011_yard_piano_fresh_ace_vocal/record/build_delivery.py
```

The generator refuses to overwrite an existing take; use a separate experiment
folder for another run. CUDA free-memory preflight requires 17 GiB, and the same
0.34 per-process memory fraction as experiment 003 is retained.
''')
e=html.escape
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>The Yard — original piano and fresh voice</title>
<style>body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:780px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(30px,6vw,44px);line-height:1.2}}audio{{width:100%}}a{{color:inherit}}pre{{white-space:pre-wrap;font:inherit}}section{{border-top:1px solid #ddd;margin-top:32px;padding-top:16px}}small{{color:#777}}</style></head>
<body><main><small>MAESTRO · EXPERIMENT 011</small><h1>The Yard<br>Original piano + fresh voice</h1>
<p>ACE-Step generated a new vocal from the original piano audio and the lyrics of the song you preferred. No sheet music supplied.</p>
<h2>Piano + voice · {duration}</h2><audio controls preload="metadata" src="audio/mix.mp3"></audio><p><a href="audio/mix.mp3">Download mix</a> · <a href="audio/mix.flac">Lossless mix</a></p>
<h2>Voice alone</h2><audio controls preload="metadata" src="audio/vocals.mp3"></audio><p><a href="audio/vocals.mp3">Download voice</a> · <a href="audio/vocals.flac">Lossless voice</a></p>
<p>The piano timing is preserved. Vocal alignment and lyric accuracy await listening.</p>
<section><h2>Lyrics</h2><pre>{e(r['lyrics'])}</pre></section><section><details><summary>Prompt and generation records</summary><p>{e(r['caption'])}</p><p><a href="README.md">Experiment notes</a> · <a href="record/quality.json">Mix checks</a> · <a href="record/generation.json">Settings and hashes</a></p></details></section>
</main></body></html>''')
print(json.dumps(dict(duration=duration,mix_peak=q['peak'],piano_gain=q['piano_gain'])))
