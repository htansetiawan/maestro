"""Grade each OMR engine's reading against the manual vocal transcription.

Two views per engine: all notes the engine put in its first part (what a naive
"take the top staff" pipeline would use), and the subset in the vocal register
(A3 and above) as a generous filter for piano-staff leakage. Recall is the share
of the 195 printed vocal notes found in order by global pitch alignment.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / 'experiments/014_yue2_excerpt_ablation/record'))
from measure import align, longest_run

NOTE = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)


def midi(name):
    letter, acc, octave = name[0], name[1:-1], int(name[-1])
    return 12 * (octave + 1) + NOTE[letter] + {'': 0, '#': 1, 'b': -1}[acc]


def manual():
    d = json.loads((ROOT / 'inputs/vocal-transcription.json').read_text())
    seq = []
    for b in d['bars']:
        for tok in b['notes'].split():
            p, dur, *_ = tok.split(':')
            if p != 'r':
                seq.append(midi(p))
    return seq


def grade(ref, cand):
    pairs = align(ref, cand)
    exact = [(i, j) for i, j in pairs if ref[i] == cand[j]]
    octave = [(i, j) for i, j in pairs if ref[i] != cand[j] and (ref[i] - cand[j]) % 12 == 0]
    return dict(engine_notes=len(cand), exact=len(exact), octave_only=len(octave),
                recall_any_octave=(len(exact) + len(octave)) / len(ref), exact_recall=len(exact) / len(ref),
                precision=(len(exact) + len(octave)) / max(1, len(cand)),
                longest_exact_run=longest_run(sorted(i for i, _ in exact)))


def main():
    ref = manual()
    report = dict(manual_notes=len(ref), engines={})
    for engine in ('audiveris', 'homr', 'oemer'):
        p = ROOT / 'outputs' / engine / 'vocal.json'
        if not p.exists():
            continue
        notes = json.loads(p.read_text())['notes']
        allp = [n['pitch'] for n in notes]
        treble = [n['pitch'] for n in notes if n['pitch'] >= 57]
        report['engines'][engine] = dict(first_part=grade(ref, allp), vocal_register=grade(ref, treble))
        a, t = report['engines'][engine]['first_part'], report['engines'][engine]['vocal_register']
        print(f"{engine:10s} first-part notes {a['engine_notes']:4d}: recall {a['recall_any_octave']:.2f} exact {a['exact_recall']:.2f} run {a['longest_exact_run']:3d} | "
              f"register-filtered {t['engine_notes']:4d}: recall {t['recall_any_octave']:.2f} exact {t['exact_recall']:.2f} run {t['longest_exact_run']}")
    (ROOT / 'outputs/vocal-recall.json').write_text(json.dumps(report, indent=1) + '\n')


if __name__ == '__main__':
    main()
