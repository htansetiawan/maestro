"""Listening page: the She vocal line read by three engines, the manual reference, and the YuE2 render."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
recall = json.loads((ROOT / 'outputs/vocal-recall.json').read_text()) if (ROOT / 'outputs/vocal-recall.json').exists() else None
adh = {r['id']: r for r in json.loads((ROOT / 'record/vocal-adherence.json').read_text())} if (ROOT / 'record/vocal-adherence.json').exists() else {}
trans = json.loads((ROOT / 'inputs/vocal-transcription.json').read_text())
NAMES = dict(homr='homr 0.7', oemer='oemer 0.1.8', audiveris='Audiveris 5.11')


def pct(x):
    return f'{x*100:.0f}%'


rows = ''
if recall:
    for e, r in recall['engines'].items():
        a = r['first_part']
        rows += f'<tr><td>{NAMES[e]}</td><td>{a["engine_notes"]}</td><td>{pct(a["recall_any_octave"])}</td><td>{pct(a["exact_recall"])}</td><td>{pct(a["precision"])}</td><td>{a["longest_exact_run"]}</td></tr>'

cards = ''
for out in sorted((ROOT / 'outputs').glob('*/audio.mp3')):
    rid = out.parent.name
    m = json.loads((out.parent / 'measurement.json').read_text())
    r = adh.get(rid)
    stats = ''
    if r:
        tempo = f'{r["tempo_ratio"]:.2f}×' if r.get('tempo_ratio') else 'n/a'
        stats = (f'<div class="stats"><span><b>{pct(r["melody_recall"])}</b> of written notes sung in order</span><span>{pct(r["exact_recall"])} in the written octave</span>'
                 f'<span>longest exact run {r["longest_exact_run"]}</span><span>{r["sung_notes"]} sung notes vs {r["written_notes"]} written</span><span>tempo {tempo}</span></div>')
    trunc = ' · stopped by the 4,500-token cap' if any(m['truncated'].values()) else ' · ended on its own'
    cards += (f'<div class="player"><h2>YuE2: piano and singer from the transcribed line</h2><p class="muted">{m["audio_seconds"]:.0f} s{trunc} · {m["seconds"]:.0f} s to render</p>'
              f'<audio controls preload="metadata" src="outputs/{rid}/audio.mp3"></audio><a href="outputs/{rid}/audio.mp3" download>Download MP3</a>{stats}</div>')
    if (out.parent / 'vocals.mp3').exists():
        cards += (f'<div class="player"><h2>The separated voice (Demucs)</h2><p class="muted">What the pitch tracker heard; separation artefacts included.</p>'
                  f'<audio controls preload="metadata" src="outputs/{rid}/vocals.mp3"></audio></div>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>She — sheet to voice</title><style>
body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}h1{{font-size:clamp(30px,5vw,44px);line-height:1.2}}small,.muted{{color:#777}}a{{color:inherit}}audio{{width:100%}}.players{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.player{{background:#f7f7f5;padding:16px;border-radius:8px}}.player h2{{font-size:18px;margin:0 0 8px}}section{{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}}.stats{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}.stats span{{background:#eceee9;padding:6px 10px;border-radius:5px;font-size:14px}}table{{border-collapse:collapse;width:100%;font-size:15px}}td,th{{text-align:left;padding:8px;border-bottom:1px solid #eee}}pre{{white-space:pre-wrap;font:13px/1.4 ui-monospace,monospace;background:#f7f7f5;padding:10px;border-radius:6px}}@media(max-width:650px){{.players{{grid-template-columns:1fr}}}}
</style><link rel="stylesheet" href="../../assets/listening.css"><script defer src="../../assets/listening.js"></script></head><body><main>
<nav class="listening-nav" aria-label="Listening experiments"><a class="journal-link" href="../../journal/">← Journal</a><div><a href="../013_score_reading_fidelity/">013 · Reading the printed score</a><a href="../014_yue2_excerpt_ablation/">014 · What YuE2 keeps of a score</a><a href="../016_she_sheet_to_voice/" aria-current="page">016 · She: sheet to voice</a></div></nav>
<small>MAESTRO · EXPERIMENT 016</small><h1>From a scanned song sheet<br>to a singer.</h1>
<p><em>She</em> (Aznavour and Kretzmer), a three-page piano-vocal score. Three OMR engines read the vocal staff; a manual transcription of the same staff ({len([1 for b in trans["bars"] for t in b["notes"].split() if not t.startswith("r:")])} printed notes, 33 bars, both lyric lines) is the reference. The transcribed line, its chord symbols and the printed lyrics then go to YuE2 as a complete lead sheet, and the singer's pitch is tracked back against the line it was given. The same tracker recovers 71% of the synthesized guide (repeated pitches merge into one segment), so 71% is the ceiling of this measurement, not 100%.</p>
<div class="players"><div class="player"><h2>Reference: the vocal line as transcribed</h2><p class="muted">Deterministic synth of the linearized song (intro, two verses, bridge, third verse, coda). Not a model output.</p><audio controls preload="metadata" src="inputs/melody-guide.mp3"></audio><a href="inputs/melody.mid">MIDI</a> · <a href="inputs/vocal-transcription.json">Transcription</a></div>{cards}</div>
<section><h2>How much of the vocal line each engine read</h2>
<table><tr><th>Engine</th><th>Notes in its first part</th><th>Melody recall</th><th>Exact octave</th><th>Precision</th><th>Longest exact run</th></tr>{rows}</table>
<p>Global pitch alignment of the engine's first-part note sequence against the transcribed vocal line. All three engines misread the opening bars of each verse in the same way, collapsing the descending sequence (E5, C5, A4) onto its middle bar; the bridge and coda were read almost perfectly by homr. No engine returned the chord symbols or the lyrics; those were typed from the sheet.</p></section>
<section><h2>The lead sheet YuE2 received</h2><details><summary>ABC (Vocal voice with chord symbols; Ins voice rests)</summary><pre>{escape((ROOT / "prepared/score.abc").read_text())}</pre></details><p class="muted">The lyrics were typed from the sheet and tagged by section ([Verse] ×2, [Bridge], [Verse], [Outro]); they stay out of the public record because they are in copyright.</p>
<p><a href="README.md">Full experiment record</a> · <a href="outputs/vocal-recall.json">OMR grading</a> · <a href="record/vocal-adherence.json">Vocal adherence</a></p></section>
</main></body></html>'''
(ROOT / 'index.html').write_text(page)
print('wrote', ROOT / 'index.html')
