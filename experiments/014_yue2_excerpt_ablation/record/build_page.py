"""Build the listening page for the excerpt ablation from the saved records."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'record'
manifest = json.loads((ROOT / 'prepared/manifest.json').read_text())
events = json.loads((ROOT / 'inputs/excerpt-events.json').read_text())


def load(name):
    p = REC / name
    return {r['label']: r for r in json.loads(p.read_text())} if p.exists() else {}


first60 = load('adherence-outputs-first60.json')
full = load('adherence-outputs-full.json')
refs = {**load('adherence-references.json'), **load('adherence-full-score.json')}
asr = json.loads((REC / 'asr-diagnostic.json').read_text()) if (REC / 'asr-diagnostic.json').exists() else {}

TITLES = {
    'melody-only': 'Melody only, no chord symbols (cot=melody)',
    'melody-chords': 'Melody + chord symbols, the 007 recipe (cot=full)',
    'melody-chords-bass': 'Melody + chord symbols + bass line in the Vocal voice',
    'model-composed': 'No score: YuE2 composes from the same style prompt',
}


def pct(x):
    return f'{x*100:.0f}%'


def tempo(r):
    return f'{r["tempo_ratio"]:.2f}×' if r.get('tempo_ratio') else 'n/a'


def stat(rid):
    a, b = first60.get(rid + '-first60'), full.get(rid)
    if not a:
        return '<p class="muted">Adherence not measured.</p>'
    return (f'<div class="stats"><span><b>{pct(a["melody_recall"])}</b> melody recall in the first 60 s</span>'
            f'<span>{pct(a["exact_recall"])} in the written octave</span><span>{pct(a["skyline_precision"])} top-line precision</span>'
            f'<span>longest exact run {a["longest_exact_run"]}</span><span>tempo {tempo(a)}</span>'
            + (f'<span class="dim">whole clip: {pct(b["melody_recall"])} recall, run {b["longest_exact_run"]}</span>' if b else '') + '</div>')


cards = []
for rid in manifest['requests']:
    cond, seed = rid.rsplit('-', 1)
    out = ROOT / 'outputs' / rid
    m = json.loads((out / 'measurement.json').read_text()) if (out / 'measurement.json').exists() else None
    if m:
        trunc = ' · stopped by the 3,500-token cap' if any(m['truncated'].values()) else ' · ended on its own'
        body = (f'<p class="muted">{m["audio_seconds"]:.0f} s{trunc} · seed {seed} · {m["seconds"]:.0f} s to render</p>'
                f'<audio controls preload="metadata" src="outputs/{rid}/audio.mp3"></audio>'
                f'<a href="outputs/{rid}/audio.mp3" download>Download MP3</a>' + stat(rid))
        if (out / 'score.abc').exists():
            body += f'<details><summary>ABC the model received</summary><pre>{escape((out/"score.abc").read_text())}</pre></details>'
    elif (out / 'failure.json').exists():
        body = f'<p>Attempt failed; see <a href="outputs/{rid}/failure.json">failure.json</a>.</p>'
    else:
        body = '<p class="muted">Not generated.</p>'
    cards.append(f'<div class="player"><h2>{escape(TITLES[cond])}</h2>{body}</div>')

REF_TITLES = {'original-recording': 'Your recording, first 52 s, against bars 0–16',
              'original-recording-full': 'Your recording, all 3:30, against all 87 bars',
              'experiment-007-full': "Last week's 007 output (5:39) against all 87 bars"}
ref_rows = ''.join(f'<tr><td>{REF_TITLES[k]}</td><td>{pct(r["melody_recall"])}</td><td>{pct(r["exact_recall"])}</td><td>{pct(r["skyline_precision"])}</td><td>{r["longest_exact_run"]}</td><td>{tempo(r)}</td></tr>'
                   for k, r in refs.items() if k in REF_TITLES)
asr_rows = ''.join(f'<tr><td>{escape(TITLES[k.rsplit("-", 1)[0]])}</td><td><code>{escape(v["text"][:140])}</code></td></tr>' for k, v in asr.items())

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Color Purple — what YuE2 keeps of a score</title><style>
body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}h1{{font-size:clamp(30px,5vw,44px);line-height:1.2}}small,.muted{{color:#777}}a{{color:inherit}}audio{{width:100%}}.players{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.player{{background:#f7f7f5;padding:16px;border-radius:8px}}.player h2{{font-size:18px;margin:0 0 8px}}section{{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}}pre{{white-space:pre-wrap;font:13px/1.4 ui-monospace,monospace;background:#fff;padding:10px;border-radius:6px;overflow:auto}}.stats{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}.stats span{{background:#eceee9;padding:6px 10px;border-radius:5px;font-size:14px}}.stats .dim{{background:none;color:#777}}table{{border-collapse:collapse;width:100%;font-size:15px}}td,th{{text-align:left;padding:8px;border-bottom:1px solid #eee;vertical-align:top}}code{{font-size:13px}}@media(max-width:650px){{.players{{grid-template-columns:1fr}}}}
</style><link rel="stylesheet" href="../../assets/listening.css"><script defer src="../../assets/listening.js"></script></head><body><main>
<nav class="listening-nav" aria-label="Listening experiments"><a class="journal-link" href="../../journal/2026-10-17.html">← October 17 journal</a><div><a href="../013_score_reading_fidelity/">013 · Reading the printed score</a><a href="../014_yue2_excerpt_ablation/" aria-current="page">014 · What YuE2 keeps of a score</a><a href="../015_stable_audio_open/">015 · Stable Audio Open</a></div></nav>
<small>MAESTRO · EXPERIMENT 014</small><h1>Same 17 bars.<br>Four ways to tell YuE2 what to play.</h1>
<p>The pickup, intro and first theme of <em>Theme from The Color Purple</em> (measures 0–16, F major, 88 BPM, {events["nominal_seconds"]:.0f} s as written). YuE2's score interface accepts two single-line voices and quoted chord symbols, so the printed left hand and chord voicings can never be sent as notes. These runs vary only what the score carries; the style prompt (solo piano, no vocals) and the empty lyrics are shared. One seed per condition, two for the 007 recipe. Four of the five clips ran to the token cap instead of ending where the score ends.</p>
<div class="players"><div class="player"><h2>Reference: the melody as written</h2><p class="muted">Deterministic synth of the {len(events["melody"])} transcribed lead notes. Not a model output.</p><audio controls preload="metadata" src="inputs/melody-guide.mp3"></audio><a href="inputs/melody.mid">MIDI</a></div>
<div class="player"><h2>Reference: melody + chord-root bass</h2><p class="muted">The bass line sent in the fourth condition: one held note per chord symbol.</p><audio controls preload="metadata" src="inputs/melody-bass-guide.mp3"></audio><a href="inputs/melody-bass.mid">MIDI</a></div></div>
<section><h2>Generated piano</h2><div class="players">{''.join(cards)}</div></section>
<section><h2>How adherence is measured, and the ceiling</h2><p>Each clip is transcribed to notes with the ByteDance piano transcription model, the highest note at each attack is taken as the top line, and that sequence is aligned globally to the written melody. <strong>Melody recall</strong> is the share of written notes found in order (any octave); <strong>written octave</strong> requires the register on the page; <strong>top-line precision</strong> is the share of top-line attacks that belong to the melody, which is low even for a real pianist because accompaniment attacks also reach the top line; the <strong>longest exact run</strong> counts consecutive written notes reproduced in order and octave; <strong>tempo</strong> is the fitted time stretch of the matched notes relative to 88 BPM. The first 60 seconds of each clip is the fair window, since the written excerpt lasts 44 seconds and the clips run on.</p>
<table><tr><th>Reference audio</th><th>Melody recall</th><th>Written octave</th><th>Top-line precision</th><th>Longest run</th><th>Tempo</th></tr>{ref_rows}</table>
<p class="muted">The 007 row grades last week's full-score run with the same method: its 1.53× stretch matches the 5:39 output against a 3:49 score.</p></section>
<section><h2>Singing diagnostic</h2><p>Whisper (base.en) on each clip. On instrumental music Whisper hallucinates stock phrases such as "thank you for watching"; a long run of sung syllables is the signal. This is an automatic diagnostic, not a listening judgement.</p>
<table><tr><th>Condition</th><th>Whisper output, first 140 characters</th></tr>{asr_rows}</table></section>
<p><a href="README.md">Full experiment record</a> · <a href="record/adherence-outputs-first60.json">Measurements, first 60 s</a> · <a href="record/adherence-outputs-full.json">whole clips</a> · <a href="record/adherence-full-score.json">full-score references</a> · <a href="inputs/excerpt-events.json">Excerpt events</a> · <a href="prepared/manifest.json">Conditions</a></p>
</main></body></html>'''
(ROOT / 'index.html').write_text(page)
print('wrote', ROOT / 'index.html')
