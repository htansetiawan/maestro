"""Compile a manually transcribed lead line; never performs model inference.

The TSV is a reduction of the source, not a transcription of both piano staves.
Rational source rhythms are retained separately from the native model grid.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {'Intro': 'intro', 'A': 'verse', 'B': 'chorus', 'C': 'verse',
            'D': 'chorus', 'E': 'verse', 'F': 'chorus', 'G': 'outro'}
# Grace-note timing is an explicit performance choice, not printed duration.
GRACES = {50: (F(0), ['Eb5', 'D5']), 82: (F(0), ['C4', 'Bb3', 'A3']),
          86: (F(2), ['C5', 'Db5'])}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=lambda x: number(x) if isinstance(x, F) else str(x)) + '\n')


def number(x):
    return int(x) if x.denominator == 1 else str(x)


def pitch(name):
    letter, acc, octave = re.fullmatch(r'([A-G])([b#]?)(\d)', name).groups()
    return 12 * (int(octave) + 1) + dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)[letter] + {'': 0, 'b': -1, '#': 1}[acc]


def read_source():
    bars, notes, chords, grace_record = [], [], [], []
    time, meter, pending = F(0), '4/4', False
    for line in (ROOT / 'inputs/transcription.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        measure, location, section, new_meter, melody, harmony = line.split('|')
        measure = int(measure)
        assert measure == len(bars), 'Skipped/duplicated source measure'
        meter = new_meter or meter
        beats = F(meter) * 4
        bars.append(dict(measure=measure, source_location=location, section=section,
                         meter=meter, onset=number(time), duration=number(beats)))
        offset = F(0)
        for token in melody.split():
            name, duration = token.split(':')
            tie = duration.endswith('~')
            duration = F(duration.rstrip('~'))
            if name != 'r':
                onset, length = time + offset, duration
                if measure in GRACES and offset == GRACES[measure][0]:
                    assert not pending
                    grace_names = GRACES[measure][1]
                    for i, grace in enumerate(grace_names):
                        notes.append([onset + F(i, 16), F(1, 16), pitch(grace)])
                    stolen = F(len(grace_names), 16)
                    grace_record.append(dict(measure=measure, beat=number(offset), pitches=grace_names,
                                             realization='1/16 quarter per grace, stolen from following note',
                                             stolen_quarters=number(stolen)))
                    onset += stolen
                    length -= stolen
                if pending:
                    assert notes[-1][2] == pitch(name) and notes[-1][0] + notes[-1][1] == onset
                    notes[-1][1] += length
                else:
                    notes.append([onset, length, pitch(name)])
            else:
                assert not pending and not tie
            pending = tie
            offset += duration
        assert offset == beats, f'Measure {measure}: {offset} != {beats}'
        for token in harmony.split():
            when, chord = token.split(':')
            assert 0 <= F(when) < beats
            chords.append([time + F(when), chord])
        time += beats
    assert not pending and len(bars) == 88
    assert [b['section'] for b in bars if b['section']] == ['Intro', *'ABCDEFG']
    assert [sum(b['source_location'].startswith(str(p)+'.') for b in bars) for p in range(1, 6)] == [12, 17, 19, 20, 20]
    return bars, notes, chords, grace_record, time


def midi(path, notes, bars, total):
    """Lead-only MIDI with exact thirds (960 ticks/quarter), meter and markers."""
    ppq = 960
    def vlq(value):
        out = [value & 127]
        while value >> 7:
            value >>= 7
            out.insert(0, (value & 127) | 128)
        return bytes(out)
    events = [(0, 0, b'\xff\x51\x03' + round(60_000_000 / 88).to_bytes(3, 'big')),
              (0, 0, b'\xff\x59\x02\xff\x00'), (0, 0, b'\xc0\x00')]
    previous_meter = None
    for bar in bars:
        tick = round(F(bar['onset']) * ppq)
        if bar['meter'] != previous_meter:
            n, d = map(int, bar['meter'].split('/'))
            events.append((tick, 0, b'\xff\x58\x04' + bytes([n, d.bit_length()-1, 24, 8])))
            previous_meter = bar['meter']
        if bar['section']:
            label = bar['section'].encode()
            events.append((tick, 0, b'\xff\x06' + vlq(len(label)) + label))
    for onset, duration, p in notes:
        events.extend([(round(onset * ppq), 2, bytes([0x90, p, 80])),
                       (round((onset+duration) * ppq), 1, bytes([0x80, p, 0]))])
    track, cursor = bytearray(), 0
    for tick, _, message in sorted(events, key=lambda x: (x[0], x[1])):
        track.extend(vlq(tick-cursor) + message)
        cursor = tick
    track.extend(vlq(round(total*ppq)-cursor) + b'\xff\x2f\x00')
    path.write_bytes(b'MThd' + struct.pack('>IHHH', 6, 0, 1, ppq) + b'MTrk' + struct.pack('>I', len(track)) + track)


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--skill-dir', type=Path, default=Path('/tmp/maestro-yue2/skills/yue2-music/instrumental'))
    cli.add_argument('--source-pdf', type=Path, default=ROOT/'source-private/theme_from_the_color_purple.pdf')
    args = cli.parse_args()
    sys.path.insert(0, str(args.skill_dir / 'scripts'))
    from compile_score import compile_events
    from instrumental import validate_request, prompt_text
    bars, notes, chords, graces, total = read_source()
    source = dict(bpm=88, key='F', bars=bars,
                  notes=[[number(t), number(d), p] for t, d, p in notes],
                  chords=[[number(t), c] for t, c in chords], grace_realizations=graces)
    write(ROOT / 'inputs/source-events.json', source)
    changes = []
    def grid(value):
        return F(round(value * 32), 32)
    quantized = []
    for i, (t, d, p) in enumerate(notes):
        start, stop = grid(t), grid(t + d)
        assert stop > start
        quantized.append([number(start), number(stop-start), p])
        if start != t or stop != t+d:
            changes.append(dict(kind='rhythm_grid', note_index=i, pitch=p,
                                source=[number(t), number(d)], native=[number(start), number(stop-start)],
                                onset_error_ms=float(start-t)*60/88*1000,
                                endpoint_error_ms=float(stop-t-d)*60/88*1000))
    native_chords = []
    for t, chord in chords:
        mapped = 'E7' if chord == 'E7+5' else chord
        native_chords.append([number(grid(t)), mapped])
        if chord != mapped or grid(t) != t:
            changes.append(dict(kind='chord_reduction', source=[number(t), chord], native=[number(grid(t)), mapped]))
    native_bars = [dict(meter=b['meter'], **({'section': SECTIONS[b['section']]} if b['section'] else {})) for b in bars]
    events = dict(bpm=88, key='F', bars=native_bars, notes=quantized, chords=native_chords)
    text, check = compile_events(events)
    request = dict(id='sheet-piano-20261005', style='Instrumental, solo acoustic grand piano, lyrical pastoral piano theme, '
                   'gentle flowing arpeggio accompaniment, expressive legato melody, F major, 88 BPM, '
                   'no vocals, no singing, no choir, no spoken words, no drums.',
                   lyrics='', abc=text, cot='full', seed=20261005)
    parsed = validate_request(request)
    assert parsed.voices['Ins'].time == total and not parsed.voices['Vocal'].notes
    prepared = ROOT / 'prepared'
    prepared.mkdir(exist_ok=True)
    for name, content in [('score.abc', text), ('prompt.txt', prompt_text(request)), ('style.txt', request['style']+'\n'), ('lyrics.txt', '')]:
        (prepared/name).write_text(content)
    repair = dict(changes=changes, grace_realizations=graces, unresolved=[], assumptions=[
        'Manual uppermost right-hand melody reduction, not complete two-staff piano transcription.',
        'Printed left-hand accompaniment and lower right-hand chord tones are represented by chord labels only.',
        'Measure 0 is a one-quarter pickup, encoded as 1/4 then 4/4; measure 75 changes to 3/4.',
        'Triplet endpoints are rounded to a 1/32-quarter grid; original rational durations remain in source-events.json.',
        'Grace durations are editorial: 1/16 quarter per note stolen from the following main note.',
        'E7+5 in measure 22 is reduced to E7 because the native chord vocabulary lacks augmented dominant seventh.',
        'Ritardando in measure 86 and the final fermata are retained as annotations; model timing stays at 88 BPM.',
        'Arpeggiation signs, dynamics, articulation, pedal and internal voicings are not encoded.',
        'Native section names approximate printed Intro/A–G; original labels and locations remain in the source table.',
        'Manually visually checked; no independent human proofreading or source-audio pitch comparison yet.'
    ])
    write(prepared/'repair-report.json', repair)
    write(prepared/'events.json', events)
    write(prepared/'request.json', request)
    check.update(passed=True, source_measures=87, pickup_measures=1, nominal_duration_seconds=float(total)*60/88,
                 vocal_sounding_notes=0, source_pdf_accuracy='manual visual transcription; independent proofreading pending',
                 generated_audio=False, rhythm_changes=len([c for c in changes if c['kind']=='rhythm_grid']),
                 maximum_endpoint_error_ms=max(abs(c[k]) for c in changes if c['kind']=='rhythm_grid' for k in ('onset_error_ms','endpoint_error_ms')))
    write(prepared/'score-check.json', check)
    midi(ROOT/'inputs/melody-exact.mid', notes, bars, total)
    midi(ROOT/'inputs/melody-native.mid', [[F(t), F(d), p] for t,d,p in quantized], bars, total)
    provenance = dict(title='Theme from The Color Purple', printed_pages=[39,40,41,42,43],
                      composers=['Quincy Jones', 'Rod Temperton', 'Jeremy Lubbock'], piano_arranger='Shiori Aoyama',
                      source='User-provided five-page Dropbox PDF; shared-link credentials omitted.',
                      source_pdf_sha256=hashlib.sha256(args.source_pdf.read_bytes()).hexdigest(),
                      source_pdf_bytes=args.source_pdf.stat().st_size, source_pdf_stored_in_git=False,
                      preparation='Manual visual reading of rendered PDF; no OMR or audio transcription model used.',
                      nominal_quarter_beats=number(total), tempo_quarter_bpm=88,
                      expressive_annotations=[dict(measure=86,marking='ritardando'),dict(measure=87,marking='fermata')],
                      tool_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                                   [args.skill_dir/'scripts'/n for n in ('compile_score.py','abc_tools.py','instrumental.py')]})
    write(ROOT/'inputs/source.json', provenance)
    write(prepared/'prepared-manifest.json', {'files':{p.name:dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
          for p in sorted(prepared.iterdir()) if p.is_file() and p.name!='prepared-manifest.json'}})
    print(json.dumps(dict(measures=len(bars), notes=len(notes), seconds=float(total)*60/88,
                          roundtrip=check['event_roundtrip'], max_endpoint_error_ms=check['maximum_endpoint_error_ms'])))


if __name__ == '__main__':
    main()
