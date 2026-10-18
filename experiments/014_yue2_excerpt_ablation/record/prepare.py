"""Build the excerpt conditions for the YuE2 melody-imitation ablation. CPU only.

Source: experiment 007's reviewed lead-line/chord transcription of
*Theme from The Color Purple* (measures 0..LAST). Each condition changes only
what the score interface carries; style, lyrics (none) and seed are shared.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SOURCE = REPO / 'experiments/007_color_purple_sheet_yue2/inputs/source-events.json'
SKILL = Path.home() / 'maestro-runtime/YuE/skills/yue2-music/instrumental/scripts'
sys.path.insert(0, str(SKILL))
sys.path.insert(0, str(Path(__file__).parent))
from abc_tools import parse_abc            # official bounded-dialect parser
from compile_score import compile_events   # official single-voice compiler
from abc_two_voice import serialize

LAST = 16                      # pickup + intro (1-8) + section A (9-16)
BPM, KEY = 88, 'F'
SEEDS = (20261017, 20261018)
STYLE = ('Instrumental, solo acoustic grand piano, lyrical pastoral piano theme, '
         'gentle flowing arpeggio accompaniment, expressive legato melody, F major, 88 BPM, '
         'no vocals, no singing, no choir, no spoken words, no drums.')
SECTION = {'Intro': 'intro', 'A': 'verse'}
NOTE = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)


def frac(x):
    return F(x)


def grid(x):
    return F(round(x * 32), 32)


def chord_bass(symbol, low=41, high=52):
    """MIDI pitch of a chord symbol's bass (slash bass or root) within [low, high] (F2..E3)."""
    root = symbol.split('/')[-1] if '/' in symbol else re.match(r'[A-G][b#]?', symbol).group(0)
    pc = (NOTE[root[0]] + {'': 0, 'b': -1, '#': 1}[root[1:]]) % 12
    for p in range(low, high + 1):
        if p % 12 == pc:
            return p
    raise ValueError(symbol)


def load_excerpt():
    src = json.loads(SOURCE.read_text())
    bars = [b for b in src['bars'] if b['measure'] <= LAST]
    end = frac(bars[-1]['onset']) + frac(bars[-1]['duration'])
    notes = [(frac(t), frac(d), p) for t, d, p in src['notes'] if frac(t) < end]
    assert all(t + d <= end for t, d, _ in notes), 'a note crosses the excerpt end'
    chords = [(frac(t), c) for t, c in src['chords'] if frac(t) < end]
    out_bars = []
    for b in bars:
        out_bars.append(dict(start=frac(b['onset']), end=frac(b['onset']) + frac(b['duration']),
                             meter=b['meter'], section=SECTION.get(b['section'])))
    return out_bars, notes, chords, end


def quantize(notes):
    q = []
    for t, d, p in notes:
        a, b = grid(t), grid(t + d)
        assert b > a
        q.append((a, b - a, p))
    return q


def bass_line(chords, bars):
    """One held bass note per chord event, from its onset to the next chord or bar end."""
    events = []
    for i, (t, symbol) in enumerate(chords):
        bar = next(b for b in bars if b['start'] <= t < b['end'])
        nxt = chords[i + 1][0] if i + 1 < len(chords) else bar['end']
        stop = min(nxt, bar['end'])
        events.append((grid(t), grid(stop) - grid(t), chord_bass(symbol)))
    return events


def midi_file(path, tracks, bpm):
    """Minimal type-1 MIDI with one track per voice (960 ppq)."""
    import struct
    ppq = 960
    def vlq(v):
        out = [v & 127]
        while v >> 7:
            v >>= 7
            out.insert(0, (v & 127) | 128)
        return bytes(out)
    chunks = []
    for channel, notes in enumerate(tracks):
        events = [(0, 0, b'\xff\x51\x03' + round(60_000_000 / bpm).to_bytes(3, 'big'))]
        for t, d, p in notes:
            events.append((round(t * ppq), 2, bytes([0x90 | channel, p, 80])))
            events.append((round((t + d) * ppq), 1, bytes([0x80 | channel, p, 0])))
        data, cursor = bytearray(), 0
        for tick, _, msg in sorted(events, key=lambda e: (e[0], e[1])):
            data.extend(vlq(tick - cursor) + msg)
            cursor = tick
        data.extend(b'\x00\xff\x2f\x00')
        chunks.append(b'MTrk' + struct.pack('>I', len(data)) + data)
    path.write_bytes(b'MThd' + struct.pack('>IHHH', 6, 1, len(chunks), ppq) + b''.join(chunks))


def num(x):
    return int(x) if x.denominator == 1 else str(x)


def main():
    bars, notes, chords, end = load_excerpt()
    melody = quantize(notes)
    bass = bass_line(chords, bars)
    qchords = [(grid(t), 'E7' if c == 'E7+5' else c) for t, c in chords]
    rests = ([], [])
    conditions = {
        'melody-only': dict(cot='melody', voices={'Vocal': rests, 'Ins': (melody, [])}),
        'melody-chords': dict(cot='full', voices={'Vocal': ([], qchords), 'Ins': (melody, [])}),
        'melody-chords-bass': dict(cot='full', voices={'Vocal': (bass, qchords), 'Ins': (melody, [])}),
    }
    prepared = ROOT / 'prepared'
    prepared.mkdir(exist_ok=True)
    requests, summary = [], {}
    for name, spec in conditions.items():
        text = serialize(BPM, KEY, bars, spec['voices'])
        score = parse_abc(text)
        info = inspect(score)
        assert info['Ins'] == [(t, p) for t, _, p in melody], f'{name}: Ins melody mismatch'
        expected_vocal = [(t, p) for t, _, p in spec['voices']['Vocal'][0]]
        assert info['Vocal'] == expected_vocal, f'{name}: Vocal mismatch'
        assert info['chords'] == [(t, c) for t, c in spec['voices']['Vocal'][1]], f'{name}: chords mismatch'
        assert info['end'] == end, (info['end'], end)
        if name == 'melody-chords':
            reference, _ = compile_events(dict(bpm=BPM, key=KEY,
                bars=[dict(meter=b['meter'], **({'section': b['section']} if b['section'] else {})) for b in bars],
                notes=[[num(t), num(d), p] for t, d, p in melody], chords=[[num(t), c] for t, c in qchords]))
            summary['official_compiler_identical'] = (reference == text)
            if reference != text:
                (prepared / 'official-compiler-reference.abc').write_text(reference)
        for seed in SEEDS if name == 'melody-chords' else SEEDS[:1]:
            rid = f'{name}-{seed}'
            d = prepared / rid
            d.mkdir(exist_ok=True)
            (d / 'score.abc').write_text(text)
            request = dict(id=rid, style=STYLE, lyrics='', abc=text, cot=spec['cot'], seed=seed)
            (d / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
            requests.append(request)
    rid = f'model-composed-{SEEDS[0]}'
    d = prepared / rid
    d.mkdir(exist_ok=True)
    request = dict(id=rid, style=STYLE, lyrics='', cot='full', seed=SEEDS[0])
    (d / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
    requests.append(request)
    inputs = ROOT / 'inputs'
    inputs.mkdir(exist_ok=True)
    (inputs / 'excerpt-events.json').write_text(json.dumps(dict(
        source=str(SOURCE.relative_to(REPO)), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        measures=f'0-{LAST}', bpm=BPM, key=KEY, nominal_seconds=float(end) * 60 / BPM,
        bars=[dict(start=num(b['start']), end=num(b['end']), meter=b['meter'], section=b['section']) for b in bars],
        melody=[[num(t), num(d), p] for t, d, p in melody],
        bass=[[num(t), num(d), p] for t, d, p in bass],
        chords=[[num(t), c] for t, c in qchords],
        bass_rule='slash bass or chord root, F2-E3, held from the chord onset to the next chord or bar end',
    ), indent=2) + '\n')
    midi_file(inputs / 'melody.mid', [melody], BPM)
    midi_file(inputs / 'melody-bass.mid', [melody, bass], BPM)
    manifest = dict(requests=[r['id'] for r in requests], conditions=list(conditions) + ['model-composed'],
                    melody_notes=len(melody), bass_notes=len(bass), chord_events=len(qchords),
                    nominal_seconds=float(end) * 60 / BPM, **summary)
    (prepared / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


def inspect(score):
    """Onset/pitch lists per voice from the official parser: notes are [onset, pitch, duration]."""
    out = {voice: [(F(n[0]), n[1]) for n in score.voices[voice].notes] for voice in ('Vocal', 'Ins')}
    out['chords'] = [(F(c[0]), c[1]) for c in score.voices['Vocal'].chords]
    out['end'] = F(score.voices['Ins'].time)
    return out


if __name__ == '__main__':
    main()
