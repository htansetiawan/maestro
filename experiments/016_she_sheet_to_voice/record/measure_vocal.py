"""Does the generated singer follow the written vocal line?

Separate the voice with Demucs (htdemucs, two stems), track its pitch with pYIN,
segment the f0 track into notes (runs of stable pitch of at least 80 ms), and
align that note sequence to the written melody with the same global pitch
alignment used for piano in experiment 014. Reports recall (any octave), exact
recall, longest exact run and the fitted tempo stretch.
"""
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import librosa

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / 'experiments/014_yue2_excerpt_ablation/record'))
from measure import align, longest_run


def separate(mp3, workdir):
    workdir.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, '-m', 'demucs.separate', '--two-stems=vocals', '-n', 'htdemucs',
                    '-o', str(workdir), str(mp3)], check=True)
    return next(workdir.rglob('vocals.wav'))


def vocal_notes(wav, sr=22050, min_ms=80):
    y, _ = librosa.load(str(wav), sr=sr, mono=True)
    f0, voiced, _ = librosa.pyin(y, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('C6'), sr=sr, frame_length=2048, hop_length=256)
    hop = 256 / sr
    midi = np.where(voiced & np.isfinite(f0), 12 * np.log2(np.maximum(f0, 1e-6) / 440) + 69, np.nan)
    notes, start, cur = [], None, []
    for i, m in enumerate(midi):
        if np.isnan(m):
            if cur and len(cur) * hop >= min_ms / 1000:
                notes.append((start * hop, len(cur) * hop, int(round(np.median(cur)))))
            cur, start = [], None
            continue
        if cur and abs(m - np.median(cur)) > 0.6:
            if len(cur) * hop >= min_ms / 1000:
                notes.append((start * hop, len(cur) * hop, int(round(np.median(cur)))))
            cur, start = [], None
        if not cur:
            start = i
        cur.append(m)
    if cur and len(cur) * hop >= min_ms / 1000:
        notes.append((start * hop, len(cur) * hop, int(round(np.median(cur)))))
    return notes, float(np.mean(voiced))


def main():
    events = json.loads((ROOT / 'inputs/linearized-events.json').read_text())
    bpm = events['bpm']
    ref = [(float(eval(t)) * 60 / bpm, p) for t, _, p in events['melody']]
    results = []
    for out in sorted((ROOT / 'outputs').glob('*/audio.mp3')):
        rid = out.parent.name
        vocals = separate(out, ROOT / 'work' / rid)
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(vocals), '-c:a', 'libmp3lame', '-b:a', '192k', str(out.parent / 'vocals.mp3')], check=True)
        notes, voiced_fraction = vocal_notes(vocals)
        pairs = align([p for _, p in ref], [p for _, _, p in notes])
        exact = [(i, j) for i, j in pairs if ref[i][1] == notes[j][2]]
        octv = [(i, j) for i, j in pairs if ref[i][1] != notes[j][2] and (ref[i][1] - notes[j][2]) % 12 == 0]
        matched = exact + octv
        tempo = onset_rms = None
        if len(matched) >= 4:
            x = np.array([ref[i][0] for i, _ in matched]); y = np.array([notes[j][0] for _, j in matched])
            slope, intercept = np.polyfit(x, y, 1); tempo = float(slope); onset_rms = float(np.sqrt(np.mean((y - (slope * x + intercept)) ** 2)))
        r = dict(id=rid, written_notes=len(ref), sung_notes=len(notes), voiced_fraction=voiced_fraction,
                 melody_recall=len(matched) / len(ref), exact_recall=len(exact) / len(ref),
                 precision=len(matched) / max(1, len(notes)), longest_exact_run=longest_run(sorted(i for i, _ in exact)),
                 tempo_ratio=tempo, aligned_onset_rms_seconds=onset_rms,
                 method='Demucs htdemucs vocals -> pYIN -> stable-pitch segments (>=80 ms) -> global pitch alignment')
        results.append(r)
        print(json.dumps(r))
        for w in (ROOT / 'work' / rid).rglob('*.wav'):
            w.unlink()
    (ROOT / 'record/vocal-adherence.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
