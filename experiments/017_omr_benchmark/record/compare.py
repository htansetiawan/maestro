"""Grade each engine's MusicXML against the exact ground truth, per staff, per condition.

Metrics per staff: measures found vs printed; note recall (any octave) and exact
recall from a global pitch alignment of attack sequences (chords contribute their
top note to the sequence, all notes to the counts); precision; longest exact run;
duration agreement among exactly matched notes; and, for the whole staff, the
share of ground-truth sounding notes (chord tones included) that the engine
reproduced with the same pitch set at the same position within a matched measure
grid when the measure counts agree.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import re
import sys

import music21 as m21

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / 'experiments/014_yue2_excerpt_ablation/record'))
from measure import align, longest_run
ENGINES = ('homr', 'oemer', 'audiveris')
PIECES = json.loads((ROOT / 'inputs-manifest.json').read_text())


def page_of(p):
    m = re.search(r'-(\d+)(?:\.mvt\d+)?\.(mxl|musicxml|xml)$', p.name)
    return int(m.group(1)) if m else 0


def read_engine(engine, cond, stem):
    d = ROOT / 'outputs' / cond / engine
    files = sorted((p for p in d.rglob('*') if p.suffix in ('.mxl', '.musicxml', '.xml') and p.name.startswith(stem)),
                   key=lambda p: (page_of(p), p.name))
    staves = [[], []]
    measures = 0
    for path in files:
        try:
            s = m21.converter.parse(str(path))
        except Exception:
            continue
        parts = list(s.parts) if len(s.parts) else [s]
        n_meas = max(len(p.getElementsByClass(m21.stream.Measure)) for p in parts)
        for pi, part in enumerate(parts[:2]):
            for mi, meas in enumerate(part.getElementsByClass(m21.stream.Measure)):
                for el in meas.recurse().notes:
                    if el.isRest or el.duration.isGrace or (el.tie and el.tie.type in ('stop', 'continue')):
                        continue
                    staves[pi].append(dict(measure=measures + mi, offset=str(F(el.getOffsetInHierarchy(meas)).limit_denominator(96)),
                                           duration=str(F(el.duration.quarterLength).limit_denominator(96)),
                                           pitches=sorted(p.midi for p in el.pitches)))
        measures += n_meas
    return staves, measures, len(files)


def grade(truth, got):
    tp = [max(n['pitches']) for n in truth]
    gp = [max(n['pitches']) for n in got]
    if not gp:
        return dict(engine_attacks=0, recall=0, exact_recall=0, precision=0, longest_exact_run=0, duration_agreement=None, chord_tone_recall=0)
    pairs = align(tp, gp)
    exact = [(i, j) for i, j in pairs if tp[i] == gp[j]]
    octv = [(i, j) for i, j in pairs if tp[i] != gp[j] and (tp[i] - gp[j]) % 12 == 0]
    dur_ok = sum(F(truth[i]['duration']) == F(got[j]['duration']) for i, j in exact)
    # chord tones: among exactly matched attacks, how many of the truth's pitches appear in the engine's stack
    truth_tones = sum(len(n['pitches']) for n in truth)
    found_tones = sum(len(set(truth[i]['pitches']) & set(got[j]['pitches'])) for i, j in exact)
    return dict(engine_attacks=len(gp), recall=(len(exact) + len(octv)) / len(tp), exact_recall=len(exact) / len(tp),
                precision=(len(exact) + len(octv)) / len(gp), longest_exact_run=longest_run(sorted(i for i, _ in exact)),
                duration_agreement=dur_ok / len(exact) if exact else None,
                chord_tone_recall=found_tones / truth_tones)


def main():
    report = {}
    for stem, info in PIECES.items():
        truth = json.loads((ROOT / 'source' / f'{stem}-truth.json').read_text())
        report[stem] = dict(measures=info['measures'], truth_attacks=[len(t) for t in truth],
                            truth_tones=[sum(len(n['pitches']) for n in t) for t in truth], conditions={})
        for cond in ('clean', 'degraded', 'harsh'):
            if not (ROOT / 'pages' / cond).exists():
                continue
            report[stem]['conditions'][cond] = {}
            for engine in ENGINES:
                staves, measures, nfiles = read_engine(engine, cond, stem)
                if not nfiles:
                    report[stem]['conditions'][cond][engine] = dict(status='no output')
                    continue
                entry = dict(files=nfiles, measures_found=measures,
                             right_hand=grade(truth[0], staves[0]), left_hand=grade(truth[1], staves[1]))
                report[stem]['conditions'][cond][engine] = entry
                rh, lh = entry['right_hand'], entry['left_hand']
                print(f"{stem:11s} {cond:8s} {engine:9s} measures {measures:3d}/{info['measures']}  RH recall {rh['recall']:.2f} exact {rh['exact_recall']:.2f} "
                      f"run {rh['longest_exact_run']:3d} tones {rh['chord_tone_recall']:.2f} | LH recall {lh['recall']:.2f} exact {lh['exact_recall']:.2f} tones {lh['chord_tone_recall']:.2f}")
    (ROOT / 'outputs/comparison.json').write_text(json.dumps(report, indent=1) + '\n')


if __name__ == '__main__':
    main()
