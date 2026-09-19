import json
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from maestro_ace.config import ROOT, load_config
from maestro_ace.data import prepare, validate_recordings
from maestro_ace.io import file_hash
from maestro_ace.sources import (
    SOURCES_DIR,
    merge_into_manifest,
    plan_windows,
    segment,
    video_id,
)


def test_video_id_accepts_urls_and_bare_ids():
    assert video_id("https://www.youtube.com/watch?v=q-73jqLVu3Y") == "q-73jqLVu3Y"
    assert video_id("https://youtu.be/q-73jqLVu3Y?t=12") == "q-73jqLVu3Y"
    assert video_id("q-73jqLVu3Y") == "q-73jqLVu3Y"
    with pytest.raises(ValueError):
        video_id("https://example.com/not-a-video")


def test_plan_windows_trims_silence_and_keeps_tail_over_minimum():
    hop = 0.1
    env = np.zeros(int(300 / hop))          # 300 s of silence
    env[int(20 / hop):int(230 / hop)] = 0.2  # music from 20 s to 230 s
    windows = plan_windows(env, hop, clip_seconds=90, min_seconds=10)
    assert windows == [(20.0, 110.0), (110.0, 200.0), (200.0, 230.0)]
    # A 5 s tail is below min_seconds and is dropped.
    env[:] = 0
    env[int(20 / hop):int(115 / hop)] = 0.2
    assert plan_windows(env, hop, clip_seconds=90, min_seconds=10) == [(20.0, 110.0)]
    # Overlap steps by clip - overlap.
    env[:] = 0
    env[0:int(200 / hop)] = 0.2
    assert plan_windows(env, hop, 90, 10, overlap_seconds=30)[:2] == [(0.0, 90.0), (60.0, 150.0)]


def test_plan_windows_drops_mostly_silent_windows_and_respects_region():
    hop = 0.1
    env = np.zeros(int(400 / hop))
    env[0:int(90 / hop)] = 0.2              # 90 s of music
    env[int(90 / hop):int(180 / hop)] = 0.0  # 90 s of applause-free silence
    env[int(180 / hop):int(270 / hop)] = 0.2
    windows = plan_windows(env, hop, 90, 10)
    assert (90.0, 180.0) not in windows and (0.0, 90.0) in windows
    assert plan_windows(env, hop, 90, 10, region=(180.0, 270.0)) == [(180.0, 270.0)]


def _fake_source(root: Path, vid: str, seconds: float, rights: str = "unverified",
                 chapters=None) -> Path:
    folder = root / SOURCES_DIR / vid
    folder.mkdir(parents=True)
    rate = 8000
    t = np.arange(int(rate * seconds)) / rate
    # A slow sweep so that no two clips are byte-identical (the manifest rejects duplicates).
    base = 220 + 10 * (sum(map(ord, vid)) % 7)  # distinct content per fake video
    tone = 0.2 * np.sin(2 * np.pi * (base + 2 * t) * t)
    tone[: rate * 5] = 0  # leading silence
    audio = folder / "audio.wav"
    sf.write(audio, np.stack([tone, tone], axis=1), rate)
    meta = {"video_id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
            "title": "Test Concert", "uploader": "Channel", "upload_date": "20200101",
            "platform_license": "", "rights": rights, "duration": seconds,
            "sample_rate": rate, "channels": 2, "chapters": chapters or [],
            "audio_path": str(audio), "audio_sha256": file_hash(audio), "video_path": None,
            "fetched_at": "2026-09-19T00:00:00+00:00", "downloader": "yt-dlp test"}
    (folder / "source.json").write_text(json.dumps(meta))
    return folder


def _prompts(root: Path):
    (root / "prompts").mkdir(exist_ok=True)
    for name in ("feedback", "eval"):
        (root / f"prompts/{name}.jsonl").write_text((ROOT / f"prompts/{name}.jsonl").read_text())


def test_segment_writes_reference_rows_that_never_train(tmp_path):
    cfg = load_config(ROOT / "configs/piano_violin.toml")
    _prompts(tmp_path)
    _fake_source(tmp_path, "abcdefghijk", seconds=125)
    summary = segment(tmp_path, cfg, "abcdefghijk", clip_seconds=60)
    assert summary["clips"] == 2  # 5 s silence trimmed; 120 s of music -> 60 + 60
    rows = [json.loads(line) for line in Path(summary["manifest"]).read_text().splitlines()]
    assert rows[0]["id"] == "yt-abcdefghijk-001"
    assert rows[0]["composition_id"] == "yt-abcdefghijk"
    assert rows[0]["role"] == "reference" and rows[0]["rights"] == "unverified"
    assert rows[0]["source_start"] == 5.0 and rows[0]["source_end"] == 65.0
    assert "TODO" in rows[0]["caption"] and "youtube.com" in rows[0]["provenance"]
    assert sf.info(tmp_path / rows[0]["audio_path"]).duration == pytest.approx(60, abs=0.01)

    # Two own compositions plus the reference clips: prepare stages the reference
    # material separately and keeps it out of both training splits.
    (tmp_path / "data/audio").mkdir(parents=True, exist_ok=True)
    own = []
    for ident in ("a", "b"):
        t = np.arange(8000 * 11) / 8000
        sf.write(tmp_path / f"data/audio/{ident}.wav",
                 0.15 * np.sin(2 * np.pi * (300 if ident == "a" else 400) * t), 8000)
        own.append({"id": ident, "composition_id": ident, "audio_path": f"data/audio/{ident}.wav",
                    "caption": "Original solo piano sketch with a lyrical melody.",
                    "instruments": ["piano"], "provenance": "Original performance by Henry."})
    manifest = tmp_path / cfg.data.manifest
    manifest.write_text("".join(json.dumps(r) + "\n" for r in own))
    merged = merge_into_manifest(tmp_path, cfg, Path(summary["manifest"]))
    assert merged == {"manifest": str(manifest), "existing": 2, "added": 2, "skipped": 0}
    assert merge_into_manifest(tmp_path, cfg, Path(summary["manifest"]))["skipped"] == 2

    result = prepare(tmp_path, cfg, tmp_path / "artifacts/prepared")
    assert result["reference"] == 2 and result["train"] + result["validation"] == 2
    prepared = tmp_path / "artifacts/prepared"
    for split in ("train", "validation"):
        samples = json.loads((prepared / f"{split}.json").read_text())["samples"]
        assert not any("yt-" in s["audio_path"] for s in samples)
    reference = json.loads((prepared / "reference.json").read_text())["samples"]
    assert len(reference) == 2 and all("yt-abcdefghijk" in s["audio_path"] for s in reference)


def test_train_role_on_unverified_rights_requires_opt_in(tmp_path):
    cfg = load_config(ROOT / "configs/piano_violin.toml").model_copy(deep=True)
    cfg.data.allow_unverified_rights = False  # test the gate regardless of the live config
    _prompts(tmp_path)
    _fake_source(tmp_path, "abcdefghijk", seconds=125)
    _fake_source(tmp_path, "lmnopqrstuv", seconds=125)
    for vid in ("abcdefghijk", "lmnopqrstuv"):
        summary = segment(tmp_path, cfg, vid, clip_seconds=60, role="train")
        merge_into_manifest(tmp_path, cfg, Path(summary["manifest"]))
    with pytest.raises(ValueError, match="finish the caption"):
        validate_recordings(tmp_path, cfg)
    manifest = tmp_path / cfg.data.manifest
    rows = [json.loads(line) for line in manifest.read_text().splitlines()]
    for row in rows:
        row["caption"] = "Live solo piano ballad with sustained chords and a singing melody."
    manifest.write_text("".join(json.dumps(r) + "\n" for r in rows))
    with pytest.raises(ValueError, match="rights are unverified"):
        validate_recordings(tmp_path, cfg)
    opted = cfg.model_copy(deep=True)
    opted.data.allow_unverified_rights = True
    assert len(validate_recordings(tmp_path, opted)) == 4


def test_segment_by_chapters(tmp_path):
    cfg = load_config(ROOT / "configs/piano_violin.toml")
    chapters = [{"title": "Song One", "start": 5.0, "end": 65.0},
                {"title": "Song Two", "start": 65.0, "end": 125.0}]
    _fake_source(tmp_path, "abcdefghijk", seconds=125, chapters=chapters)
    summary = segment(tmp_path, cfg, "abcdefghijk", clip_seconds=120, use_chapters=True)
    rows = [json.loads(line) for line in Path(summary["manifest"]).read_text().splitlines()]
    assert [(r["source_start"], r["source_end"]) for r in rows] == [(5.0, 65.0), (65.0, 125.0)]
    assert "chapter: Song Two" in rows[1]["caption"]


def test_find_tracks_splits_at_gaps_and_merges_short_pieces():
    from maestro_ace.sources import find_tracks

    hop = 0.1
    env = np.zeros(int(700 / hop))
    env[int(1 / hop):int(220 / hop)] = 0.2      # song 1
    env[int(221 / hop):int(470 / hop)] = 0.2    # song 2 (1 s gap before)
    env[int(474 / hop):int(500 / hop)] = 0.2    # 26 s fragment -> merged into song 3
    env[int(500.5 / hop):int(680 / hop)] = 0.2  # song 3
    tracks = find_tracks(env, hop, gap_db=-35, min_gap_seconds=0.3, min_track_seconds=90)
    assert tracks == [(1.0, 220.0), (221.0, 470.0), (474.0, 680.0)]
    # A 0.2 s dip is not a gap.
    env[int(100 / hop):int(100.2 / hop)] = 0
    assert find_tracks(env, hop, min_gap_seconds=0.3)[0] == (1.0, 220.0)


def test_segment_tracks_gives_each_song_its_own_composition_and_caption_updates(tmp_path):
    from maestro_ace.sources import pending_captions, set_caption

    cfg = load_config(ROOT / "configs/piano_violin.toml")
    _prompts(tmp_path)
    folder = _fake_source(tmp_path, "abcdefghijk", seconds=260)
    rate = 8000
    audio, _ = sf.read(folder / "audio.wav")
    audio[int(130 * rate):int(131 * rate)] = 0  # one-second gap between two songs
    sf.write(folder / "audio.wav", audio, rate)
    meta = json.loads((folder / "source.json").read_text())
    meta["audio_sha256"] = file_hash(folder / "audio.wav")
    (folder / "source.json").write_text(json.dumps(meta))
    summary = segment(tmp_path, cfg, "abcdefghijk", clip_seconds=60, role="train",
                      use_tracks=True, min_track_seconds=60)
    assert summary["compositions"] == 2
    rows = [json.loads(line) for line in Path(summary["manifest"]).read_text().splitlines()]
    assert {r["composition_id"] for r in rows} == {"yt-abcdefghijk-t01", "yt-abcdefghijk-t02"}
    assert all(r["source_end"] <= 130.0 for r in rows if r["composition_id"].endswith("t01"))
    merge_into_manifest(tmp_path, cfg, Path(summary["manifest"]))
    assert len(pending_captions(tmp_path, cfg)) == len(rows)
    with pytest.raises(ValueError, match="TODO"):
        set_caption(tmp_path, cfg, rows[0]["id"], text="TODO later")
    row = set_caption(tmp_path, cfg, rows[0]["id"],
                      text="Pop ballad duet, male and female vocals over piano and strings.",
                      bpm=72, keyscale="Db major", instruments=["vocals", "piano", "strings"])
    assert row["bpm"] == 72 and row["instruments"] == ["vocals", "piano", "strings"]
    assert len(pending_captions(tmp_path, cfg)) == len(rows) - 1
    with pytest.raises(KeyError):
        set_caption(tmp_path, cfg, "nope", text="Solo piano with a lyrical melody line.")
