"""Render a MIDI file to MP3 with a deterministic additive 'piano-like' synth (no soundfont needed)."""
import subprocess, sys
from pathlib import Path
import numpy as np
import pretty_midi

SR = 48000


def render(midi_path, out_mp3, gain=0.5):
    pm = pretty_midi.PrettyMIDI(str(midi_path))
    total = pm.get_end_time() + 1.5
    buf = np.zeros(int(total * SR) + 1, dtype=np.float64)
    for inst in pm.instruments:
        for n in inst.notes:
            dur = max(0.05, n.end - n.start)
            t = np.arange(int((dur + 0.6) * SR)) / SR
            f = 440.0 * 2 ** ((n.pitch - 69) / 12)
            env = np.exp(-t * 3.0) * (1 - np.exp(-t * 400))
            env[t > dur] *= np.exp(-(t[t > dur] - dur) * 12)
            tone = sum((0.6 ** k) * np.sin(2 * np.pi * f * (k + 1) * t) for k in range(5) if f * (k + 1) < SR / 2)
            vel = (n.velocity / 127) ** 1.5
            s = int(n.start * SR)
            seg = tone * env * vel
            buf[s:s + len(seg)] += seg[:len(buf) - s]
    buf *= gain / max(1e-6, np.abs(buf).max())
    raw = (buf * 32767).astype(np.int16).tobytes()
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-',
                    '-c:a', 'libmp3lame', '-b:a', '192k', str(out_mp3)], input=raw, check=True)


if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2])
