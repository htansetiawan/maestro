"""Build the OMR benchmark inputs: two pieces with exact ground truth, rendered to pages.

Pieces: Mozart K.545 first movement (KernScores `**kern`, 73 bars) and a 16-bar
simple-piano-book arrangement of Beethoven's Ode to Joy theme encoded here with
music21. Each is rendered by Verovio to page images at 300 dpi (clean), and a
degraded copy imitates a scan: slight rotation, blur, noise, hard binarization.
Ground truth is the source encoding itself, exported as MusicXML and as a
per-staff event list.
"""
from fractions import Fraction as F
import io
import json
from pathlib import Path
import random

import cairosvg
import music21 as m21
import numpy as np
from PIL import Image, ImageFilter
import verovio

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source'
PAGES = ROOT / 'pages'
random.seed(20261018)


def ode_to_joy():
    """Two-staff easy arrangement in C major: melody in the right hand, root-fifth dyads in the left."""
    melody = [  # (pitch, quarterLength) per bar, Beethoven's theme, 16 bars
        [('E4', 1), ('E4', 1), ('F4', 1), ('G4', 1)], [('G4', 1), ('F4', 1), ('E4', 1), ('D4', 1)],
        [('C4', 1), ('C4', 1), ('D4', 1), ('E4', 1)], [('E4', 1.5), ('D4', 0.5), ('D4', 2)],
        [('E4', 1), ('E4', 1), ('F4', 1), ('G4', 1)], [('G4', 1), ('F4', 1), ('E4', 1), ('D4', 1)],
        [('C4', 1), ('C4', 1), ('D4', 1), ('E4', 1)], [('D4', 1.5), ('C4', 0.5), ('C4', 2)],
        [('D4', 1), ('D4', 1), ('E4', 1), ('C4', 1)], [('D4', 1), ('E4', 0.5), ('F4', 0.5), ('E4', 1), ('C4', 1)],
        [('D4', 1), ('E4', 0.5), ('F4', 0.5), ('E4', 1), ('D4', 1)], [('C4', 1), ('D4', 1), ('G3', 2)],
        [('E4', 1), ('E4', 1), ('F4', 1), ('G4', 1)], [('G4', 1), ('F4', 1), ('E4', 1), ('D4', 1)],
        [('C4', 1), ('C4', 1), ('D4', 1), ('E4', 1)], [('D4', 1.5), ('C4', 0.5), ('C4', 2)],
    ]
    bass = [  # left hand: two half-note dyads per bar (root and fifth)
        ['C3 G3', 'C3 G3'], ['G2 D3', 'G2 D3'], ['C3 G3', 'C3 G3'], ['G2 D3', 'C3 G3'],
        ['C3 G3', 'C3 G3'], ['G2 D3', 'G2 D3'], ['C3 G3', 'C3 G3'], ['G2 D3', 'C3 G3'],
        ['G2 D3', 'C3 G3'], ['G2 D3', 'C3 G3'], ['G2 D3', 'C3 G3'], ['G2 D3', 'G2 D3'],
        ['C3 G3', 'C3 G3'], ['G2 D3', 'G2 D3'], ['C3 G3', 'C3 G3'], ['G2 D3', 'C3 G3'],
    ]
    rh, lh = m21.stream.Part(), m21.stream.Part()
    rh.insert(0, m21.instrument.Piano()); lh.insert(0, m21.instrument.Piano())
    rh.partName, lh.partName = 'Piano', 'Piano'
    for i, (mel, bs) in enumerate(zip(melody, bass), 1):
        mr, ml = m21.stream.Measure(number=i), m21.stream.Measure(number=i)
        if i == 1:
            mr.append(m21.clef.TrebleClef()); ml.append(m21.clef.BassClef())
            for mm in (mr, ml):
                mm.append(m21.key.KeySignature(0)); mm.append(m21.meter.TimeSignature('4/4'))
            mr.insert(0, m21.tempo.MetronomeMark(number=108))
        for p, q in mel:
            mr.append(m21.note.Note(p, quarterLength=q))
        for dyad in bs:
            ml.append(m21.chord.Chord(dyad.split(), quarterLength=2))
        rh.append(mr); ml.append(m21.bar.Barline('final') if i == 16 else m21.bar.Barline('regular')); lh.append(ml)
    s = m21.stream.Score([rh, lh])
    s.insert(0, m21.metadata.Metadata(title='Ode to Joy', composer='L. van Beethoven, easy arrangement'))
    s.insert(0, m21.layout.StaffGroup([rh, lh], symbol='brace'))
    return s


def events_by_staff(score):
    """Ground-truth note list per part: (measure index, offset, duration, [midi]) for sounding attacks."""
    out = []
    for part in score.parts:
        rows = []
        for mi, meas in enumerate(part.getElementsByClass(m21.stream.Measure)):
            for el in meas.recurse().notes:
                if el.isRest or el.duration.isGrace or (el.tie and el.tie.type in ('stop', 'continue')):
                    continue
                rows.append(dict(measure=mi, offset=str(F(el.getOffsetInHierarchy(meas)).limit_denominator(96)),
                                 duration=str(F(el.duration.quarterLength).limit_denominator(96)),
                                 pitches=sorted(p.midi for p in el.pitches)))
        out.append(rows)
    return out


def render(path, stem, scale=38):
    tk = verovio.toolkit()
    tk.setOptions({"pageHeight": 2970, "pageWidth": 2100, "scale": scale, "adjustPageHeight": False,
                   "breaks": "auto", "header": "none", "footer": "none"})
    assert tk.loadFile(str(path)), path
    n = tk.getPageCount()
    for i in range(1, n + 1):
        svg = tk.renderToSVG(i)
        png = cairosvg.svg2png(bytestring=svg.encode(), dpi=300, output_width=2480)
        rgba = Image.open(io.BytesIO(png)).convert('RGBA')
        white = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
        img = Image.alpha_composite(white, rgba).convert('L')
        (PAGES / 'clean').mkdir(parents=True, exist_ok=True)
        img.save(PAGES / 'clean' / f'{stem}-{i}.png')
        degrade(img).save((PAGES / 'degraded' / f'{stem}-{i}.png') if (PAGES / 'degraded').mkdir(parents=True, exist_ok=True) is None else None)
    return n


def degrade(img):
    """Imitate a 300 dpi photocopy scan: 0.4 degree skew, blur, speckle, hard threshold."""
    rotated = img.rotate(random.uniform(-0.5, 0.5), resample=Image.BICUBIC, fillcolor=255)
    blurred = rotated.filter(ImageFilter.GaussianBlur(radius=1.1))
    a = np.asarray(blurred).astype(np.float32)
    a += np.random.default_rng(1).normal(0, 18, a.shape)
    a = np.clip(a, 0, 255)
    binary = (a > 150).astype(np.uint8) * 255
    return Image.fromarray(binary)


def main():
    SRC.mkdir(exist_ok=True)
    ode = ode_to_joy()
    ode.write('musicxml', fp=str(SRC / 'ode-to-joy.musicxml'))
    manifest = {}
    for stem, path in [('k545-1', SRC / 'k545-1.krn'), ('ode-to-joy', SRC / 'ode-to-joy.musicxml')]:
        score = m21.converter.parse(str(path))
        truth = events_by_staff(score)
        (SRC / f'{stem}-truth.json').write_text(json.dumps(truth) + '\n')
        if stem == 'k545-1':
            score.write('musicxml', fp=str(SRC / 'k545-1.musicxml'))
        pages = render(path, stem)
        manifest[stem] = dict(source=path.name, staves=len(truth), notes_per_staff=[len(t) for t in truth],
                              measures=len(score.parts[0].getElementsByClass(m21.stream.Measure)), pages=pages)
        print(stem, manifest[stem])
    (ROOT / 'inputs-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
