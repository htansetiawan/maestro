"""Listening page for the Stable Audio Open trials."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rec = ROOT / 'record'
status = json.loads((rec / 'status.json').read_text()) if (rec / 'status.json').exists() else dict(status='not started')
protocol = json.loads((rec / 'protocol.json').read_text()) if (rec / 'protocol.json').exists() else None
sim = {r['label']: r for r in json.loads((rec / 'similarity.json').read_text())} if (rec / 'similarity.json').exists() else {}
TITLES = {'t2a-piano-20261017': 'Text → audio: solo piano, seed A', 't2a-piano-20261018': 'Text → audio: solo piano, seed B',
          'a2a-piano-sigma0.5': 'Source piano → piano, σ = 0.5 (closest to the source)', 'a2a-piano-sigma2': 'Source piano → piano, σ = 2',
          'a2a-piano-sigma8': 'Source piano → piano, σ = 8 (mostly regenerated)',
          'a2a-orchestra-sigma2': 'Source piano → piano with orchestra, σ = 2', 'a2a-orchestra-sigma8': 'Source piano → piano with orchestra, σ = 8'}


def stats(r):
    if not r:
        return ''
    return (f'<div class="stats"><span>chroma similarity {r["chroma_similarity"]:.2f}</span><span>{r["source_topline_recall"]*100:.0f}% of source top line</span>'
            f'<span>{r["exact_recall"]*100:.0f}% exact octave</span><span>{r["topline_precision"]*100:.0f}% precision</span></div>')


cards = []
conds = protocol['conditions'] if protocol else []
for c in conds:
    out = ROOT / 'outputs' / c['id']
    if (out / 'audio.mp3').exists():
        m = json.loads((out / 'measurement.json').read_text())
        body = (f'<p class="muted">{m["audio_seconds"]:.1f} s · {m["seconds"]:.0f} s to generate · prompt: {escape(c["prompt"])}</p>'
                f'<audio controls preload="metadata" src="outputs/{c["id"]}/audio.mp3"></audio><a href="outputs/{c["id"]}/audio.mp3" download>Download MP3</a>' + stats(sim.get(c['id'])))
    elif (out / 'failure.json').exists():
        body = f'<p>Failed; see <a href="outputs/{c["id"]}/failure.json">failure.json</a>.</p>'
    else:
        body = '<p class="muted">Pending.</p>'
    cards.append(f'<div class="player"><h2>{escape(TITLES.get(c["id"], c["id"]))}</h2>{body}</div>')
if not conds:
    cards.append(f'<div class="player"><h2>Status: {escape(status["status"])}</h2><p>{escape(status.get("action", ""))}</p></div>')
ceiling = sim.get('source-mp3-ceiling')
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Color Purple — Stable Audio Open</title><style>
body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}h1{{font-size:clamp(30px,5vw,44px);line-height:1.2}}small,.muted{{color:#777}}a{{color:inherit}}audio{{width:100%}}.players{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.player{{background:#f7f7f5;padding:16px;border-radius:8px}}.player h2{{font-size:18px;margin:0 0 8px}}section{{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}}.stats{{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}}.stats span{{background:#eceee9;padding:6px 10px;border-radius:5px;font-size:14px}}@media(max-width:650px){{.players{{grid-template-columns:1fr}}}}
</style><link rel="stylesheet" href="../../assets/listening.css"><script defer src="../../assets/listening.js"></script></head><body><main>
<nav class="listening-nav" aria-label="Listening experiments"><a class="journal-link" href="../../journal/2026-10-17.html">← October 17 journal</a><div><a href="../013_score_reading_fidelity/">013 · Reading the printed score</a><a href="../014_yue2_excerpt_ablation/">014 · What YuE2 keeps of a score</a><a href="../015_stable_audio_open/" aria-current="page">015 · Stable Audio Open</a></div></nav>
<small>MAESTRO · EXPERIMENT 015</small><h1>Stable Audio Open<br>over the same piano.</h1>
<p>Stable Audio Open 1.0 is a text-to-audio latent diffusion model (47 s, 44.1 kHz stereo) with no score input. Two questions: what does it produce for the piano prompt used in the YuE2 trials, and how much of the original recording survives when the recording is used as the starting point (audio-to-audio at increasing noise levels), including the LEGO-style request to add an orchestra.</p>
<div class="players"><div class="player"><h2>Reference: the original piano, first 47 s</h2><audio controls preload="metadata" src="record/source-excerpt.mp3"></audio>{stats(ceiling) if ceiling else ''}<p class="muted">Measurement ceiling: the source against an MP3 of itself.</p></div></div>
<section><h2>Generated audio</h2><div class="players">{''.join(cards)}</div></section>
<section><h2>How survival is measured</h2><p><strong>Chroma similarity</strong> is the mean frame-wise cosine between the 12-bin pitch-class profiles of the source and the output (1.0 = identical harmony over time). The <strong>top-line</strong> numbers reuse experiment 014's method: both clips are transcribed to notes, the highest note at each attack is aligned, and recall says how many of the source's top-line notes reappear. These grade note content, not sound quality.</p>
<p><a href="README.md">Full experiment record</a> · <a href="record/protocol.json">Settings</a> · <a href="record/similarity.json">Measurements</a></p></section>
</main></body></html>'''
(ROOT / 'index.html').write_text(page)
print('wrote', ROOT / 'index.html')
