"""Chroma similarity (015 method) of each clip to the audio it was conditioned on.

MusicGen clips: against the guide or recording they were conditioned on, first
30 s; the text-only clip against the Color Purple guide as a floor. EnCodec
round trips: against the recording itself, first 46 s.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT.parent
import librosa
import numpy as np

# copied from 015/record/measure.py (its module name collides with 014's)
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




CP_GUIDE = EXP / '014_yue2_excerpt_ablation/inputs/melody-guide.mp3'
CP_REC = EXP / '005_color_purple_orchestra/data/source.wav'
SHE_GUIDE = EXP / '016_she_sheet_to_voice/inputs/melody-guide.mp3'
pairs = [('cp-guide', CP_GUIDE, 30), ('cp-recording', CP_REC, 30), ('cp-text-only', CP_GUIDE, 30), ('she-guide', SHE_GUIDE, 30)]
pairs += [(f'encodec24-{b}kbps', CP_REC, 46) for b in ('1.5', '3', '6', '12', '24')] + [('encodec32-musicgen', CP_REC, 46)]
pairs += [('guide-vs-recording', CP_GUIDE, 30)]  # how similar the synthesized guide is to the recording: a reference point
out = {}
for cond, ref, secs in pairs:
    clip = CP_REC if cond == 'guide-vs-recording' else ROOT / 'outputs' / cond / 'audio.mp3'
    out[cond] = similarity(chroma(ref, secs), chroma(clip, secs))
    print(f'{cond:22s} chroma {out[cond]:.2f}')
(ROOT / 'outputs/chroma.json').write_text(json.dumps(out, indent=1) + '\n')
