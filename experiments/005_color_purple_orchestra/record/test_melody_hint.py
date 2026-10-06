"""Check octave interpretation, invalid inputs, and the exported MIDI event stream."""
from pathlib import Path
import struct
import tempfile
import unittest

from melody_hint import PHRASES, compile_notes, vlq, write_midi


class MelodyTests(unittest.TestCase):
    def test_user_phrases_and_transposition(self):
        events = compile_notes(PHRASES)
        self.assertEqual([e["midi"] for e in events],
                         [55, 60, 64, 57, 60, 65, 62, 64, 55, 60, 64, 57, 60, 65, 69, 67])
        self.assertEqual([e["onset_beats"] for e in events], list(range(16)))
        shifted = compile_notes(PHRASES, tonic_midi=62)
        self.assertEqual([e["midi"] for e in shifted], [e["midi"]+2 for e in events])

    def test_reject_invalid_notation_and_out_of_range_pitch(self):
        for text in ("8", "0", "do", "5_foo", "3#"):
            with self.assertRaises(ValueError):
                compile_notes([text])
        with self.assertRaises(ValueError):
            compile_notes(["1_"], tonic_midi=0)

    def test_midi_events(self):
        self.assertEqual(vlq(480), b"\x83\x60")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.mid"
            write_midi(path, compile_notes(PHRASES), 90)
            data = path.read_bytes()
        self.assertEqual(data[:14], b"MThd"+struct.pack(">IHHH", 6, 0, 1, 480))
        self.assertEqual(data[14:18], b"MTrk")
        self.assertEqual(struct.unpack(">I", data[18:22])[0], len(data)-22)
        i, tick, notes = 22, 0, []
        while i < len(data):
            delta = 0
            while True:
                byte = data[i]
                i += 1
                delta = (delta << 7) | (byte & 127)
                if byte < 128:
                    break
            tick += delta
            status = data[i]
            i += 1
            if status == 255:
                kind, length = data[i:i+2]
                i += 2
                if kind == 81:
                    self.assertEqual(int.from_bytes(data[i:i+length], "big"), 666667)
                i += length
            elif status == 192:
                i += 1
            elif status in (128, 144):
                pitch, velocity = data[i:i+2]
                i += 2
                notes.append((tick, status, pitch, velocity))
            else:
                self.fail(f"Unexpected MIDI status: {status}")
        self.assertEqual(len(notes), 32)
        self.assertEqual(notes[0], (0, 144, 55, 80))
        self.assertEqual(notes[-1], (16*480, 128, 67, 0))
        for n in range(16):
            self.assertEqual(notes[2*n+1][0]-notes[2*n][0], 480)


if __name__ == "__main__":
    unittest.main()
