"""Dataset workbench: a small local web UI for building the ACE training manifest.

It serves the clips from ``data/`` for listening, lets one person write captions and
metadata, and drives the intake stages (fetch, import, segment, prepare) as background
jobs. It binds to loopback by default and expects to sit behind Cloudflare Tunnel.

Access control is a single shared token (``MAESTRO_WEB_TOKEN``). The first visit with
``?token=...`` sets an HttpOnly cookie; every other request must carry that cookie.
Without the environment variable the server refuses to start unless ``--host`` is
loopback, in which case it runs open for local use.
"""

from __future__ import annotations

import hmac
import json
import os
import secrets
import threading
import traceback
import uuid
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse

from .config import Config, load_config
from .data import validate_recordings
from .io import read_jsonl
from .sources import (
    fetch,
    import_local,
    list_sources,
    merge_into_manifest,
    remove_clip,
    segment,
    set_caption,
    source_dir,
    video_id,
)

STATIC = Path(__file__).with_name("web_static")
COOKIE = "maestro_web"
# Served without the token so link previews (iMessage, WhatsApp, Slack) and browser tabs
# get the card and icons. Nothing here reveals dataset content.
PUBLIC_FILES = {
    "/og-card.png": ("og-card.png", "image/png"),
    "/favicon.ico": ("favicon.ico", "image/x-icon"),
    "/favicon-32.png": ("favicon-32.png", "image/png"),
    "/apple-touch-icon.png": ("apple-touch-icon.png", "image/png"),
    "/icon-512.png": ("icon-512.png", "image/png"),
}


class Jobs:
    """Serial background jobs with captured logs, one at a time to keep the disk sane."""

    def __init__(self) -> None:
        self.items: dict[str, dict] = {}
        self.lock = threading.Lock()

    def start(self, kind: str, target, **kwargs) -> dict:
        job = {"id": uuid.uuid4().hex[:8], "kind": kind, "status": "running", "log": [],
               "result": None, "args": kwargs}
        with self.lock:
            self.items[job["id"]] = job

        def run() -> None:
            try:
                job["result"] = target(job, **kwargs)
                job["status"] = "done"
            except Exception as exc:  # noqa: BLE001 - surfaced to the UI
                job["log"].append(f"ERROR {exc}")
                job["log"].append(traceback.format_exc()[-1500:])
                job["status"] = "failed"

        threading.Thread(target=run, daemon=True).start()
        return job

    def listing(self) -> list[dict]:
        with self.lock:
            return sorted(self.items.values(), key=lambda j: j["id"], reverse=True)[:20]


def _clip_row(row: dict, root: Path) -> dict:
    path = root / row["audio_path"]
    return {**row, "exists": path.is_file(), "todo": "TODO" in row.get("caption", ""),
            "role": row.get("role", "train"), "rights": row.get("rights", "own")}


def _readiness(root: Path, cfg: Config) -> dict:
    manifest = root / cfg.data.manifest
    if not manifest.is_file():
        return {"ok": False, "message": "No manifest yet. Fetch or import a source and segment it."}
    try:
        rows = validate_recordings(root, cfg)
    except Exception as exc:  # noqa: BLE001 - message is the point
        return {"ok": False, "message": str(exc)}
    train = {r["composition_id"] for r in rows if r["role"] == "train"}
    return {"ok": True, "message": f"Ready: {len(rows)} clips, {len(train)} training compositions. "
                                   "Run prepare to freeze the split."}


def create_app(root: Path, config_path: Path, token: str | None) -> FastAPI:
    app = FastAPI(title="Maestro dataset workbench", docs_url=None, redoc_url=None)
    jobs = Jobs()
    state_lock = threading.Lock()

    def cfg() -> Config:
        return load_config(config_path)

    def authorised(request: Request) -> bool:
        if token is None:
            return True
        cookie = request.cookies.get(COOKIE, "")
        return hmac.compare_digest(cookie, token)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        if request.url.path in PUBLIC_FILES:
            return await call_next(request)
        if token is not None:
            query_token = request.query_params.get("token")
            if query_token is not None and hmac.compare_digest(query_token, token):
                response = RedirectResponse(url=request.url.path or "/")
                response.set_cookie(COOKIE, token, httponly=True, secure=True, samesite="lax",
                                    max_age=60 * 60 * 24 * 90)
                return response
            if not authorised(request):
                if request.url.path.startswith("/api/"):
                    return JSONResponse({"error": "unauthorised"}, status_code=401)
                # 200 on purpose: link-preview scrapers drop cards on error statuses.
                # The page itself carries no data, only the card and a hint.
                return HTMLResponse((STATIC / "locked.html").read_text(), status_code=200,
                                    headers={"Cache-Control": "no-store"})
        return await call_next(request)

    for route, (name, media) in PUBLIC_FILES.items():
        def make(name=name, media=media):
            def public_file():
                return FileResponse(STATIC / name, media_type=media,
                                    headers={"Cache-Control": "public, max-age=86400"})
            return public_file
        app.add_api_route(route, make(), methods=["GET"], include_in_schema=False)

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return (STATIC / "index.html").read_text()

    @app.get("/api/state")
    def state() -> dict:
        c = cfg()
        manifest = root / c.data.manifest
        rows = [_clip_row(r, root) for r in read_jsonl(manifest)] if manifest.is_file() else []
        sources = list_sources(root)
        for src in sources:
            seg = source_dir(root, src["video_id"]) / "clips/segment.json"
            src["segmented"] = seg.is_file()
            src["merged"] = sum(1 for r in rows if r.get("source_id") == src["video_id"])
            src["regions"] = json.loads(seg.read_text()).get("regions", []) if seg.is_file() else []
        return {
            "experiment": root.name, "config": str(config_path),
            "allow_unverified_rights": c.data.allow_unverified_rights,
            "limits": {"min_seconds": c.data.min_seconds, "max_seconds": c.data.max_seconds},
            "clips": rows,
            "progress": {"total": len(rows), "todo": sum(r["todo"] for r in rows),
                         "train": sum(r["role"] == "train" for r in rows),
                         "reference": sum(r["role"] == "reference" for r in rows),
                         "compositions": len({r["composition_id"] for r in rows if r["role"] == "train"})},
            "sources": sources, "readiness": _readiness(root, c), "jobs": jobs.listing(),
            "prepared": (root / "artifacts/prepared/summary.json").is_file(),
        }

    @app.get("/api/audio/{clip_id}")
    def audio(clip_id: str):
        c = cfg()
        rows = read_jsonl(root / c.data.manifest)
        hit = next((r for r in rows if r["id"] == clip_id), None)
        if hit is None:
            raise HTTPException(404, "unknown clip")
        path = (root / hit["audio_path"]).resolve()
        if root.resolve() not in path.parents or not path.is_file():
            raise HTTPException(404, "clip file missing")
        return FileResponse(path, media_type="audio/wav")

    @app.get("/api/source-audio/{source_id}")
    def source_audio(source_id: str):
        meta_file = source_dir(root, source_id) / "source.json"
        if not meta_file.is_file():
            raise HTTPException(404, "unknown source")
        path = Path(json.loads(meta_file.read_text())["audio_path"]).resolve()
        if root.resolve() not in path.parents or not path.is_file():
            raise HTTPException(404, "source audio missing")
        return FileResponse(path, media_type="audio/wav")

    @app.get("/api/analysis/{clip_id}")
    def analysis(clip_id: str) -> dict:
        from .autolabel import load_analysis

        data = load_analysis(root, clip_id)
        if data is None:
            raise HTTPException(404, "no analysis yet; run auto-label")
        return data

    @app.post("/api/clip/{clip_id}")
    def update_clip(clip_id: str, payload: dict = Body(...)) -> dict:
        instruments = payload.get("instruments")
        if isinstance(instruments, str):
            instruments = [i.strip() for i in instruments.split(",") if i.strip()]
        try:
            with state_lock:
                row = set_caption(root, cfg(), clip_id, text=payload.get("caption"),
                                  bpm=payload.get("bpm"), keyscale=payload.get("keyscale"),
                                  timesignature=payload.get("timesignature"),
                                  instruments=instruments, role=payload.get("role"))
        except KeyError as exc:
            raise HTTPException(404, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        return _clip_row(row, root)

    @app.delete("/api/clip/{clip_id}")
    def delete_clip(clip_id: str) -> dict:
        try:
            with state_lock:
                return remove_clip(root, cfg(), clip_id)
        except KeyError as exc:
            raise HTTPException(404, str(exc)) from exc

    def job_fetch(job: dict, url: str, keep_video: bool) -> dict:
        job["log"].append(f"fetching {url}")
        meta = fetch(root, url, keep_video=keep_video)
        job["log"].append(f"got {meta['title']!r}, {meta['duration']:.0f} s, "
                          f"audible {meta.get('audible_seconds')} s")
        return {"video_id": meta["video_id"], "title": meta["title"]}

    def job_import(job: dict, path: str) -> dict:
        job["log"].append(f"importing {path}")
        metas = import_local(root, [Path(path)])
        for m in metas:
            job["log"].append(f"{m['video_id']}: {m['title']} — {m['duration']:.0f} s")
        return {"imported": len(metas)}

    def job_segment(job: dict, source_id: str, clip_seconds: float, role: str,
                    instruments: list[str], tracks: bool, merge: bool) -> dict:
        c = cfg()
        job["log"].append(f"segmenting {source_id} at {clip_seconds:.0f} s, role={role}, "
                          f"tracks={tracks}")
        with state_lock:
            summary = segment(root, c, source_id, clip_seconds=clip_seconds, role=role,
                              instruments=instruments, use_tracks=tracks)
            job["log"].append(f"{summary['clips']} clips in {summary['compositions']} compositions")
            if merge and summary["manifest"]:
                merged = merge_into_manifest(root, c, Path(summary["manifest"]))
                job["log"].append(f"merged {merged['added']} rows, skipped {merged['skipped']}")
        return summary

    def job_prepare(job: dict) -> dict:
        from .data import prepare
        from .io import write_json

        c = cfg()
        with state_lock:
            result = prepare(root, c, root / "artifacts/prepared")
            write_json(root / "artifacts/prepared/summary.json", result)
        job["log"].append(json.dumps(result))
        return result

    def job_autolabel(job: dict, ids: list[str] | None, force: bool) -> dict:
        from .autolabel import autolabel

        with state_lock:
            return autolabel(root, cfg(), ids=ids, force=force, log=job["log"].append)

    @app.post("/api/jobs/autolabel")
    def start_autolabel(payload: dict = Body(default={})) -> dict:
        return jobs.start("autolabel", job_autolabel, ids=payload.get("ids") or None,
                          force=bool(payload.get("force")))

    @app.post("/api/jobs/fetch")
    def start_fetch(payload: dict = Body(...)) -> dict:
        url = payload.get("url", "").strip()
        video_id(url)  # validates early
        return jobs.start("fetch", job_fetch, url=url, keep_video=bool(payload.get("keep_video")))

    @app.post("/api/jobs/import")
    def start_import(payload: dict = Body(...)) -> dict:
        path = Path(payload.get("path", "")).expanduser()
        if not path.exists():
            raise HTTPException(400, f"No such path on the server: {path}")
        return jobs.start("import", job_import, path=str(path))

    @app.post("/api/jobs/segment")
    def start_segment(payload: dict = Body(...)) -> dict:
        instruments = payload.get("instruments") or ["piano"]
        if isinstance(instruments, str):
            instruments = [i.strip() for i in instruments.split(",") if i.strip()]
        return jobs.start("segment", job_segment, source_id=payload["source_id"],
                          clip_seconds=float(payload.get("clip_seconds", 90)),
                          role=payload.get("role", "reference"), instruments=instruments,
                          tracks=bool(payload.get("tracks")), merge=bool(payload.get("merge", True)))

    @app.post("/api/jobs/prepare")
    def start_prepare() -> dict:
        return jobs.start("prepare", job_prepare)

    return app


def serve(root: Path, config_path: Path, host: str = "127.0.0.1", port: int = 8090) -> None:
    import uvicorn

    token = os.environ.get("MAESTRO_WEB_TOKEN") or None
    if token is None and host not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit("Set MAESTRO_WEB_TOKEN before binding to a non-loopback address. "
                         f"Example: MAESTRO_WEB_TOKEN={secrets.token_urlsafe(24)}")
    if token is None:
        print("No MAESTRO_WEB_TOKEN set: serving open on loopback only.")
    else:
        print(f"Open http://{host}:{port}/?token=<MAESTRO_WEB_TOKEN> once to set the cookie.")
    uvicorn.run(create_app(root, config_path, token), host=host, port=port, log_level="warning")
