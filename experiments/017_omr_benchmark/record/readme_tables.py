"""Print the README tables from outputs/comparison.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rep = json.loads((ROOT / 'outputs/comparison.json').read_text())
NAMES = dict(homr='homr 0.7', oemer='oemer 0.1.8', audiveris='Audiveris 5.11')
pct = lambda x: '—' if x is None else f'{x*100:.0f}%'
for stem, r in rep.items():
    print(f'\n{stem}: {r["measures"]} measures; RH {r["truth_attacks"][0]} attacks / {r["truth_tones"][0]} notes; LH {r["truth_attacks"][1]} attacks / {r["truth_tones"][1]} notes\n')
    print('| Pages | Engine | Measures | RH attacks exact | RH notes incl. chord tones | RH longest run | RH durations right | LH attacks exact | LH notes incl. chord tones | LH precision |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for cond, c in r['conditions'].items():
        for e in ('homr', 'oemer', 'audiveris'):
            x = c.get(e, {})
            if x.get('status') == 'no output':
                print(f'| {cond} | {NAMES[e]} | no output | | | | | | | |'); continue
            rh, lh = x['right_hand'], x['left_hand']
            print(f'| {cond} | {NAMES[e]} | {x["measures_found"]} | {pct(rh["exact_recall"])} | {pct(rh["chord_tone_recall"])} | {rh["longest_exact_run"]} | {pct(rh["duration_agreement"])} | {pct(lh["exact_recall"])} | {pct(lh["chord_tone_recall"])} | {pct(lh["precision"])} |')
