"""Publish clear version labels, full audio, exact conditions and limitations."""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
request=json.loads((ROOT/'inputs/request.json').read_text())
a=json.loads((ROOT/'outputs/new-piano-vocal-extended/measurement.json').read_text())
b=json.loads((ROOT/'outputs/existing-piano-vocal/mix.json').read_text())
alignment=json.loads((ROOT/'outputs/existing-piano-vocal/alignment.json').read_text())

def player(title,description,path):
    return f'<article><h2>{html.escape(title)}</h2><p>{html.escape(description)}</p><audio controls preload="metadata" src="{path}.mp3"></audio><p><a href="{path}.mp3">Download MP3</a> · <a href="{path}.flac">Lossless FLAC</a></p></article>'

body=player('A · New piano and singing · 6:12',
    'YuE2 generates the singer and piano together from the adapted sheet score and Harvard Yard lyrics. This is a new performance.',
    'outputs/new-piano-vocal-extended/audio')
body+=player('B · Existing piano with added singing · 5:39',
    'The original experiment 007 piano stays fixed. Singing isolated from A is adjusted in time and mixed over it. This is an experimental vocal overlay, not a native YuE2 inpainting task.',
    'outputs/existing-piano-vocal/audio')
body+=player('The aligned vocal alone · 5:39',
    'Listen for separation leakage, stretched vowels, and phrasing. This is the vocal stem used in B, before its mixing gain.',
    'outputs/existing-piano-vocal/vocals-aligned')
body+='''<details><summary>Original piano and initial capped take</summary><h3>Original piano · 5:39</h3>
<audio controls preload="metadata" src="../007_color_purple_sheet_yue2/outputs/sheet-piano-20261005/audio.mp3"></audio>
<h3>Initial vocal take · 6:00 · token limit reached</h3><audio controls preload="metadata" src="outputs/new-piano-vocal/audio.mp3"></audio>
<p>The initial capped take is retained. A uses the same request and seed with a larger token allowance and reaches a natural ending. It is a rerender, not a literal continuation of the initial waveform.</p></details>'''
body+='''<h2>What is established</h2><p>All 298 lead events retain their score timing and pitch classes. Of these, 178 are assigned to singing and 120 to instrumental passages. Sung phrases have documented octave shifts into A2–G4. The Harvard Yard lyrics are adapted to the available phrases.</p>
<p>A ends normally. B retains the original decoded piano waveform without time stretching or regeneration; its level is unchanged in this mix. Only the vocal is time-adjusted and scaled.</p>
<p>The alignment compares harmonic features, not phonemes. Local vocal duration ratios range from 0.456 to 1.823, so some passages undergo substantial timing changes. Separation can leave traces of A’s piano. Human listening is still needed to assess melody, lyric placement and naturalness. Automated transcription recognizes many requested lines but also produces extensive unexpected text; it does not confirm clean lyric delivery.</p>
<p><a href="inputs/vocal.abc">Actual vocal score</a> · <a href="inputs/lyrics.txt">Actual lyrics</a> · <a href="inputs/lyric-note-map.json">Intended syllable map</a> · <a href="inputs/edit_manifest.json">Score changes</a> · <a href="record/score-review.json">Independent score review</a> · <a href="outputs/existing-piano-vocal/alignment.json">Timing map</a> · <a href="outputs/existing-piano-vocal/mix.json">Piano preservation check</a> · <a href="README.md">Full protocol</a></p>'''
body+='<details><summary>Exact generation style</summary><pre>'+html.escape(request['style'])+'</pre></details>'
body+='<details><summary>Actual lyrics</summary><pre>'+html.escape(request['lyrics'])+'</pre></details>'
for name,title in [('new-piano-vocal','A'),('existing-piano-vocal','B')]:
    path=ROOT/'record'/('transcript-'+name+'.json')
    if path.exists():
        transcript=json.loads(path.read_text())['result']['text']
        body+=f'<details><summary>ASR diagnostic · {title}</summary><p>One Whisper-base.en pass; imperfect singing recognition, not ground truth or a timing metric.</p><pre>{html.escape(transcript)}</pre></details>'
(ROOT/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Yard Remembers — two vocal versions</title><style>
body{max-width:900px;margin:48px auto;padding:0 22px;font:16px/1.65 system-ui;color:#333;background:#fff}
h1{font-size:34px;line-height:1.2}h2{font-size:23px;line-height:1.3}a{color:#555}audio{width:100%}
article{border:1px solid #ddd;border-radius:10px;padding:20px;margin:24px 0}article h2{margin-top:0}
details{background:#f6f6f6;padding:16px;border-radius:8px;margin:16px 0}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere}
</style><p>Maestro · Experiment 008</p><h1>The Yard Remembers</h1><p>The same theme, two ways of adding singing. Created sequentially from the Color Purple sheet-music experiment.</p>'''+body+'</html>')
print('Built listening page with both requested versions and diagnostic stems.')
