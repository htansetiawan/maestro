import json

import numpy as np
import pytest
import soundfile as sf

pytest.importorskip("librosa")

from maestro_ace.autolabel import (  # noqa: E402
    autolabel,
    draft_caption,
    estimate_key,
    estimate_sections,
    estimate_tempo,
    summarise_tags,
)
from maestro_ace.config import ROOT, load_config  # noqa: E402


def _piano_like(seconds: float = 40.0, sr: int = 22050, bpm: float = 80.0) -> np.ndarray:
    """C major arpeggio pulses at a steady tempo, louder in the middle third."""
    t = np.arange(int(sr * seconds)) / sr
    y = np.zeros_like(t)
    beat = 60.0 / bpm
    notes = [261.63, 329.63, 392.00, 523.25]  # C E G C
    for i in range(int(seconds / beat)):
        start = int(i * beat * sr)
        n = int(beat * sr * 0.9)
        seg = t[:n]
        env = np.exp(-3 * seg)
        f = notes[i % 4]
        y[start:start + n] += env * (np.sin(2 * np.pi * f * seg) + 0.3 * np.sin(4 * np.pi * f * seg))
    third = len(y) // 3
    y[third:2 * third] *= 2.2
    return (0.2 * y / np.abs(y).max()).astype(np.float32)


def test_key_and_tempo_on_synthetic_arpeggio():
    y = _piano_like()
    key = estimate_key(y, 22050)
    assert key["keyscale"] in ("C major", "A minor")
    tempo = estimate_tempo(y, 22050)
    assert 70 <= tempo["bpm"] <= 90 or 140 <= tempo["bpm"] * 2 <= 180


def test_sections_cover_duration_and_mark_loud_middle():
    y = _piano_like(seconds=60)
    sections = estimate_sections(y, 22050, 60.0)
    assert sections[0]["start"] == 0.0 and abs(sections[-1]["end"] - 60.0) < 1.0
    loudest = max(sections, key=lambda s: s["level_db"])
    assert 15 < loudest["start"] < 45


def test_caption_template_is_deterministic_and_uses_vocabulary():
    tags = summarise_tags({"windows": [
        {"start": 0.0, "probs": {"piano": 0.7, "strings": 0.05, "drums": 0.05}},
        {"start": 10.0, "probs": {"piano": 0.5, "strings": 0.3, "drums": 0.05}},
        {"start": 20.0, "probs": {"piano": 0.4, "strings": 0.3, "drums": 0.2}},
        {"start": 30.0, "probs": {"piano": 0.4, "strings": 0.3, "drums": 0.2}},
    ]})
    assert tags["instruments"] == ["piano", "strings", "drums"] and tags["vocals"] == []
    assert tags["first_seen"]["strings"] == 10.0 and tags["first_seen"]["drums"] == 20.0
    analysis = {"tempo": {"bpm": 72}, "key": {"keyscale": "Eb major"}, "tags": tags,
                "sections": [{"start": 0, "end": 30, "level_db": -12, "dynamics": "quiet"},
                             {"start": 30, "end": 60, "level_db": -2, "dynamics": "full"},
                             {"start": 60, "end": 90, "level_db": -10, "dynamics": "quiet"}]}
    caption = draft_caption(analysis)
    assert caption == draft_caption(analysis)
    assert caption.startswith("Instrumental piece led by piano with strings, drums.")
    assert "Drums from 0:20" in caption and "builds to a full peak around 0:30" in caption
    assert caption.endswith("Slow tempo, 72 BPM, Eb major.")
    vocal = summarise_tags({"windows": [
        {"start": 0.0, "probs": {"piano": 0.5, "female vocals": 0.4}},
        {"start": 10.0, "probs": {"piano": 0.5, "female vocals": 0.4}}]})
    assert vocal["vocals"] == ["female vocals"]
    assert draft_caption({**analysis, "tags": vocal}).startswith("Pop ballad with female vocals, piano lead.")


def test_autolabel_writes_drafts_and_keeps_human_captions(tmp_path):
    cfg = load_config(ROOT / "configs/piano_violin.toml")
    (tmp_path / "data/audio").mkdir(parents=True)
    y = _piano_like(seconds=40)
    sf.write(tmp_path / "data/audio/a.wav", np.stack([y, y], axis=1), 22050)
    sf.write(tmp_path / "data/audio/b.wav", np.stack([y * 0.8, y * 0.8], axis=1), 22050)
    rows = [{"id": "a", "composition_id": "a", "audio_path": "data/audio/a.wav",
             "caption": "TODO: describe what is audible in this clip.", "instruments": ["piano"],
             "provenance": "synthetic test audio for autolabel"},
            {"id": "b", "composition_id": "b", "audio_path": "data/audio/b.wav",
             "caption": "Human wrote this one already, keep it.", "instruments": ["piano"],
             "provenance": "synthetic test audio for autolabel"}]
    manifest = tmp_path / cfg.data.manifest
    manifest.write_text("".join(json.dumps(r) + "\n" for r in rows))
    result = autolabel(tmp_path, cfg, use_clap=False, log=lambda *_: None)
    assert result == {"labelled": ["a"], "skipped_human": ["b"]}
    updated = {r["id"]: r for r in (json.loads(line) for line in manifest.read_text().splitlines())}
    assert updated["a"]["caption"].startswith("TODO: Instrumental piece led by piano")
    assert updated["a"]["bpm"] > 0 and updated["a"]["keyscale"] and updated["a"]["timesignature"] == "4"
    assert updated["b"]["caption"] == "Human wrote this one already, keep it."
    assert (tmp_path / "data/analysis/a.json").is_file()
    assert not (tmp_path / "data/analysis/b.json").exists()
