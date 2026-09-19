"""External audio sources: fetch YouTube audio/video, cut it into clips, draft manifest rows.

Everything downloaded lands under the ignored ``data/sources/`` tree with a sidecar
``source.json`` recording the URL, title, uploader, upload date, licence as reported by
the platform, the downloader version and the fetch time. Clips inherit that provenance.

Nothing here decides whether the material may be trained on. Every clip row is written
with ``rights = "unverified"`` (or ``"cc"`` when the platform reports a Creative Commons
licence) and ``role = "reference"`` unless the caller asks for ``--role train``. The
training gate lives in :func:`maestro_ace.data.validate_recordings`.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import shutil
from pathlib import Path

import numpy as np
import soundfile as sf

from .config import Config
from .io import file_hash, read_jsonl, write_json, write_jsonl

SOURCES_DIR = Path("data/sources/youtube")
LOCAL_DIR = Path("data/sources/local")
TARGET_SAMPLE_RATE = 48000
AUDIO_SUFFIXES = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".opus", ".aiff", ".aif"}
PREFIX = {"youtube": "yt", "local": "loc"}
YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


# --------------------------------------------------------------------------- fetch


def video_id(url_or_id: str) -> str:
    """Return the 11-character YouTube ID for a URL or a bare ID."""
    candidate = url_or_id.strip()
    if YOUTUBE_ID.match(candidate) and "/" not in candidate and "." not in candidate:
        return candidate
    for pattern in (r"[?&]v=([A-Za-z0-9_-]{11})", r"youtu\.be/([A-Za-z0-9_-]{11})",
                    r"/shorts/([A-Za-z0-9_-]{11})", r"/live/([A-Za-z0-9_-]{11})",
                    r"/embed/([A-Za-z0-9_-]{11})"):
        match = re.search(pattern, candidate)
        if match:
            return match.group(1)
    raise ValueError(f"Could not read a YouTube video ID from: {url_or_id}")


def source_dir(root: Path, sid: str) -> Path:
    """Folder of a fetched (YouTube) or imported (local) source; YouTube wins if both exist."""
    for base in (SOURCES_DIR, LOCAL_DIR):
        if (root / base / sid / "source.json").is_file():
            return root / base / sid
    return root / SOURCES_DIR / sid


def require_ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe are required (apt install ffmpeg)")
    return path


def _ytdlp():
    try:
        import yt_dlp
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("Install the downloader: uv sync --extra youtube") from exc
    return yt_dlp


def _licence_from_info(info: dict) -> str:
    text = " ".join(str(info.get(key) or "") for key in ("license", "licence")).lower()
    return "cc" if "creative commons" in text else "unverified"


def fetch(root: Path, url: str, keep_video: bool = False, overwrite: bool = False) -> dict:
    """Download one YouTube video's audio as 48 kHz stereo WAV (and optionally the video).

    Returns the sidecar metadata that was written to ``source.json``.
    """
    require_ffmpeg()
    yt_dlp = _ytdlp()
    vid = video_id(url)
    folder = source_dir(root, vid)
    sidecar = folder / "source.json"
    if sidecar.is_file() and not overwrite:
        meta = json.loads(sidecar.read_text())
        if Path(meta["audio_path"]).is_file():
            print(f"Already fetched {vid}: {meta['title']!r}; use --overwrite to refetch")
            return meta
    folder.mkdir(parents=True, exist_ok=True)
    canonical = f"https://www.youtube.com/watch?v={vid}"
    audio_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(folder / "audio.%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
        "postprocessor_args": {"ffmpegextractaudio": ["-ar", str(TARGET_SAMPLE_RATE), "-ac", "2"]},
        "noplaylist": True, "quiet": True, "noprogress": True, "no_warnings": True,
        "overwrites": True, "writeinfojson": False,
    }
    with yt_dlp.YoutubeDL(audio_opts) as ydl:
        info = ydl.extract_info(canonical, download=True)
    audio_path = folder / "audio.wav"
    if not audio_path.is_file():
        raise RuntimeError(f"Downloader finished but {audio_path} is missing")
    video_path = None
    if keep_video:
        video_opts = {
            "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
            "merge_output_format": "mp4",
            "outtmpl": str(folder / "video.%(ext)s"),
            "noplaylist": True, "quiet": True, "noprogress": True, "no_warnings": True,
            "overwrites": True,
        }
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.extract_info(canonical, download=True)
        candidates = sorted(folder.glob("video.*"))
        video_path = str(candidates[0]) if candidates else None
    audio_info = sf.info(audio_path)
    span = audible_span(audio_path)
    if span["audible_seconds"] < 0.9 * audio_info.duration:
        print(f"WARNING {vid}: only {span['audible_seconds']:.0f} of {audio_info.duration:.0f} s "
              f"are audible (last sound at {span['audible_end']} s); the source may be muted "
              "part-way through. Segmenting skips silent windows.")
    chapters = [{"title": c.get("title", ""), "start": float(c["start_time"]),
                 "end": float(c["end_time"])} for c in (info.get("chapters") or [])
                if c.get("start_time") is not None and c.get("end_time") is not None]
    meta = {
        "kind": "youtube", "video_id": vid, "url": canonical, "title": info.get("title", ""),
        "uploader": info.get("uploader") or info.get("channel") or "",
        "channel_url": info.get("channel_url") or info.get("uploader_url") or "",
        "upload_date": info.get("upload_date", ""),
        "platform_license": info.get("license") or "",
        "rights": _licence_from_info(info),
        "duration": audio_info.duration, "sample_rate": audio_info.samplerate,
        "channels": audio_info.channels, **span, "chapters": chapters,
        "audio_path": str(audio_path), "audio_sha256": file_hash(audio_path),
        "video_path": video_path,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "downloader": f"yt-dlp {yt_dlp.version.__version__}",
        "description": (info.get("description") or "")[:2000],
    }
    write_json(sidecar, meta)
    return meta


# --------------------------------------------------------------------------- segment


def _envelope(path: Path, hop_seconds: float = 0.1) -> tuple[np.ndarray, int]:
    """Per-hop RMS envelope of a file, read in blocks so long sources do not load whole."""
    info = sf.info(path)
    hop = int(info.samplerate * hop_seconds)
    values = []
    with sf.SoundFile(path) as handle:
        for block in handle.blocks(blocksize=hop, dtype="float32", always_2d=True):
            values.append(float(np.sqrt(np.mean(np.square(block)))) if block.size else 0.0)
    return np.asarray(values, dtype=np.float64), hop


def audible_span(path: Path, silence_db: float = -45.0) -> dict:
    """Seconds of audible material and where it starts/stops. Flags muted tails.

    Compilations on video platforms are sometimes muted part-way through by rights
    claims; the file keeps its full length but carries digital silence afterwards.
    """
    envelope, hop = _envelope(path)
    hop_seconds = hop / sf.info(path).samplerate
    if envelope.size == 0 or envelope.max() <= 0:
        return {"audible_seconds": 0.0, "audible_start": None, "audible_end": None}
    active = envelope > envelope.max() * (10 ** (silence_db / 20))
    idx = np.flatnonzero(active)
    return {"audible_seconds": round(float(active.sum()) * hop_seconds, 1),
            "audible_start": round(float(idx[0]) * hop_seconds, 1),
            "audible_end": round(float(idx[-1] + 1) * hop_seconds, 1)}


def find_tracks(envelope: np.ndarray, hop_seconds: float, gap_db: float = -35.0,
                min_gap_seconds: float = 0.3, min_track_seconds: float = 90.0,
                region: tuple[float, float] | None = None) -> list[tuple[float, float]]:
    """Split a compilation into tracks at quiet gaps.

    A gap is a run of at least ``min_gap_seconds`` below ``gap_db`` relative to the peak.
    Tracks shorter than ``min_track_seconds`` (a pause inside a ballad, a spoken intro)
    are merged into the following track, or the preceding one at the end.
    """
    if envelope.size == 0 or envelope.max() <= 0:
        return []
    threshold = envelope.max() * (10 ** (gap_db / 20))
    quiet = envelope < threshold
    lo, hi = 0, envelope.size
    if region is not None:
        lo = max(0, int(region[0] / hop_seconds))
        hi = min(envelope.size, int(np.ceil(region[1] / hop_seconds)))
    loud = np.flatnonzero(~quiet[lo:hi])
    if loud.size == 0:
        return []
    first, last = lo + int(loud[0]), lo + int(loud[-1]) + 1
    min_gap = max(1, int(round(min_gap_seconds / hop_seconds)))
    cuts, run_start = [], None
    for i in range(first, last):
        if quiet[i]:
            run_start = i if run_start is None else run_start
        elif run_start is not None:
            if i - run_start >= min_gap:
                cuts.append((run_start, i))
            run_start = None
    bounds = [first] + [gap_end for _, gap_end in cuts] + [last]
    tracks = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    # Trim each track's trailing gap so clips do not end in silence.
    trimmed = []
    for a, b in tracks:
        while b > a and quiet[b - 1]:
            b -= 1
        if b > a:
            trimmed.append((a, b))
    min_track = int(round(min_track_seconds / hop_seconds))
    merged: list[list[int]] = []
    carry = None
    for a, b in trimmed:
        if carry is not None:
            a = carry
            carry = None
        if b - a < min_track:
            carry = a
            continue
        merged.append([a, b])
    if carry is not None:
        if merged:
            merged[-1][1] = trimmed[-1][1]
        else:
            merged.append([carry, trimmed[-1][1]])
    return [(round(a * hop_seconds, 3), round(b * hop_seconds, 3)) for a, b in merged]


def plan_windows(envelope: np.ndarray, hop_seconds: float, clip_seconds: float,
                 min_seconds: float, overlap_seconds: float = 0.0,
                 silence_db: float = -45.0, min_active: float = 0.6,
                 region: tuple[float, float] | None = None) -> list[tuple[float, float]]:
    """Choose [start, end) windows in seconds over the active part of an envelope.

    Leading/trailing silence is trimmed. Windows are ``clip_seconds`` long, stepping by
    ``clip_seconds - overlap_seconds``. A final shorter window is kept only if it is at
    least ``min_seconds``. Windows whose active fraction is below ``min_active`` are dropped
    (applause gaps, spoken introductions with long pauses, silence).
    """
    if clip_seconds < min_seconds:
        raise ValueError("clip_seconds must be at least min_seconds")
    if overlap_seconds >= clip_seconds:
        raise ValueError("overlap must be shorter than the clip")
    if envelope.size == 0:
        return []
    peak = float(envelope.max())
    if peak <= 0:
        return []
    threshold = peak * (10 ** (silence_db / 20))
    active = envelope > threshold
    lo, hi = 0, envelope.size
    if region is not None:
        lo = max(0, int(region[0] / hop_seconds))
        hi = min(envelope.size, int(np.ceil(region[1] / hop_seconds)))
    idx = np.flatnonzero(active[lo:hi])
    if idx.size == 0:
        return []
    first, last = lo + int(idx[0]), lo + int(idx[-1]) + 1
    start_s, end_s = first * hop_seconds, last * hop_seconds
    windows = []
    step = clip_seconds - overlap_seconds
    cursor = start_s
    while cursor < end_s:
        stop = min(cursor + clip_seconds, end_s)
        if stop - cursor + 1e-9 < min_seconds:
            break
        a, b = int(cursor / hop_seconds), int(np.ceil(stop / hop_seconds))
        fraction = float(active[a:b].mean()) if b > a else 0.0
        if fraction >= min_active:
            windows.append((round(cursor, 3), round(stop, 3)))
        cursor += step
    return windows


def _write_clip(source: Path, target: Path, start: float, end: float) -> None:
    with sf.SoundFile(source) as handle:
        rate = handle.samplerate
        handle.seek(int(round(start * rate)))
        frames = int(round((end - start) * rate))
        data = handle.read(frames, dtype="float32", always_2d=True)
    # Short fades stop clicks at the cut points without touching the musical content.
    fade = min(int(0.02 * rate), data.shape[0] // 4)
    if fade > 0:
        ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)[:, None]
        data[:fade] *= ramp
        data[-fade:] *= ramp[::-1]
    target.parent.mkdir(parents=True, exist_ok=True)
    sf.write(target, data, rate, subtype="PCM_24")


def _slug(text: str, limit: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit].strip("-") or "clip"


def segment(root: Path, cfg: Config, vid: str, clip_seconds: float = 90.0,
            overlap_seconds: float = 0.0, use_chapters: bool = False,
            role: str = "reference", instruments: list[str] | None = None,
            silence_db: float = -45.0, min_active: float = 0.6,
            use_tracks: bool = False, gap_db: float = -35.0, min_gap_seconds: float = 0.3,
            min_track_seconds: float = 90.0) -> dict:
    """Cut a fetched source into manifest-ready clips and write ``clips/manifest.jsonl``.

    Rows are drafts: the caption carries a ``TODO`` marker that the training gate rejects,
    so nothing trains until a human has written what is actually audible.

    With ``use_tracks`` a compilation is first split at quiet gaps (see
    :func:`find_tracks`) and every track becomes its own ``composition_id``, so the
    held-out split separates songs rather than one whole video.
    """
    if not cfg.data.min_seconds <= clip_seconds <= cfg.data.max_seconds:
        raise ValueError(f"clip_seconds must lie within data.min_seconds..max_seconds "
                         f"({cfg.data.min_seconds}..{cfg.data.max_seconds})")
    folder = source_dir(root, vid)
    sidecar = folder / "source.json"
    if not sidecar.is_file():
        raise FileNotFoundError(f"Fetch {vid} first: {sidecar} is missing")
    meta = json.loads(sidecar.read_text())
    kind = meta.get("kind", "youtube")
    prefix = PREFIX[kind]
    audio_path = Path(meta["audio_path"])
    if not audio_path.is_file():
        raise FileNotFoundError(f"Fetched audio missing: {audio_path}")
    if file_hash(audio_path) != meta["audio_sha256"]:
        raise ValueError("Fetched audio changed since source.json was written; refetch")
    envelope, hop = _envelope(audio_path)
    hop_seconds = hop / meta["sample_rate"]
    # Each region is (label, composition suffix, (start, end) or None for the whole file).
    regions: list[tuple[str, str, tuple[float, float] | None]] = [("", "", None)]
    if use_chapters and meta.get("chapters"):
        regions = [(f"chapter: {c['title']}", f"-c{i + 1:02d}", (c["start"], c["end"]))
                   for i, c in enumerate(meta["chapters"])]
    elif use_tracks:
        tracks = find_tracks(envelope, hop_seconds, gap_db, min_gap_seconds, min_track_seconds)
        regions = [(f"track {i + 1} of {len(tracks)}", f"-t{i + 1:02d}", t)
                   for i, t in enumerate(tracks)]
    clip_dir = folder / "clips"
    if clip_dir.exists():
        shutil.rmtree(clip_dir)
    rows, index = [], 0
    for label, suffix, region in regions:
        windows = plan_windows(envelope, hop_seconds, clip_seconds, cfg.data.min_seconds,
                               overlap_seconds, silence_db, min_active, region)
        for start, end in windows:
            index += 1
            clip_id = f"{prefix}-{vid}-{index:03d}"
            target = clip_dir / f"{clip_id}.wav"
            _write_clip(audio_path, target, start, end)
            where = f"{start:.1f}-{end:.1f} s"
            if label:
                where += f" ({label})"
            caption = (f"TODO: describe what is audible in this clip. Source title: "
                       f"{meta['title']}. Segment {where}.")
            if kind == "youtube":
                provenance = (f"YouTube {meta['url']} — {meta['title']!r} by {meta['uploader']}, "
                              f"uploaded {meta['upload_date'] or 'unknown'}; fetched "
                              f"{meta['fetched_at']} with {meta['downloader']}; segment {where}; "
                              f"platform licence: {meta['platform_license'] or 'not stated'}; "
                              f"training rights {meta['rights']}.")
            else:
                provenance = (f"Local file {meta['url']} — {meta['title']!r} by "
                              f"{meta.get('artist') or 'unknown artist'}, album "
                              f"{meta.get('album') or 'unknown'} ({meta.get('year') or 'n.d.'}); "
                              f"imported {meta['fetched_at']} via {meta['downloader']}; "
                              f"segment {where}; training rights {meta['rights']}.")
            rows.append({
                "id": clip_id, "composition_id": f"{prefix}-{vid}{suffix}",
                "audio_path": str(target.relative_to(root)),
                "caption": caption, "instruments": instruments or ["piano"],
                "provenance": provenance, "role": role, "rights": meta["rights"],
                "source_url": meta["url"], "source_id": vid,
                "source_start": start, "source_end": end,
            })
    manifest = clip_dir / "manifest.jsonl"
    if rows:
        write_jsonl(manifest, rows)
    summary = {"video_id": vid, "title": meta["title"], "source_seconds": meta["duration"],
               "clips": len(rows), "compositions": len({r["composition_id"] for r in rows}),
               "regions": [{"label": lb, "start": r[0] if r else None, "end": r[1] if r else None}
                           for lb, _, r in regions],
               "clip_seconds": clip_seconds, "role": role,
               "rights": meta["rights"], "manifest": str(manifest) if rows else None,
               "slug": _slug(meta["title"])}
    write_json(clip_dir / "segment.json", {**summary, "windows": [
        {"id": r["id"], "start": r["source_start"], "end": r["source_end"]} for r in rows]})
    return summary


# --------------------------------------------------------------------------- merge


def merge_into_manifest(root: Path, cfg: Config, clip_manifest: Path) -> dict:
    """Append clip rows to the experiment manifest, skipping IDs already present."""
    target = root / cfg.data.manifest
    new_rows = read_jsonl(clip_manifest)
    existing = read_jsonl(target) if target.is_file() else []
    seen = {r["id"] for r in existing}
    added = [r for r in new_rows if r["id"] not in seen]
    write_jsonl(target, existing + added)
    return {"manifest": str(target), "existing": len(existing), "added": len(added),
            "skipped": len(new_rows) - len(added)}


def set_caption(root: Path, cfg: Config, clip_id: str, text: str | None = None,
                bpm: int | None = None, keyscale: str | None = None,
                timesignature: str | None = None, instruments: list[str] | None = None,
                role: str | None = None) -> dict:
    """Update one manifest row in place. Only fields that are passed change."""
    target = root / cfg.data.manifest
    rows = read_jsonl(target)
    hits = [r for r in rows if r["id"] == clip_id]
    if not hits:
        raise KeyError(f"No manifest row with id {clip_id!r} in {target}")
    row = hits[0]
    if text is not None:
        if "TODO" in text or len(text.strip()) < 15:
            raise ValueError("Caption must describe what is audible, without a TODO marker")
        row["caption"] = text.strip()
    if bpm is not None:
        row["bpm"] = bpm
    if keyscale is not None:
        row["keyscale"] = keyscale
    if timesignature is not None:
        row["timesignature"] = timesignature
    if instruments:
        row["instruments"] = instruments
    if role is not None:
        row["role"] = role
    write_jsonl(target, rows)
    return row


def pending_captions(root: Path, cfg: Config) -> list[dict]:
    """Rows whose caption still carries the TODO marker, with source offsets for listening."""
    target = root / cfg.data.manifest
    if not target.is_file():
        return []
    return [{"id": r["id"], "composition_id": r["composition_id"], "role": r.get("role", "train"),
             "audio_path": r["audio_path"], "source_url": r.get("source_url", ""),
             "source_start": r.get("source_start"), "source_end": r.get("source_end")}
            for r in read_jsonl(target) if "TODO" in r["caption"]]


def list_sources(root: Path) -> list[dict]:
    rows = []
    sidecars = sorted((root / SOURCES_DIR).glob("*/source.json")) + \
        sorted((root / LOCAL_DIR).glob("*/source.json"))
    for sidecar in sidecars:
        meta = json.loads(sidecar.read_text())
        seg = sidecar.parent / "clips/segment.json"
        clips = json.loads(seg.read_text())["clips"] if seg.is_file() else 0
        rows.append({"video_id": meta["video_id"], "kind": meta.get("kind", "youtube"),
                     "title": meta["title"], "artist": meta.get("artist", ""),
                     "album": meta.get("album", ""), "url": meta.get("url", ""),
                     "duration": round(meta["duration"], 1),
                     "audible_seconds": meta.get("audible_seconds"),
                     "rights": meta["rights"], "clips": clips,
                     "video": bool(meta.get("video_path"))})
    return rows


# --------------------------------------------------------------------------- local import


def _probe_tags(path: Path) -> dict:
    import subprocess

    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:format_tags",
                          "-of", "json", str(path)], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {out.stderr.strip()[:200]}")
    fmt = json.loads(out.stdout).get("format", {})
    tags = {k.lower(): v for k, v in fmt.get("tags", {}).items()}
    return {"title": tags.get("title", ""), "artist": tags.get("artist", ""),
            "album": tags.get("album", ""), "year": tags.get("date", tags.get("year", "")),
            "genre": tags.get("genre", ""), "source_duration": float(fmt.get("duration") or 0)}


def local_source_id(path: Path) -> str:
    slug = _slug(path.stem, limit=48)
    if not slug[0].isalnum():
        slug = "x" + slug
    return slug


def import_local(root: Path, paths: list[Path], overwrite: bool = False) -> list[dict]:
    """Decode local audio files (MP3, FLAC, WAV, M4A, ...) to 48 kHz stereo WAV sources.

    Each file becomes ``data/sources/local/<slug>/audio.wav`` with a ``source.json`` sidecar
    carrying its tags and original path. Directories are walked recursively. The originals
    are read only. Rights are recorded as ``unverified``; the caller decides what to do.
    """
    import subprocess

    require_ffmpeg()
    files: list[Path] = []
    for item in paths:
        item = item.expanduser().resolve()
        if item.is_dir():
            files += sorted(f for f in item.rglob("*") if f.suffix.lower() in AUDIO_SUFFIXES)
        elif item.is_file() and item.suffix.lower() in AUDIO_SUFFIXES:
            files.append(item)
        else:
            raise FileNotFoundError(f"No audio file or folder at {item}")
    if not files:
        raise FileNotFoundError("No audio files found in the given paths")
    results = []
    seen_hashes: dict[str, str] = {}
    for src in files:
        sha = file_hash(src)
        if sha in seen_hashes:
            print(f"skip {src.name}: byte-identical to {seen_hashes[sha]}")
            continue
        seen_hashes[sha] = src.name
        sid = local_source_id(src)
        folder = root / LOCAL_DIR / sid
        sidecar = folder / "source.json"
        if sidecar.is_file() and not overwrite:
            meta = json.loads(sidecar.read_text())
            if meta.get("original_sha256") == sha and Path(meta["audio_path"]).is_file():
                results.append(meta)
                continue
            if meta.get("original_sha256") != sha:
                sid = f"{sid}-{sha[:6]}"
                folder = root / LOCAL_DIR / sid
                sidecar = folder / "source.json"
        folder.mkdir(parents=True, exist_ok=True)
        audio_path = folder / "audio.wav"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ar", str(TARGET_SAMPLE_RATE),
               "-ac", "2", "-c:a", "pcm_s24le", str(audio_path)]
        out = subprocess.run(cmd, capture_output=True, text=True)
        if out.returncode != 0:
            raise RuntimeError(f"ffmpeg failed on {src}: {out.stderr.strip()[:300]}")
        tags = _probe_tags(src)
        info = sf.info(audio_path)
        span = audible_span(audio_path)
        meta = {
            "kind": "local", "video_id": sid, "url": str(src), "title": tags["title"] or src.stem,
            "artist": tags["artist"], "album": tags["album"], "year": tags["year"],
            "genre": tags["genre"], "uploader": tags["artist"], "upload_date": tags["year"],
            "platform_license": "", "rights": "unverified",
            "duration": info.duration, "sample_rate": info.samplerate, "channels": info.channels,
            **span, "chapters": [], "audio_path": str(audio_path),
            "audio_sha256": file_hash(audio_path), "original_sha256": sha, "video_path": None,
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "downloader": "ffmpeg decode", "description": "",
        }
        write_json(sidecar, meta)
        results.append(meta)
    return results


def remove_clip(root: Path, cfg: Config, clip_id: str) -> dict:
    """Drop one row from the manifest. The clip file stays on disk."""
    target = root / cfg.data.manifest
    rows = read_jsonl(target)
    kept = [r for r in rows if r["id"] != clip_id]
    if len(kept) == len(rows):
        raise KeyError(f"No manifest row with id {clip_id!r}")
    write_jsonl(target, kept)
    return {"removed": clip_id, "remaining": len(kept)}
