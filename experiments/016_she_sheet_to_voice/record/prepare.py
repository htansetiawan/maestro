"""Build the YuE2 request for She from the manual vocal transcription. CPU only.

Vocal voice: the melody with chord symbols. Ins voice: rests. Lyrics follow the
linearized form with section tags. Also writes a guide MIDI of the melody.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(Path.home() / 'maestro-runtime/YuE/skills/yue2-music/instrumental/scripts'))
sys.path.insert(0, str(REPO / 'experiments/014_yue2_excerpt_ablation/record'))
from abc_tools import parse_abc
from abc_two_voice import serialize
from prepare import midi_file

BPM = 70
STYLE = ('English, classic pop ballad, warm expressive male baritone, intimate crooner, '
         'solo acoustic grand piano accompaniment, slow and tender, C major, 70 BPM, no drums, no choir')
NOTE = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
TAG = dict(intro='[Intro]', verse='[Verse]', bridge='[Bridge]', outro='[Outro]')


def midi(name):
    return 12 * (int(name[-1]) + 1) + NOTE[name[0]] + {'': 0, '#': 1, 'b': -1}[name[1:-1]]


def main():
    d = json.loads((ROOT / 'inputs/vocal-transcription.json').read_text())
    by_n = {b['n']: b for b in d['bars']}
    bars, notes, chords, lyrics, time = [], [], [], [], F(0)
    for seg in d['linearized']:
        lines = []
        for n in seg['bars']:
            b = by_n[n]
            bars.append(dict(start=time, end=time + 4, meter='4/4', section=seg['section']))
            for onset, sym in b['chords']:
                chords.append((time + F(onset), sym))
            syllables = b['lyric2'].split() if seg['lyric'] == 2 and 'lyric2' in b else None
            offset, k = F(0), 0
            for tok in b['notes'].split():
                p, dur, *syl = tok.split(':')
                dur = F(dur)
                if p != 'r':
                    notes.append((time + offset, dur, midi(p)))
                    word = syllables[k] if syllables else (syl[0] if syl else '_')
                    if syllables:
                        k += 1
                    if word not in ('_', 'r'):
                        lines.append(word)
                elif syllables:
                    k += 1
                offset += dur
            assert offset == 4, (n, offset)
            time += 4
        if seg['section'] != 'intro':
            lyrics.append(TAG[seg['section']] + '\n' + join(lines))
    text = serialize(BPM, 'C', bars, {'Vocal': (notes, chords), 'Ins': ([], [])})
    score = parse_abc(text)
    assert [(F(n[0]), n[1]) for n in score.voices['Vocal'].notes] == [(t, p) for t, _, p in notes]
    assert [(F(c[0]), c[1]) for c in score.voices['Vocal'].chords] == chords
    assert not score.voices['Ins'].notes
    lyric_text = '\n\n'.join(lyrics) + '\n'
    request = dict(id='she-vocal-20261018', style=STYLE, lyrics=lyric_text, abc=text, cot='full', seed=20261018)
    out = ROOT / 'prepared'
    out.mkdir(exist_ok=True)
    (out / 'score.abc').write_text(text)
    (out / 'lyrics.txt').write_text(lyric_text)
    (out / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
    events = dict(bpm=BPM, key='C', melody=[[str(t), str(du), p] for t, du, p in notes],
                  chords=[[str(t), c] for t, c in chords], bars=len(bars), nominal_seconds=float(time) * 60 / BPM)
    (ROOT / 'inputs/linearized-events.json').write_text(json.dumps(events, indent=1) + '\n')
    midi_file(ROOT / 'inputs/melody.mid', [notes], BPM)
    print(json.dumps(dict(bars=len(bars), notes=len(notes), chords=len(chords), seconds=events['nominal_seconds'],
                          abc_chars=len(text), lyric_lines=len(lyrics))))


def join(words):
    """Rejoin hyphenated syllables into words, one phrase per printed bar group."""
    out = ''
    for w in words:
        if w.startswith('-'):
            out += w[1:]
        else:
            out += (' ' if out else '') + w
        if out.endswith('-'):
            out = out[:-1]
    return out


if __name__ == '__main__':
    main()
