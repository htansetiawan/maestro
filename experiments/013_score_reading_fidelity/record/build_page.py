"""Inspection page: what three OMR engines read from the printed score versus the manual lead line."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rep = json.loads((ROOT / 'outputs/comparison.json').read_text())
NAMES = dict(audiveris='Audiveris 5.11 (rule-based, Java)', homr='homr 0.7 (vision transformer)', oemer='oemer 0.1.8 (U-Net + classifiers)')
LOSS = json.loads((ROOT / 'outputs/loss-ledger.json').read_text()) if (ROOT / 'outputs/loss-ledger.json').exists() else None


def pct(x):
    return f'{x*100:.0f}%' if isinstance(x, (int, float)) else '—'


rows, cards = [], []
for engine, e in rep['engines'].items():
    if e.get('status') != 'parsed':
        rows.append(f'<tr><td>{NAMES[engine]}</td><td colspan=6>{escape(e.get("status", "?"))}</td></tr>')
        continue
    L = e['ledger']
    rows.append(f'<tr><td>{NAMES[engine]}</td><td>{e["measures_total"]} / {rep["manual"]["measures"]}</td><td>{pct(e["melody_recall"])}</td><td>{pct(e["exact_recall"])}</td><td>{pct(e["skyline_precision"])}</td>'
                f'<td>{e["measures_exact"] if e["measures_exact"] is not None else "grid differs"}</td><td>{L["chord_symbols"]} / {rep["manual"]["chord_events"]}</td></tr>')
    guide = f'<audio controls preload="metadata" src="outputs/{engine}/two-hands.mp3"></audio><a href="outputs/{engine}/two-hands.mp3" download>Download MP3</a>' if (ROOT / 'outputs' / engine / 'two-hands.mp3').exists() else '<p class="muted">No playable rendering.</p>'
    cards.append(f'<div class="player"><h2>{escape(NAMES[engine])} — both staves as read</h2><p class="muted">{L["right_hand_sounding_notes"]} right-hand notes in {L["right_hand_attacks"]} attacks ({L["right_hand_chord_stacks"]} chord stacks) · {L["left_hand_sounding_notes"]} left-hand notes · {L["tuplet_events"]} tuplet events · {L["grace_notes"]} grace notes</p>{guide}</div>')

per_measure = ''
for engine, e in rep['engines'].items():
    if e.get('status') == 'parsed' and e.get('measures_exact') is not None:
        reading = json.loads((ROOT / 'outputs' / engine / 'reading.json').read_text())
        bad = [m for m in reading['per_measure'] if not m['match']]
        items = ''.join(f'<li>m.{m["measure"]}: written {" ".join(n for _, n in map(lambda x: (x, name(x[1])), m["manual"]))} · read {" ".join(name(p) for _, p in m["omr_top"]) or "nothing"}</li>' for m in bad[:40])
        per_measure += f'<details><summary>{escape(NAMES[engine])}: {len(bad)} measures where the top line differs</summary><ul>{items}</ul></details>'


def name(p):
    return ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B'][p % 12] + str(p // 12 - 1)


loss = ''
if LOSS:
    loss = f'''<section><h2>What the score holds, and what reaches YuE2</h2>
<table><tr><th>Layer of the printed arrangement</th><th>Notes (from {escape(LOSS["engine"])}'s reading)</th><th>Carried by YuE2's score input?</th></tr>
<tr><td>Lead melody (top of the right hand)</td><td>{LOSS["melody_notes"]}</td><td>Yes — the <code>Ins</code> voice, after rounding tuplets to a 1/32-quarter grid</td></tr>
<tr><td>Right-hand chord tones under the melody</td><td>{LOSS["rh_inner_notes"]}</td><td>No — only as a quoted chord symbol</td></tr>
<tr><td>Left hand (bass and arpeggios)</td><td>{LOSS["lh_notes"]}</td><td>No — only as the slash bass of a chord symbol</td></tr>
<tr><td>Chord symbols</td><td>{LOSS["chord_symbols"]}</td><td>Yes, when the quality is in the native vocabulary ({LOSS["unsupported_chords"]} are not)</td></tr>
<tr><td>Grace notes, tuplets, dynamics, pedal, ritardando, fermata</td><td>{LOSS["graces"]} graces · {LOSS["tuplets"]} tuplets</td><td>No (graces get editorial timing; the rest is dropped)</td></tr></table>
<p>{LOSS["carried_fraction"]*100:.0f}% of the sounding notes on the page can be expressed in the model's score input. Everything else is regenerated from the chord symbols and the style prompt.</p></section>'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Color Purple — reading the printed score</title><style>
body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}h1{{font-size:clamp(30px,5vw,44px);line-height:1.2}}small,.muted{{color:#777}}a{{color:inherit}}audio{{width:100%}}.players{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.player{{background:#f7f7f5;padding:16px;border-radius:8px}}.player h2{{font-size:18px;margin:0 0 8px}}section{{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}}table{{border-collapse:collapse;width:100%;font-size:15px}}td,th{{text-align:left;padding:8px;border-bottom:1px solid #eee;vertical-align:top}}details{{margin-top:12px}}li{{font-size:14px}}code{{font-size:14px}}@media(max-width:650px){{.players{{grid-template-columns:1fr}}}}
</style><link rel="stylesheet" href="../../assets/listening.css"><script defer src="../../assets/listening.js"></script></head><body><main>
<nav class="listening-nav" aria-label="Listening experiments"><a class="journal-link" href="../../journal/2026-10-17.html">← October 17 journal</a><div><a href="../013_score_reading_fidelity/" aria-current="page">013 · Reading the printed score</a><a href="../014_yue2_excerpt_ablation/">014 · What YuE2 keeps of a score</a><a href="../015_stable_audio_open/">015 · Stable Audio Open</a></div></nav>
<small>MAESTRO · EXPERIMENT 013</small><h1>Can software read the sheet<br>before a model plays it?</h1>
<p>Last week's score-conditioned YuE2 run started from a hand-made reduction of the five scanned pages of <em>Theme from The Color Purple</em>. This page checks the first link: three optical music recognition engines read the same scan, and their readings are compared with the manual lead line ({rep["manual"]["melody_notes"]} notes, {rep["manual"]["measures"]} measures, {rep["manual"]["chord_events"]} chord symbols). The scanned pages are copyrighted and stay offline.</p>
<div class="players"><div class="player"><h2>Reference: the manual lead line</h2><p class="muted">Experiment 007's melody guide, deterministic synth.</p><audio controls preload="metadata" src="../007_color_purple_sheet_yue2/inputs/melody-guide.mp3"></audio></div></div>
<section><h2>What each engine read</h2><div class="players">{''.join(cards)}</div></section>
<section><h2>Agreement with the manual lead line</h2>
<table><tr><th>Engine</th><th>Measures found</th><th>Melody recall</th><th>Exact octave</th><th>Top-line precision</th><th>Measures identical</th><th>Chord symbols read</th></tr>{''.join(rows)}</table>
<p>Recall and precision come from a global alignment of the engine's right-hand top line against the manual melody, so a missed or extra measure costs notes rather than breaking the comparison. "Measures identical" counts bars whose top-line onsets and pitches match exactly; it is only computed when the engine found the printed number of measures on every page.</p>{per_measure}</section>
{loss}
<p><a href="README.md">Full experiment record</a> · <a href="outputs/comparison.json">Comparison data</a></p>
</main></body></html>'''
(ROOT / 'index.html').write_text(page)
print('wrote', ROOT / 'index.html')
