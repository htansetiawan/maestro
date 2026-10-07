#!/usr/bin/env python3
"""Build a bounded, octave-adapted vocal score; no models or GPU calls."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1] / 'inputs'
SOURCE = ROOT / 'experiments/007_color_purple_sheet_yue2'
SKILL = Path('/tmp/maestro-yue2/skills/yue2-music/instrumental/scripts')
sys.path.insert(0, str(SKILL))
from compile_score import lengths, spelling, compress
from abc_tools import parse_abc, report

# Each phrase has one octave displacement throughout. Unlisted bars retain
# their exact original pitches in Ins. Hyphens here mark manual syllables only.
PHRASES = [
    (9, 11, -12, 'verse', 'Morn-ing in the Har-vard Yard'),
    (13, 14, -12, 'verse', 'Sun-light warms the old brick walls'),
    (17, 19, -24, 'chorus', 'Hold us here be-neath the star-light'),
    (21, 22, -12, 'chorus', 'In the qui-et soft light'),
    (25, 27, -24, 'verse', 'Books lie o-pen on the grass'),
    (28, 30, -24, 'verse', 'Laugh-ter floats be-neath the trees we chase the day'),
    (33, 36, -12, 'chorus', 'Red brick build-ings keep our sto-ries when our foot-steps fade'),
    (37, 38, -24, 'chorus', 'Let our love stay'),
    (44, 46, -12, 'verse', 'Some-one saves a place for me'),
    (47, 49, -12, 'verse', 'We trade our dreams be-neath the shel-ter of a tree'),
    (52, 55, -12, 'bridge', 'Year by year an-oth-er spring brings voic-es here'),
    (56, 59, -12, 'bridge', 'Stran-gers turn to life-long friends and learn to start a-gain'),
    (60, 63, -24, 'chorus', 'Hold us here a lit-tle long-er where the roots of love grow strong'),
    (64, 67, -24, 'chorus', 'In the Yard we learned be-long-ing let our sto-ries stay'),
    (68, 71, -12, 'chorus', 'When I walk these paths once more old friends come back to me'),
    (72, 74, -12, 'chorus', 'Har-vard Yard be-neath your trees all our love stays here'),
]


def enc(x):
    return int(x) if x.denominator == 1 else str(x)


def write(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, default=lambda v: enc(v) if isinstance(v, F) else str(v)) + '\n')


def render_bar(bar, voice, notes, chords):
    start, end = F(bar['onset']), F(bar['onset']) + F(bar['duration'])
    ns = [n for n in notes if n['voice'] == voice and n['onset'] < end and n['onset'] + n['duration'] > start]
    cs = []
    if voice == 'Vocal':
        current = next((c for t, c in reversed(chords) if t <= start), None)
        if current:
            cs.append((start, current))
        cs += [(t, c) for t, c in chords if start < t < end]
    if not ns and not cs:
        return 'Z'
    cuts = sorted({start, end, *(max(start, n['onset']) for n in ns),
                   *(min(end, n['onset'] + n['duration']) for n in ns), *(t for t, _ in cs)})
    result, active = [], {}
    for a, b in zip(cuts, cuts[1:]):
        result.extend('"' + c + '"' for t, c in cs if t == a)
        note = next((n for n in ns if n['onset'] <= a < n['onset'] + n['duration']), None)
        parts = lengths((b - a) * 32)
        for j, count in enumerate(parts):
            name = spelling(note['pitch'], 'F', active) if note else 'z'
            tie = '-' if note and (j < len(parts)-1 or b < note['onset'] + note['duration']) else ''
            result.append(name + (str(count) if count != 1 else '') + tie)
    return ''.join(result)


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    data = json.loads((SOURCE / 'prepared/events.json').read_text())
    source = json.loads((SOURCE / 'inputs/source-events.json').read_text())
    bars = source['bars']
    notes, changes, phrase_maps = [], [], []
    for idx, (on, dur, pitch) in enumerate(data['notes']):
        on, dur = F(on), F(dur)
        bar = next(b for b in bars if F(b['onset']) <= on < F(b['onset']) + F(b['duration']))
        pi = next((i for i, p in enumerate(PHRASES) if p[0] <= bar['measure'] <= p[1]), None)
        shift = PHRASES[pi][2] if pi is not None else 0
        note = dict(source_note_index=idx, measure=bar['measure'], onset=on, duration=dur,
                    pitch=pitch+shift, source_pitch=pitch, voice='Vocal' if pi is not None else 'Ins', phrase_index=pi)
        notes.append(note)
        if shift:
            changes.append(dict(source_note_index=idx, measure=bar['measure'], onset=enc(on), duration=enc(dur),
                                old_voice='Ins', new_voice='Vocal', original_midi=pitch, adapted_midi=pitch+shift,
                                semitone_change=shift, phrase_id=f'phrase-{pi+1:02d}'))
    vocal = [n for n in notes if n['voice'] == 'Vocal']
    for i, n in enumerate(vocal):
        n['vocal_note_index'] = i
    for pi, (lo, hi, shift, section, syll_text) in enumerate(PHRASES):
        ns = [n for n in vocal if n['phrase_index'] == pi]
        syllables = [(word.replace('-', ''), syl) for word in syll_text.split() for syl in word.split('-')]
        assert len(syllables) <= len(ns), (pi, len(syllables), len(ns))
        # Reserve surplus notes for a phrase-ending melisma; no new syllable
        # attacks on ornamental notes are required by this intended alignment.
        mapped = []
        for si, (word, syl) in enumerate(syllables):
            assigned = ns[si:] if si == len(syllables)-1 else [ns[si]]
            mapped.append(dict(word=word, syllable=syl, note_indices=[n['vocal_note_index'] for n in assigned],
                pitches=[n['pitch'] for n in assigned], onset=enc(assigned[0]['onset']),
                duration=enc(assigned[-1]['onset'] + assigned[-1]['duration'] - assigned[0]['onset']),
                articulation='Sustain final vowel across these notes; release consonant at phrase end.' if len(assigned)>1 else 'One syllable attack on this note.'))
        phrase_maps.append(dict(phrase_id=f'phrase-{pi+1:02d}', section=section, measures=[lo, hi],
            onset=enc(ns[0]['onset']), end=enc(ns[-1]['onset']+ns[-1]['duration']), octave_shift=shift//12,
            lyric=syll_text.replace('-', ''), syllables=mapped))
    sections = []
    for b in bars:
        p = next((p for p in PHRASES if p[0] <= b['measure'] <= p[1]), None)
        sections.append(p[3] if p else ('intro' if b['measure'] < 9 else 'outro' if b['measure'] >= 75 else 'interlude'))
    chords = [(F(t), c) for t, c in data['chords']]
    lines = ['X:1', 'T:', 'M:1/4', 'L:1/128', 'Q:1/4=88',
        'V: Vocal clef=treble name="Vocal Melody" snm="Vocal"',
        'V: Ins clef=treble name="Ins Melody" snm="Inst."', 'K:F']
    idx = 0
    while idx < len(bars):
        end = idx+1
        while end < len(bars) and end-idx < 4 and sections[end] == sections[idx] and bars[end]['meter'] == bars[idx]['meter']:
            end += 1
        if idx == 0 or sections[idx] != sections[idx-1]:
            lines.append('% ' + sections[idx])
        for voice in ('Vocal', 'Ins'):
            lines.append('V: ' + voice)
            if idx and bars[idx]['meter'] != bars[idx-1]['meter']:
                lines.append('M:' + bars[idx]['meter'])
            lines.append(compress([render_bar(b, voice, notes, chords) for b in bars[idx:end]]))
        idx = end
    abc = '\n'.join(lines) + '\n'
    parsed = parse_abc(abc)
    original = parse_abc((SOURCE / 'prepared/score.abc').read_text())
    for voice in ('Vocal', 'Ins'):
        expected = [(n['onset'], n['pitch'], n['duration']) for n in notes if n['voice'] == voice]
        assert list(map(tuple, parsed.voices[voice].notes)) == expected
        assert parsed.voices[voice].bars == original.voices[voice].bars
        assert parsed.voices[voice].keys == original.voices[voice].keys
    assert parsed.bpm == original.bpm == 88
    assert parsed.unit == original.unit
    assert parsed.voices['Vocal'].chords == original.voices['Vocal'].chords
    assert len(parsed.voices['Vocal'].bars) == len(original.voices['Vocal'].bars) == 88
    assert sorted((n['onset'], n['pitch'] % 12, n['duration']) for n in notes) == sorted((t, p % 12, d) for t, p, d in original.voices['Ins'].notes)
    covered = [ni for p in phrase_maps for s in p['syllables'] for ni in s['note_indices']]
    assert covered == list(range(len(vocal)))
    lyric_lines = ['[Intro]']
    # Lyrics carry the same interlude boundaries as the score; these tags are
    # guidance, not a forced synchronization interface.
    last_end, last_section = 8, 'intro'
    for p in phrase_maps:
        if p['measures'][0] > last_end+1:
            lyric_lines += ['', '[Instrumental Break]']
            last_section = 'interlude'
        if p['section'] != last_section:
            lyric_lines += ['', '[' + p['section'].title() + ']']
        lyric_lines.append(p['lyric'])
        last_end, last_section = p['measures'][1], p['section']
    lyric_lines += ['', '[Outro]', '']
    lyrics = '\n'.join(lyric_lines)
    style = ('Warm expressive male baritone singing in English, intimate lyrical solo acoustic grand piano accompaniment, '
             'pastoral cinematic ballad, gentle flowing piano arpeggios, F major, 88 BPM. '
             'Follow the supplied Vocal melody and harmony; piano plays Ins passages and accompaniment. '
             'Natural clear diction, legato singing with phrase-ending melismas and breathing between phrases. '
             'Instrumental piano introduction, interludes and outro. One male singer and one acoustic grand piano only; '
             'no backing singers, choir, orchestra, guitar, drums or spoken words.')
    request = dict(id='sheet-piano-vocal-20261006', style=style, lyrics=lyrics, abc=abc, cot='full', seed=20261006)
    (OUT / 'vocal.abc').write_text(abc)
    (OUT / 'lyrics.txt').write_text(lyrics)
    write('request.json', request)
    write('lyric-note-map.json', dict(schema_version=1, voice='Vocal', note_index_base=0,
        note_index_definition='Sounding Vocal notes after merging ABC ties, chronological order; excludes Ins notes.',
        status='Intended manual syllable mapping only; not a model API input or measured audio alignment.',
        pronunciation_source='Manual English orthographic syllabification; no dictionary phonemes supplied or claimed.',
        note_count=len(vocal), phrases=phrase_maps))
    source_lyrics = ROOT / 'experiments/003_color_purple_yard_vocals/lyrics.txt'
    old_lines = [s for s in source_lyrics.read_text().splitlines() if s and not s.startswith('[')]
    new_lines = [p['lyric'] for p in phrase_maps]
    source_paths = [SOURCE/'prepared/score.abc', SOURCE/'prepared/events.json', SOURCE/'inputs/source-events.json', SOURCE/'inputs/transcription.tsv', source_lyrics]
    manifest = dict(schema_version=1, contract='Preserve all prepared lead events, onset/duration, pitch class, harmony, complete 87 measures plus pickup, 88 BPM and meters. Route selected phrases to Vocal with documented whole-octave shifts; preserve all remaining notes in Ins.',
        source_hashes={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
        scope='Symbolic adaptation only. No audio generated or listened to by this script. Inherits experiment 007 transcription and rhythm reductions; does not independently certify PDF note accuracy.',
        rationale='Piano melody ranges and phrase ornaments are unsuitable for direct unedited singing. Coherent phrases move down one or two octaves for a warm male baritone; piano retains intro, outro and turnarounds. Fewer lyrics leave held vowels and melismas instead of compressing the original long poem.',
        vocal_range_midi=[min(n['pitch'] for n in vocal), max(n['pitch'] for n in vocal)],
        vocal_range_name='A2–G4', changed_notes=changes,
        instrumental_measures=[b['measure'] for b, s in zip(bars, sections) if s in {'intro','interlude','outro'}],
        changed_harmony=[], changed_timing=[], section_assignments=[dict(measure=b['measure'], section=s) for b,s in zip(bars,sections)],
        lyrics=dict(retained_verbatim_lines=[s for s in new_lines if s in old_lines],
            revised_or_new_lines=[s for s in new_lines if s not in old_lines],
            original_lines_not_retained_verbatim=[s for s in old_lines if s not in new_lines],
            themes_preserved=['Harvard Yard','red brick buildings','trees','friendship','love','college memories','returning years later']),
        checks=dict(native_abc_parse=True, complete_bar_grid=True, note_count_preserved=len(notes),
            pitch_class_onset_duration_preserved=True, unchanged_harmony_events=True,
            every_vocal_note_mapped_once=True, vocal_note_count=len(vocal), instrumental_note_count=len(notes)-len(vocal)),
        inspection=report(parsed))
    write('edit_manifest.json', manifest)
    print(json.dumps(manifest['checks'], indent=2))


if __name__ == '__main__':
    main()
