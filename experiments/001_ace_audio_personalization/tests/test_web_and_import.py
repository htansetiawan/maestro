import json
import shutil
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from maestro_ace.config import ROOT, load_config
from maestro_ace.sources import import_local, merge_into_manifest, segment

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")


def _write_album(folder: Path, n: int = 2, seconds: float = 130.0) -> None:
    folder.mkdir(parents=True)
    rate = 8000
    t = np.arange(int(rate * seconds)) / rate
    for i in range(n):
        tone = 0.2 * np.sin(2 * np.pi * (200 + 40 * i + t) * t)
        sf.write(folder / f"0{i + 1} Song {i + 1}.wav", np.stack([tone, tone], axis=1), rate)


def test_import_local_decodes_to_48k_and_segments(tmp_path):
    cfg = load_config(ROOT / "configs/piano_violin.toml")
    album = tmp_path / "album"
    _write_album(album)
    metas = import_local(tmp_path, [album])
    assert [m["video_id"] for m in metas] == ["01-song-1", "02-song-2"]
    assert all(m["kind"] == "local" and m["sample_rate"] == 48000 and m["channels"] == 2
               for m in metas)
    assert metas[0]["rights"] == "unverified" and metas[0]["url"].endswith("01 Song 1.wav")
    # Re-import is idempotent; a byte-identical copy elsewhere is skipped.
    shutil.copy(album / "01 Song 1.wav", album / "copy of song 1.wav")
    assert len(import_local(tmp_path, [album])) == 2
    summary = segment(tmp_path, cfg, "01-song-1", clip_seconds=60, role="train")
    rows = [json.loads(line) for line in Path(summary["manifest"]).read_text().splitlines()]
    assert rows[0]["id"] == "loc-01-song-1-001" and rows[0]["composition_id"] == "loc-01-song-1"
    assert "Local file" in rows[0]["provenance"]


def _workbench(tmp_path: Path):
    from fastapi.testclient import TestClient

    from maestro_ace.web import create_app

    cfg_path = ROOT / "configs/piano_violin.toml"
    cfg = load_config(cfg_path)
    (tmp_path / "prompts").mkdir()
    for name in ("feedback", "eval"):
        (tmp_path / f"prompts/{name}.jsonl").write_text((ROOT / f"prompts/{name}.jsonl").read_text())
    _write_album(tmp_path / "album", n=2)
    for meta in import_local(tmp_path, [tmp_path / "album"]):
        summary = segment(tmp_path, cfg, meta["video_id"], clip_seconds=60, role="train")
        merge_into_manifest(tmp_path, cfg, Path(summary["manifest"]))
    return TestClient(create_app(tmp_path, cfg_path, token="secret"))


def test_workbench_requires_token_then_edits_manifest(tmp_path):
    client = _workbench(tmp_path)
    assert client.get("/api/state").status_code == 401
    locked = client.get("/")
    assert locked.status_code == 200 and "private" in locked.text and "og:image" in locked.text
    assert "dataset workbench" in locked.text and "api/state" not in locked.text
    card = client.get("/og-card.png")
    assert card.status_code == 200 and card.headers["content-type"] == "image/png"
    assert client.get("/favicon.ico").status_code == 200
    first = client.get("/?token=secret", follow_redirects=False)
    assert first.status_code in (302, 307) and "maestro_web" in first.headers.get("set-cookie", "")
    client.cookies.set("maestro_web", "secret")
    page = client.get("/")
    assert page.status_code == 200 and "dataset workbench" in page.text
    state = client.get("/api/state").json()
    assert state["progress"]["total"] == 6 and state["progress"]["todo"] == 6
    assert state["readiness"]["ok"] is False and "caption" in state["readiness"]["message"]
    assert {s["kind"] for s in state["sources"]} == {"local"}

    clip = state["clips"][0]["id"]
    audio = client.get(f"/api/audio/{clip}", headers={"Range": "bytes=0-99"})
    assert audio.status_code in (200, 206) and len(audio.content) >= 100
    bad = client.post(f"/api/clip/{clip}", json={"caption": "TODO still"})
    assert bad.status_code == 400
    ok = client.post(f"/api/clip/{clip}", json={
        "caption": "Solo piano, slow arpeggios, warm and quiet, a long crescendo.",
        "bpm": 72, "keyscale": "Eb major", "timesignature": "4",
        "instruments": ["piano"], "role": "train"})
    assert ok.status_code == 200 and ok.json()["todo"] is False and ok.json()["bpm"] == 72
    assert client.get("/api/state").json()["progress"]["todo"] == 5
    gone = client.delete(f"/api/clip/{state['clips'][1]['id']}")
    assert gone.status_code == 200 and gone.json()["remaining"] == 5
    assert client.delete("/api/clip/nope").status_code == 404
    assert client.get("/api/audio/nope").status_code == 404
