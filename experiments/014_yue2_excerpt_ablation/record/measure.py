"""Measure how much of a reference melody is audible in a piano recording.

Pipeline: audio -> ByteDance piano transcription (CPU) -> skyline (highest note
per onset cluster) -> global sequence alignment against the reference melody
(pitch match, gaps allowed) -> recall, precision, octave errors, tempo ratio,
onset deviation. A high score means the top line follows the score; it does
not grade sound quality, voicing, or harmony. Transcription errors count
against the audio, so the same measurement on the human recording is the ceiling.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys

import numpy as np


def transcribe(path, sr=16000):
    import librosa
    from piano_transcription_inference import PianoTranscription, sample_rate
    audio, _ = librosa.load(str(path), sr=sample_rate, mono=True)
    model = PianoTranscription(device=__import__('os').environ.get('MEASURE_DEVICE', 'cpu'), checkpoint_path=None)
    result = model.transcribe(audio, None)
    notes = [(n['onset_time'], n['offset_time'], int(n['midi_note']), n['velocity']) for n in result['est_note_events']]
    return sorted(notes)


def skyline(notes, window=0.06):
    """Highest-pitched note among onsets within `window` seconds of each other."""
    out, i = [], 0
    while i < len(notes):
        j = i
        while j + 1 < len(notes) and notes[j + 1][0] - notes[i][0] <= window:
            j += 1
        cluster = notes[i:j + 1]
        top = max(cluster, key=lambda n: n[2])
        out.append((top[0], top[1], top[2]))
        i = j + 1
    return out


def align(reference, candidate, gap=-1.0):
    """Needleman-Wunsch on pitch sequences. match=+2 exact, +1 octave-equivalent, mismatch=-2."""
    n, m = len(reference), len(candidate)
    score = np.zeros((n + 1, m + 1)); back = np.zeros((n + 1, m + 1), dtype=np.int8)
    score[:, 0] = np.arange(n + 1) * gap; score[0, :] = np.arange(m + 1) * gap
    back[1:, 0] = 1; back[0, 1:] = 2
    for i in range(1, n + 1):
        rp = reference[i - 1]
        for j in range(1, m + 1):
            cp = candidate[j - 1]
            s = 2 if rp == cp else (1 if (rp - cp) % 12 == 0 else -2)
            options = (score[i - 1, j - 1] + s, score[i - 1, j] + gap, score[i, j - 1] + gap)
            k = int(np.argmax(options)); score[i, j] = options[k]; back[i, j] = k
    pairs, i, j = [], n, m
    while i > 0 or j > 0:
        k = back[i, j]
        if k == 0:
            pairs.append((i - 1, j - 1)); i -= 1; j -= 1
        elif k == 1:
            i -= 1
        else:
            j -= 1
    return pairs[::-1]


def measure(reference_notes, bpm, audio_path, label, start_offset=0.0):
    """reference_notes: [(quarter onset, quarter duration, midi)]"""
    ref = [(float(t) * 60 / bpm, p) for t, _, p in reference_notes]
    raw = transcribe(audio_path)
    sky = skyline(raw)
    pairs = align([p for _, p in ref], [p for _, _, p in sky])
    exact = [(i, j) for i, j in pairs if ref[i][1] == sky[j][2]]
    octave = [(i, j) for i, j in pairs if ref[i][1] != sky[j][2] and (ref[i][1] - sky[j][2]) % 12 == 0]
    matched = exact + octave
    tempo_ratio = onset_rms = None
    if len(matched) >= 4:
        x = np.array([ref[i][0] for i, _ in matched]); y = np.array([sky[j][0] for _, j in matched])
        slope, intercept = np.polyfit(x, y, 1)
        tempo_ratio = float(slope)                 # >1: the audio is slower than the score tempo
        onset_rms = float(np.sqrt(np.mean((y - (slope * x + intercept)) ** 2)))
    return dict(label=label, audio=str(audio_path), reference_notes=len(ref), transcribed_notes=len(raw),
                skyline_notes=len(sky), exact_pitch_matches=len(exact), octave_matches=len(octave),
                melody_recall=len(matched) / len(ref), exact_recall=len(exact) / len(ref),
                skyline_precision=len(matched) / max(1, len(sky)),
                tempo_ratio=tempo_ratio, aligned_onset_rms_seconds=onset_rms,
                longest_exact_run=longest_run(sorted(i for i, _ in exact)),
                method='ByteDance piano_transcription_inference (CPU) -> skyline -> global pitch alignment')


def longest_run(indices):
    best = run = 0
    for a, b in zip(indices, indices[1:]):
        run = run + 1 if b == a + 1 else 0
        best = max(best, run)
    return best + 1 if indices else 0


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--events', required=True, help='JSON with melody [[onset, dur, midi]...] and bpm')
    cli.add_argument('--audio', required=True, nargs='+')
    cli.add_argument('--labels', nargs='*')
    cli.add_argument('--output', required=True)
    cli.add_argument('--melody-key', default='melody')
    args = cli.parse_args()
    events = json.loads(Path(args.events).read_text())
    melody = [(F(t), F(d), p) for t, d, p in events[args.melody_key]]
    labels = args.labels or [Path(a).parent.name for a in args.audio]
    results = [measure(melody, events['bpm'], Path(a), l) for a, l in zip(args.audio, labels)]
    Path(args.output).write_text(json.dumps(results, indent=2) + '\n')
    for r in results:
        print(f"{r['label']:32s} recall {r['melody_recall']:.2f} exact {r['exact_recall']:.2f} "
              f"precision {r['skyline_precision']:.2f} tempo x{(r['tempo_ratio'] or float('nan')):.2f} "
              f"run {r['longest_exact_run']}")


if __name__ == '__main__':
    main()
