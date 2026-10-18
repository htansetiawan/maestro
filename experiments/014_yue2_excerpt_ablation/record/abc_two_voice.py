"""Serialize two monophonic voices into YuE2's native ABC dialect.

Unlike the skill's compile_score.py, this writer allows sounding notes in the
``Vocal`` voice, so an instrumental bass line can be probed there. Times are
quarter-note Fractions; the output grid is L:1/128 (1/32 quarter), matching
experiment 007. Validate the result with the official abc_tools.parse_abc.
"""
from fractions import Fraction as F
import re

DURATIONS = (48, 32, 24, 16, 12, 8, 6, 4, 3, 2, 1)
UNIT = F(1, 32)            # quarter notes per L:1/128 unit
NATURAL = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
FLAT_ORDER = 'BEADGCF'
SHARP_ORDER = 'FCGDAEB'
KEY_SIGNATURE = {'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6,
                 'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6}


def key_accidentals(key):
    count = KEY_SIGNATURE[key]
    letters = SHARP_ORDER[:count] if count > 0 else FLAT_ORDER[:-count]
    return {letter: (1 if count > 0 else -1) if letter in letters else 0 for letter in NATURAL}


def split_units(units):
    assert units.denominator == 1 and units > 0, units
    left, parts = int(units), []
    for part in DURATIONS:
        while left >= part:
            parts.append(part)
            left -= part
    return parts


def spell(pitch, key, active):
    signature = key_accidentals(key)
    prefer_flat = KEY_SIGNATURE[key] <= 0
    best = None
    for letter, pc in NATURAL.items():
        for alteration in (-1, 0, 1):
            base = pitch - alteration - 60 - pc
            if base % 12:
                continue
            octave = base // 12
            score = (alteration != signature[letter], abs(alteration),
                     (alteration > 0) if prefer_flat else (alteration < 0))
            candidate = (score, letter, alteration, octave)
            if best is None or candidate < best:
                best = candidate
    _, letter, alteration, octave = best
    mark = ''
    if alteration != active.get(letter, signature[letter]):
        mark = {-1: '_', 0: '=', 1: '^'}[alteration]
        active[letter] = alteration
    if octave < 0:
        name = letter + ',' * (-octave)
    elif octave == 0:
        name = letter
    else:
        name = letter.lower() + "'" * (octave - 1)
    return mark + name


def bar_text(start, end, notes, chords, key):
    """One bar of one voice. notes: [(onset, duration, pitch)] inside [start, end)."""
    events = sorted(n for n in notes if start <= n[0] < end)
    chord_times = sorted(t for t, _ in chords if start <= t < end)
    chord_at = {t: c for t, c in chords if start <= t < end}
    if not events and not chord_times:
        return 'Z'
    active, out, time = {}, [], start
    def emit_rest(a, b):
        nonlocal time
        boundaries = [t for t in chord_times if a < t < b]
        for seg_start, seg_end in zip([a] + boundaries, boundaries + [b]):
            if seg_start in chord_at:
                out.append(f'"{chord_at[seg_start]}"')
            for part in split_units((seg_end - seg_start) / UNIT):
                out.append('z' if part == 1 else f'z{part}')
        time = b
    for onset, duration, pitch in events:
        assert onset >= time, f'overlapping notes at {onset}'
        if onset > time:
            emit_rest(time, onset)
        stop = onset + duration
        assert stop <= end, f'note at {onset} crosses the bar line'
        name = spell(pitch, key, active)
        boundaries = [t for t in chord_times if onset < t < stop]
        segments = list(zip([onset] + boundaries, boundaries + [stop]))
        tokens = []
        for seg_start, seg_end in segments:
            prefix = f'"{chord_at[seg_start]}"' if seg_start in chord_at else ''
            parts = split_units((seg_end - seg_start) / UNIT)
            for i, part in enumerate(parts):
                tokens.append((prefix if i == 0 else '') + (name if (seg_start == onset and i == 0) else re.sub(r'^[_=^]+', '', name)) + ('' if part == 1 else str(part)))
        out.append('-'.join(tokens))
        time = stop
    if time < end:
        emit_rest(time, end)
    return ''.join(out)


def serialize(bpm, key, bars, voices, sections=None):
    """bars: [dict(start, end, meter, section)], voices: {'Vocal': (notes, chords), 'Ins': (notes, chords)}."""
    groups, current = [], []
    for i, bar in enumerate(bars):
        new_group = (not current or len(current) == 4 or bar['meter'] != current[-1]['meter']
                     or (bar.get('section') and bar['section'] != current[-1].get('section')))
        if new_group and current:
            groups.append(current)
            current = []
        current.append(bar)
    groups.append(current)
    lines = ['X:1', 'T:', f'M:{bars[0]["meter"]}', 'L:1/128', f'Q:1/4={bpm}',
             'V: Vocal clef=treble name="Vocal Melody" snm="Vocal"',
             'V: Ins clef=treble name="Ins Melody" snm="Inst."', f'K:{key}']
    meter, section = bars[0]['meter'], None
    for group in groups:
        if group[0].get('section') and group[0]['section'] != section:
            section = group[0]['section']
            lines.append(f'% {section}')
        meter_line = f'M:{group[0]["meter"]}' if group[0]['meter'] != meter or group is groups[0] and False else None
        meter_changed = group[0]['meter'] != meter
        meter = group[0]['meter']
        for voice in ('Vocal', 'Ins'):
            notes, chords = voices[voice]
            lines.append(f'V: {voice}')
            if meter_changed:
                lines.append(f'M:{meter}')
            texts = [bar_text(b['start'], b['end'], notes, chords, key) for b in group]
            lines.append(compress(texts))
    return '\n'.join(lines) + '\n'


def compress(texts):
    out, i = [], 0
    while i < len(texts):
        if texts[i] != 'Z':
            out.append(texts[i] + '|')
            i += 1
            continue
        j = i
        while j < len(texts) and texts[j] == 'Z':
            j += 1
        out.append('Z' + (str(j - i) if j - i > 1 else '') + '|')
        i = j
    return ''.join(out)
