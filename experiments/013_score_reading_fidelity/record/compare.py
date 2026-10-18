"""Compare each OMR engine's reading of the printed score with the reviewed manual
lead-line transcription (experiment 007), and count what the full two-staff
score contains that YuE2's two monophonic voices cannot carry.

Outputs per engine: outputs/<engine>/reading.json (per-measure events),
outputs/<engine>/two-hands.mid; and outputs/comparison.json overall.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

import music21 as m21
import re

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
MANUAL = json.loads((REPO / 'experiments/007_color_purple_sheet_yue2/inputs/source-events.json').read_text())
PAGE_MEASURES = [12, 17, 19, 20, 20]          # bars per printed page in the manual table (page 1 includes the pickup)
sys.path.insert(0, str(REPO / 'experiments/014_yue2_excerpt_ablation/record'))
from measure import align                      # same global pitch alignment as the audio measurement


ENGINE_DIRS = dict(audiveris='audiveris-pages', homr='homr', oemer='oemer')   # one book per scanned page


def page_of(path):
    m = re.search(r'page-(\d)', path.name)
    return int(m.group(1)) if m else 0


def files(engine):
    d = ROOT / 'outputs' / ENGINE_DIRS[engine]
    found = sorted([p for p in d.rglob('*') if p.suffix in ('.mxl', '.musicxml', '.xml') and 'run.log' not in p.name],
                   key=lambda p: (page_of(p), p.name))
    return found


def read(path):
    """Return list of measures; each has staff -> [(offset_quarters, duration_quarters, [midi...])] and chord symbols."""
    score = m21.converter.parse(str(path))
    parts = list(score.parts) if hasattr(score, 'parts') and len(score.parts) else [score]
    measures = {}
    for pi, part in enumerate(parts):
        for meas in part.getElementsByClass(m21.stream.Measure):
            key = meas.measureNumber if meas.measureNumber is not None else len(measures)
            slot = measures.setdefault(key, dict(staves={}, chords=[], meter=None))
            if meas.timeSignature is not None:
                slot['meter'] = meas.timeSignature.ratioString
            events = slot['staves'].setdefault(pi, [])
            for el in meas.recurse().notes:
                if el.isRest:
                    continue
                pitches = [p.midi for p in el.pitches]
                is_grace = el.duration.isGrace
                tup = bool(el.duration.tuplets)
                events.append(dict(offset=str(F(el.getOffsetInHierarchy(meas)).limit_denominator(96)),
                                   duration=str(F(el.duration.quarterLength).limit_denominator(96)),
                                   pitches=pitches, grace=is_grace, tuplet=tup,
                                   tie=(el.tie.type if el.tie else None)))
            for h in meas.recurse().getElementsByClass(m21.harmony.ChordSymbol):
                slot['chords'].append(dict(offset=str(F(h.getOffsetInHierarchy(meas)).limit_denominator(96)), figure=h.figure))
    return [measures[k] for k in sorted(measures)], score


def skyline(measures, staff=0):
    """Top pitch at each attack of the given staff, in reading order, with (measure index, offset)."""
    out = []
    for mi, meas in enumerate(measures):
        for ev in sorted(meas['staves'].get(staff, []), key=lambda e: F(e['offset'])):
            if ev['grace'] or ev['tie'] in ('stop', 'continue'):
                continue
            out.append((mi, F(ev['offset']), max(ev['pitches'])))
    return out


def manual_melody():
    bars = MANUAL['bars']
    out = []
    for t, d, p in MANUAL['notes']:
        t = F(t)
        bar = next(i for i, b in enumerate(bars) if F(b['onset']) <= t < F(b['onset']) + F(b['duration']))
        out.append((bar, t - F(bars[bar]['onset']), p))
    return out


def ledger(measures):
    """What the printed score holds, by staff: notes, chord stacks, left-hand notes, tuplets, graces."""
    counts = dict(right_hand_attacks=0, right_hand_sounding_notes=0, right_hand_chord_stacks=0,
                  left_hand_attacks=0, left_hand_sounding_notes=0, tuplet_events=0, grace_notes=0, chord_symbols=0)
    for meas in measures:
        for staff, events in meas['staves'].items():
            hand = 'right_hand' if staff == 0 else 'left_hand'
            for ev in events:
                if ev['tie'] in ('stop', 'continue'):
                    continue
                if ev['grace']:
                    counts['grace_notes'] += 1
                    continue
                counts[f'{hand}_attacks'] += 1
                counts[f'{hand}_sounding_notes'] += len(ev['pitches'])
                if hand == 'right_hand' and len(ev['pitches']) > 1:
                    counts['right_hand_chord_stacks'] += 1
                counts['tuplet_events'] += ev['tuplet']
        counts['chord_symbols'] += len(meas['chords'])
    return counts


def main():
    manual = manual_melody()
    manual_pitches = [p for _, _, p in manual]
    report = dict(manual=dict(measures=len(MANUAL['bars']), melody_notes=len(manual), chord_events=len(MANUAL['chords'])), engines={})
    for engine in ('audiveris', 'homr', 'oemer'):
        found = files(engine)
        if not found:
            report['engines'][engine] = dict(status='no output')
            continue
        measures, per_page = [], []
        combined = m21.stream.Score()
        for path in found:
            try:
                ms, score = read(path)
            except Exception as error:
                per_page.append(dict(file=path.name, error=str(error)))
                continue
            per_page.append(dict(file=path.name, measures=len(ms), staves=max((len(m['staves']) for m in ms), default=0)))
            measures.extend(ms)
            for part in (score.parts if len(score.parts) else [score]):
                combined.insert(0, part) if False else None
        sky = skyline(measures, staff=0)
        pairs = align(manual_pitches, [p for _, _, p in sky])
        exact = [(i, j) for i, j in pairs if manual_pitches[i] == sky[j][2]]
        octave = [(i, j) for i, j in pairs if manual_pitches[i] != sky[j][2] and (manual_pitches[i] - sky[j][2]) % 12 == 0]
        # Measure-level agreement where the measure counts line up page by page.
        by_page = {}
        for path, pp in zip(found, per_page):
            by_page[page_of(path)] = by_page.get(page_of(path), 0) + (pp.get('measures') or 0)
        same_grid = [by_page.get(i + 1, 0) for i in range(5)] == PAGE_MEASURES
        per_measure = []
        if same_grid:
            for mi, bar in enumerate(MANUAL['bars']):
                want = sorted((off, p) for b, off, p in manual if b == mi)
                got = sorted((off, p) for b, off, p in sky if b == mi)
                per_measure.append(dict(measure=mi, manual=[[str(o), p] for o, p in want], omr_top=[[str(o), p] for o, p in got],
                                        match=(want == got)))
        starts = [sum(PAGE_MEASURES[:i]) for i in range(5)]
        covered_bars = {b for i in range(5) if by_page.get(i + 1, 0) for b in range(starts[i], starts[i] + PAGE_MEASURES[i])}
        covered_idx = [k for k, (b, _, _) in enumerate(manual) if b in covered_bars]
        hit = {i for i, _ in exact + octave}
        recall_covered = (len(hit & set(covered_idx)) / len(covered_idx)) if covered_idx else None
        entry = dict(status='parsed', files=per_page, pages_read=sum(1 for i in range(5) if by_page.get(i + 1, 0)),
                     melody_recall_on_pages_read=recall_covered, measures_by_page=[by_page.get(i + 1, 0) for i in range(5)],
                     expected_measures_by_page=PAGE_MEASURES, measures_total=len(measures), measure_grid_matches_manual=same_grid,
                     melody_recall=len(exact + octave) / len(manual), exact_recall=len(exact) / len(manual),
                     skyline_precision=len(exact + octave) / max(1, len(sky)), skyline_notes=len(sky),
                     measures_exact=sum(m['match'] for m in per_measure) if per_measure else None,
                     ledger=ledger(measures),
                     chords_read=[c['figure'] for m in measures for c in m['chords']][:200])
        out = ROOT / 'outputs' / engine
        (out / 'reading.json').write_text(json.dumps(dict(measures=measures, per_measure=per_measure), indent=1, default=str) + '\n')
        # Two-hand MIDI of the engine's reading, for listening.
        try:
            whole = m21.stream.Score()
            for path in found:
                s = m21.converter.parse(str(path))
                for pi, part in enumerate(s.parts if len(s.parts) else [s]):
                    whole.insert(0, part)
            whole.write('midi', fp=str(out / 'two-hands.mid'))
            entry['two_hands_midi'] = True
        except Exception as error:
            entry['two_hands_midi'] = f'failed: {error}'
        report['engines'][engine] = entry
        print(engine, json.dumps({k: v for k, v in entry.items() if k not in ('chords_read', 'files')}, default=str))
    (ROOT / 'outputs/comparison.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
    parsed = {k: v for k, v in report['engines'].items() if v.get('status') == 'parsed'}
    if parsed:
        best = max(parsed, key=lambda k: parsed[k]['melody_recall'])
        L = parsed[best]['ledger']
        total = L['right_hand_sounding_notes'] + L['left_hand_sounding_notes']
        native = {'', 'm', 'dim', 'aug', '7', 'maj7', 'm7', 'dim7', 'm7b5', 'sus4', 'sus2', '6', 'm6', '7sus4', 'm(maj7)'}
        unsupported = [c for _, c in MANUAL['chords'] if re.sub(r'^[A-G][b#]?', '', c.split('/')[0]) not in native]
        (ROOT / 'outputs/loss-ledger.json').write_text(json.dumps(dict(
            engine=best, melody_notes=L['right_hand_attacks'], rh_inner_notes=L['right_hand_sounding_notes'] - L['right_hand_attacks'],
            lh_notes=L['left_hand_sounding_notes'], chord_symbols=len(MANUAL['chords']), unsupported_chords=len(unsupported),
            unsupported_chord_list=unsupported, graces=L['grace_notes'], tuplets=L['tuplet_events'],
            total_sounding_notes=total, carried_fraction=L['right_hand_attacks'] / total if total else None,
            note='Counts come from the best-agreeing OMR reading of the two staves; the top note of each right-hand attack is the only layer YuE2 can take as notes.'),
            indent=2) + '\n')


if __name__ == '__main__':
    main()
