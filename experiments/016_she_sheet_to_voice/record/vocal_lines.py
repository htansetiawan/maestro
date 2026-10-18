"""Extract the vocal staff (top part) from each OMR engine's MusicXML, compare the engines
pairwise, and write per-engine note lists.

Output: outputs/<engine>/vocal.json, outputs/vocal-agreement.json
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
from measure import align
ENGINES = dict(audiveris='audiveris', homr='homr', oemer='oemer')
EXPECTED_MEASURES = [10, 10, 11]      # printed bars per page: p1 = 2 intro + 8, p2 = 10, p3 = 11 incl. coda


def page_of(p):
    m = re.search(r'page-(\d)', p.name)
    return int(m.group(1)) if m else 0


def files(engine):
    d = ROOT / 'outputs' / ENGINES[engine]
    return sorted((p for p in d.rglob('*') if p.suffix in ('.mxl', '.musicxml', '.xml')), key=lambda p: (page_of(p), p.name))


def vocal_part(score):
    """The vocal line is the first part/staff of each system in this piano-vocal score."""
    parts = list(score.parts) if len(score.parts) else [score]
    return parts[0]


def notes_of(part):
    out = []
    for mi, meas in enumerate(part.getElementsByClass(m21.stream.Measure)):
        for el in meas.recurse().notes:
            if el.isRest or el.duration.isGrace:
                continue
            if el.tie and el.tie.type in ('stop', 'continue'):
                continue
            lyric = el.lyric if hasattr(el, 'lyric') else None
            out.append(dict(measure=mi, offset=str(F(el.getOffsetInHierarchy(meas)).limit_denominator(48)),
                            duration=str(F(el.duration.quarterLength).limit_denominator(48)),
                            pitch=max(p.midi for p in el.pitches), lyric=lyric))
    return out


def main():
    lines = {}
    for engine in ENGINES:
        notes, pages, offset = [], [], 0
        for path in files(engine):
            try:
                s = m21.converter.parse(str(path))
            except Exception as error:
                pages.append(dict(file=path.name, error=str(error)))
                continue
            part = vocal_part(s)
            ns = notes_of(part)
            n_meas = len(part.getElementsByClass(m21.stream.Measure))
            for n in ns:
                n['measure'] += offset
                n['page'] = page_of(path)
            offset += n_meas
            pages.append(dict(file=path.name, measures=n_meas, notes=len(ns)))
            notes.extend(ns)
        lines[engine] = dict(pages=pages, notes=notes)
        (ROOT / 'outputs' / ENGINES[engine] / 'vocal.json').write_text(json.dumps(lines[engine], indent=1) + '\n')
        print(engine, [p.get('measures') for p in pages], 'expected', EXPECTED_MEASURES, 'notes', len(notes))
    names = [e for e in ENGINES if lines[e]['notes']]
    agreement = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            pa = [n['pitch'] for n in lines[a]['notes']]; pb = [n['pitch'] for n in lines[b]['notes']]
            pairs = align(pa, pb)
            exact = sum(pa[i] == pb[j] for i, j in pairs)
            agreement[f'{a}-{b}'] = dict(exact_matches=exact, a_notes=len(pa), b_notes=len(pb),
                                         exact_fraction_of_a=exact / len(pa), exact_fraction_of_b=exact / len(pb))
            print(f'{a} vs {b}: {exact} exact matches of {len(pa)}/{len(pb)} notes')
    (ROOT / 'outputs/vocal-agreement.json').write_text(json.dumps(agreement, indent=1) + '\n')


if __name__ == '__main__':
    main()
