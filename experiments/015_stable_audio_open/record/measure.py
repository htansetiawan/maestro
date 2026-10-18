"""How much of the source piano survives each Stable Audio output?

Chroma similarity (frame-wise cosine of CQT chroma, after a small global lag
search) and the melody adherence measurement from experiment 014 against the
source recording's own transcribed top line. Sound quality is not graded.
"""
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import librosa

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SOURCE = REPO / 'experiments/005_color_purple_orchestra/data/source.wav'
sys.path.insert(0, str(REPO / 'experiments/014_yue2_excerpt_ablation/record'))
from measure import transcribe, skyline, align


def chroma(path, seconds, sr=22050):
    y, _ = librosa.load(str(path), sr=sr, mono=True, duration=seconds)
    return librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=2048)


def similarity(a, b, max_lag=10):
    n = min(a.shape[1], b.shape[1]) - 2 * max_lag
    best = -1
    for lag in range(-max_lag, max_lag + 1):
        x = a[:, max_lag:max_lag + n]
        y = b[:, max_lag + lag:max_lag + lag + n]
        assert x.shape == y.shape, (x.shape, y.shape)
        cos = np.sum(x * y, 0) / (np.linalg.norm(x, axis=0) * np.linalg.norm(y, axis=0) + 1e-9)
        best = max(best, float(np.mean(cos)))
    return best


def main():
    protocol = json.loads((ROOT / 'record/protocol.json').read_text())
    seconds = protocol['model_seconds']
    src_chroma = chroma(SOURCE, seconds)
    src_notes = skyline(transcribe(SOURCE))
    src_notes = [n for n in src_notes if n[0] < seconds]
    src_pitches = [p for _, _, p in src_notes]
    results = []
    # Self-similarity ceiling: the source against a 256k MP3 of itself.
    tmp = ROOT / 'record/source-excerpt.mp3'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(SOURCE), '-t', str(seconds), '-c:a', 'libmp3lame', '-b:a', '256k', str(tmp)], check=True)
    for label, path in [('source-mp3-ceiling', tmp)] + [(c['id'], ROOT / 'outputs' / c['id'] / 'audio.mp3') for c in protocol['conditions']]:
        if not path.exists():
            continue
        sky = skyline(transcribe(path))
        pairs = align(src_pitches, [p for _, _, p in sky])
        matched = [(i, j) for i, j in pairs if (src_pitches[i] - sky[j][2]) % 12 == 0]
        exact = [(i, j) for i, j in matched if src_pitches[i] == sky[j][2]]
        results.append(dict(label=label, chroma_similarity=similarity(src_chroma, chroma(path, seconds)),
                            source_topline_recall=len(matched) / len(src_pitches), exact_recall=len(exact) / len(src_pitches),
                            topline_precision=len(matched) / max(1, len(sky)), transcribed_topline_notes=len(sky)))
        r = results[-1]
        print(f"{label:28s} chroma {r['chroma_similarity']:.2f} recall {r['source_topline_recall']:.2f} exact {r['exact_recall']:.2f} precision {r['topline_precision']:.2f}")
    (ROOT / 'record/similarity.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
