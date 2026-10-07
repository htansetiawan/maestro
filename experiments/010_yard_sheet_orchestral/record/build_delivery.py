"""Render an honest queued or completed listening page from existing artifacts."""
from pathlib import Path
import html
import json
ROOT = Path(__file__).resolve().parents[1]
request = json.loads((ROOT/'inputs/request.json').read_text())
measurement = ROOT/'outputs/sheet-orchestral/measurement.json'
base = 'outputs/sheet-orchestral/'
if measurement.exists():
    m = json.loads(measurement.read_text())
    seconds = round(m['audio_seconds'])
    duration = f'{seconds//60}:{seconds%60:02d}'
    state = 'Generated; token limit reached' if any(m['truncated'].values()) else 'Generated without token-limit truncation'
    status = f'{state}. Duration **{duration}**. Audio and lyric fidelity await listening.'
    audio = f'<audio controls preload="metadata" src="{base}audio.mp3"></audio><p><a href="{base}audio.mp3">Download MP3</a> · <a href="{base}audio.flac">Lossless FLAC</a></p>'
    metrics = '\n\nRun measurements:\n\n```json\n'+json.dumps(m,indent=2)+'\n```\n'
else:
    status = 'Queued for GPU memory. Audio has not been generated yet.'
    audio = '<p>Waiting for GPU memory. The player will appear after generation and publication.</p>'
    metrics = ''
notes = '''The supplied five-page *Theme from The Color Purple* PDF is represented by
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
'''
readme = f'''# 010 — The Yard, conditioned on the sheet music

**{status}**

[Listening page](index.html) · [Actual lyrics](inputs/lyrics.txt) ·
[Actual conditioning score](inputs/vocal.abc) · [Request](inputs/request.json)

{notes}
## Exact prompt

{request['style']}

## Provenance and verification

[Provenance](inputs/provenance.json) · [Symbolic inspection](record/score-inspection.json) ·
[Prior independent score review](../008_color_purple_two_vocal_versions/record/score-review.json) ·
[Original transcription limitations](../007_color_purple_sheet_yue2/README.md)

The original source PDF SHA256 is
`4fff8e8f669eeaede7506398a22203d4353b14a2ddd5ba9db0b1e752df08fbbc`.
A matching local PDF was verified during preparation. The copy supplied to the
model is `inputs/vocal.abc`; its saved output must match byte for byte.

YuE2 runtime 0.1.6, the same pinned model and listening VAE as 009, `cot=full`,
seed {request['seed']}, semantic ceiling 15,000 tokens, default synthesis settings,
24 GiB memory budget, AR offload, 1,024-frame tiled decoding. Full effective
configuration and weight hashes are saved with the output. Native token arrays
and latents stay local and ignored; audio and readable manifests are published.
File integrity, score-input equality and non-silent audio do not prove audible
score adherence, lyric accuracy or musical quality.
{metrics}
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
'''
(ROOT/'README.md').write_text(readme)
e=html.escape
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Yard — sheet-conditioned orchestral version</title>
<style>body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:780px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(30px,6vw,44px);line-height:1.2}}audio{{width:100%}}a{{color:inherit}}pre{{white-space:pre-wrap;font:inherit}}details{{border-top:1px solid #ddd;padding-top:20px;margin-top:32px}}</style></head><body><main>
<small>MAESTRO · EXPERIMENT 010</small><h1>The Yard<br>Sheet-conditioned orchestral version</h1>
<p>{e(status.replace('**',''))}</p>{audio}
<p>New singing and orchestral accompaniment conditioned on the supplied melody and chords. No audio recording used.</p>
<p><a href="inputs/vocal.abc">Conditioning score</a> · <a href="README.md">Experiment details</a></p>
<h2>Lyrics</h2><pre>{e(request['lyrics'])}</pre>
<details><summary>Exact prompt</summary><p>{e(request['style'])}</p></details>
</main></body></html>''')
print(status)
