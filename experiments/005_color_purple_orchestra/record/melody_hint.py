"""Compile the user's scale degrees into inspectable note events, MIDI, and guide audio.

This small demonstration is not ACE-Step generation or a full Jianpu parser.
An underscore lowers a scale degree by one octave; spaces separate quarter notes.
"""
import json
from pathlib import Path
import re
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PHRASES = ["5_ 1 3 6_ 1 4 2 3", "5_ 1 3 6_ 1 4 6 5"]
MAJOR = [0, 2, 4, 5, 7, 9, 11]


def compile_notes(phrases, tonic_midi=60):
    events = []
    for phrase, text in enumerate(phrases):
        for token in text.split():
            match = re.fullmatch(r"([1-7])(_*)", token)
            if match is None:
                raise ValueError(f"Unsupported degree token: {token}")
            degree, lowers = int(match[1]), len(match[2])
            pitch = tonic_midi + MAJOR[degree-1] - 12*lowers
            if not 0 <= pitch <= 127:
                raise ValueError(f"Pitch outside MIDI range: {pitch}")
            events.append(dict(token=token, degree=degree, octave_offset=-lowers,
                               midi=pitch, onset_beats=len(events), duration_beats=1,
                               phrase=phrase+1))
    return events


def vlq(value):
    encoded = [value & 127]
    while value >> 7:
        value >>= 7
        encoded.insert(0, (value & 127) | 128)
    return bytes(encoded)


def write_midi(path, events, bpm):
    tempo = round(60_000_000 / bpm)
    track = b"\x00\xff\x51\x03" + tempo.to_bytes(3, "big")
    track += b"\x00\xff\x58\x04\x04\x02\x18\x08\x00\xc0\x00"
    for event in events:
        track += b"\x00\x90" + bytes([event["midi"], 80])
        track += vlq(480 * event["duration_beats"]) + b"\x80" + bytes([event["midi"], 0])
    track += b"\x00\xff\x2f\x00"
    path.write_bytes(b"MThd" + struct.pack(">IHHH", 6, 0, 1, 480)
                     + b"MTrk" + struct.pack(">I", len(track)) + track)


def main():
    import numpy as np
    import soundfile as sf
    out = ROOT / "melody-demo"
    out.mkdir(exist_ok=False)
    bpm, sample_rate = 90, 48000
    events = compile_notes(PHRASES)
    metadata = dict(notation=PHRASES, tonic="C4", tonic_midi=60, scale="major", bpm=bpm,
                    meter="4/4", assumptions="Every token is one quarter note; no inferred rhythm or rests.",
                    audio_kind="Deterministic additive-synth guide; not an ACE output or piano performance.",
                    used_in_orchestral_generation=False, events=events)
    (out / "notes.json").write_text(json.dumps(metadata, indent=2) + "\n")
    write_midi(out / "melody.mid", events, bpm)
    seconds_per_beat = 60 / bpm
    wave = np.zeros(round((len(events)*seconds_per_beat+.3)*sample_rate), dtype="float32")
    note_samples = round(seconds_per_beat*.9*sample_rate)
    t = np.arange(note_samples) / sample_rate
    envelope = np.minimum(t/.012, 1) * np.minimum((t[-1]-t)/.04, 1) * np.exp(-2*t)
    for event in events:
        hz = 440 * 2**((event["midi"]-69)/12)
        note = (np.sin(2*np.pi*hz*t) + .2*np.sin(4*np.pi*hz*t)) * envelope * .3
        start = round(event["onset_beats"]*seconds_per_beat*sample_rate)
        wave[start:start+note_samples] += note.astype("float32")
    wav = out / "melody-guide.wav"
    sf.write(wav, wave, sample_rate, subtype="PCM_24")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(wav),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(out / "melody-guide.mp3")], check=True)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
