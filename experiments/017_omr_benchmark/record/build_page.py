"""Results page for the OMR benchmark with exact ground truth."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rep = json.loads((ROOT / 'outputs/comparison.json').read_text())
NAMES = dict(homr='homr 0.7', oemer='oemer 0.1.8', audiveris='Audiveris 5.11')
TITLES = {'k545-1': 'Mozart, Sonata in C K. 545, first movement (73 bars, KernScores encoding)',
          'ode-to-joy': 'Beethoven, Ode to Joy theme, easy two-hand arrangement (16 bars, encoded here)'}


def pct(x):
    return '—' if x is None else f'{x*100:.0f}%'


sections = ''
for stem, r in rep.items():
    rows = ''
    for cond in ('clean', 'degraded', 'harsh'):
        if cond not in r['conditions']:
            continue
        for e in ('homr', 'oemer', 'audiveris'):
            x = r['conditions'][cond].get(e, {})
            if x.get('status') == 'no output' or not x:
                rows += f'<tr><td>{cond}</td><td>{NAMES[e]}</td><td colspan=8>no output</td></tr>'
                continue
            rh, lh = x['right_hand'], x['left_hand']
            rows += (f'<tr><td>{cond}</td><td>{NAMES[e]}</td><td>{x["measures_found"]} / {r["measures"]}</td>'
                     f'<td>{pct(rh["exact_recall"])}</td><td>{pct(rh["chord_tone_recall"])}</td><td>{rh["longest_exact_run"]}</td>'
                     f'<td>{pct(lh["exact_recall"])}</td><td>{pct(lh["chord_tone_recall"])}</td><td>{lh["longest_exact_run"]}</td><td>{pct(rh["duration_agreement"])}</td></tr>')
    sections += f'''<section><h2>{escape(TITLES[stem])}</h2><p class="muted">Ground truth: {r["truth_attacks"][0]} right-hand attacks ({r["truth_tones"][0]} notes), {r["truth_attacks"][1]} left-hand attacks ({r["truth_tones"][1]} notes).</p>
<table><tr><th>Pages</th><th>Engine</th><th>Measures</th><th>RH attacks exact</th><th>RH notes incl. chord tones</th><th>RH longest run</th><th>LH attacks exact</th><th>LH notes incl. chord tones</th><th>LH longest run</th><th>Durations right (RH)</th></tr>{rows}</table></section>'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OMR against exact ground truth</title><style>
body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}h1{{font-size:clamp(30px,5vw,44px);line-height:1.2}}small,.muted{{color:#777}}a{{color:inherit}}section{{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}}table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{text-align:left;padding:7px;border-bottom:1px solid #eee;vertical-align:top}}.pages{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}}.pages img{{width:100%;border:1px solid #e6e5e2;border-radius:6px}}@media(max-width:650px){{.pages{{grid-template-columns:1fr}}}}
</style><link rel="stylesheet" href="../../assets/listening.css"></head><body><main>
<nav class="listening-nav" aria-label="Experiments"><a class="journal-link" href="../../journal/">← Journal</a><div><a href="../013_score_reading_fidelity/">013 · Reading the printed score</a><a href="../016_she_sheet_to_voice/">016 · She: sheet to voice</a><a href="../017_omr_benchmark/" aria-current="page">017 · OMR against ground truth</a></div></nav>
<small>MAESTRO · EXPERIMENT 017</small><h1>How much of a page<br>does OMR give back?</h1>
<p>Two public-domain pieces with exact encodings were rendered to pages by Verovio, clean, lightly degraded to imitate a photocopy (slight skew, blur, hard threshold), and heavily degraded to imitate a phone photograph (half resolution, 1.5° skew, uneven lighting, blur, noise, JPEG), and read back by three open OMR engines. Because the page was produced from the encoding, every note on both staves has a known answer. Recall is measured by aligning each staff's attack sequence to the truth; "notes incl. chord tones" counts every pitch in the truth, not just the top of each attack.</p>
<div class="pages"><figure><img src="preview/ode-to-joy-clean.png" alt="Ode to Joy, clean rendering"><figcaption class="muted">Clean page</figcaption></figure><figure><img src="preview/ode-to-joy-degraded.png" alt="Ode to Joy, degraded rendering"><figcaption class="muted">Degraded page (0.5° skew, blur, hard threshold)</figcaption></figure><figure><img src="preview/ode-to-joy-harsh.png" alt="Ode to Joy, phone photograph imitation"><figcaption class="muted">Phone-photo page (150 dpi, 1.5° skew, uneven light, blur, noise, JPEG q40)</figcaption></figure></div>
{sections}
<p><a href="README.md">Full experiment record</a> · <a href="outputs/comparison.json">All numbers</a> · <a href="source/ode-to-joy.musicxml">Ode to Joy encoding</a></p>
</main></body></html>'''
(ROOT / 'index.html').write_text(page)
print('wrote', ROOT / 'index.html')
