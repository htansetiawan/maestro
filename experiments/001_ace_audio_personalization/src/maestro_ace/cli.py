"""Experiment-scoped, explicit stage runner. No hidden downloads or GPU work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ROOT, load_config
from .io import write_json


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="maestro-ace")
    p.add_argument("--config", type=Path, default=ROOT / "configs/piano_violin.toml")
    p.add_argument("--ace-root", type=Path, help="Pinned ACE-Step 1.5 checkout (GPU stages)")
    p.add_argument("--checkpoints", type=Path, help="ACE checkpoint directory (GPU stages)")
    sub = p.add_subparsers(dest="stage", required=True)
    sub.add_parser("doctor", help="Show environment, config and stage readiness")
    sub.add_parser("smoke", help="Run every stage locally with synthetic data and a tiny CPU model")
    sub.add_parser("prepare", help="Validate recordings and freeze composition-level split")
    sub.add_parser("preprocess", help="ACE preprocessing for SFT train and validation")
    sub.add_parser("sft", help="Train LoRA with ACE flow-matching loss")
    g = sub.add_parser("generate", help="Generate frozen prompts and seeded candidates")
    g.add_argument("--split", choices=["feedback", "eval"], required=True)
    g.add_argument("--model", choices=["base", "sft", "human", "ai"], required=True)
    rank = sub.add_parser("rank", help="Create human or CLAP preference pairs")
    rank.add_argument("--source", choices=["human", "ai"], required=True)
    rank.add_argument("--ballots", type=Path, help="Required for human ranking")
    pp = sub.add_parser("preprocess-pairs", help="ACE preprocessing for ranked candidates")
    pp.add_argument("--source", choices=["human", "ai"], required=True)
    tr = sub.add_parser("preference", help="Train experimental offline flow-DPO adapter")
    tr.add_argument("--source", choices=["human", "ai"], required=True)
    sub.add_parser("report", help="Build a matched-seed blind listening index")
    fetch = sub.add_parser("fetch", help="Download YouTube audio (48 kHz WAV) into data/sources/")
    fetch.add_argument("urls", nargs="+", help="YouTube URLs or video IDs")
    fetch.add_argument("--keep-video", action="store_true", help="Also keep an mp4 for viewing")
    fetch.add_argument("--overwrite", action="store_true")
    seg = sub.add_parser("segment", help="Cut a fetched source into clips and draft manifest rows")
    seg.add_argument("video_ids", nargs="+", help="Video IDs or URLs already fetched")
    seg.add_argument("--clip-seconds", type=float, default=90.0)
    seg.add_argument("--overlap-seconds", type=float, default=0.0)
    seg.add_argument("--chapters", action="store_true", help="Cut per YouTube chapter")
    seg.add_argument("--tracks", action="store_true",
                     help="Split a compilation at quiet gaps; one composition per track")
    seg.add_argument("--gap-db", type=float, default=-35.0, help="Gap threshold below peak")
    seg.add_argument("--min-gap-seconds", type=float, default=0.3)
    seg.add_argument("--min-track-seconds", type=float, default=90.0)
    seg.add_argument("--role", choices=["reference", "train"], default="reference",
                     help="train rows still pass the rights gate in prepare")
    seg.add_argument("--instruments", default="piano", help="Comma-separated, e.g. piano,strings")
    seg.add_argument("--silence-db", type=float, default=-45.0)
    seg.add_argument("--min-active", type=float, default=0.6)
    seg.add_argument("--merge", action="store_true",
                     help="Append the clip rows to data/recordings.jsonl")
    sub.add_parser("sources", help="List fetched sources and their clip counts")
    cap = sub.add_parser("caption", help="Set caption/metadata on one manifest row")
    cap.add_argument("clip_id")
    cap.add_argument("--text", help="What is audible: instruments, texture, motion, mood")
    cap.add_argument("--bpm", type=int)
    cap.add_argument("--keyscale", help='e.g. "Eb major"')
    cap.add_argument("--timesignature", help='e.g. "4"')
    cap.add_argument("--instruments", help="Comma-separated")
    cap.add_argument("--role", choices=["reference", "train"])
    sub.add_parser("pending", help="List manifest rows whose captions are still TODO")
    imp = sub.add_parser("import", help="Decode local audio files/folders into data/sources/local/")
    imp.add_argument("paths", nargs="+", type=Path)
    imp.add_argument("--overwrite", action="store_true")
    imp.add_argument("--segment", action="store_true", help="Also cut clips for each file")
    imp.add_argument("--clip-seconds", type=float, default=90.0)
    imp.add_argument("--role", choices=["reference", "train"], default="reference")
    imp.add_argument("--instruments", default="piano")
    imp.add_argument("--merge", action="store_true", help="Append clip rows to the manifest")
    al = sub.add_parser("autolabel", help="Draft captions/BPM/key/instruments from the audio")
    al.add_argument("--ids", nargs="*", help="Only these clip IDs (default: every TODO row)")
    al.add_argument("--force", action="store_true", help="Also overwrite human captions")
    al.add_argument("--no-clap", action="store_true", help="Skip CLAP instrument tagging")
    al.add_argument("--device", help="cuda or cpu for CLAP (default: auto)")
    web = sub.add_parser("web", help="Serve the dataset workbench (local web UI)")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8090)
    return p


def _require_gpu_args(args, cfg):
    if not args.ace_root or not args.checkpoints:
        raise ValueError("GPU stages require --ace-root and --checkpoints")
    from .ace import check_ace_checkout, check_checkpoint_dir, use_ace_python

    revision = check_ace_checkout(args.ace_root, cfg)
    check_checkpoint_dir(args.checkpoints, cfg)
    use_ace_python(args.ace_root.resolve())
    import torch

    if cfg.runtime.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but PyTorch cannot see a CUDA GPU")
    print(f"ACE {revision[:12]} | torch {torch.__version__} | {cfg.runtime.device}")


def _prepared(artifacts: Path) -> Path:
    folder = artifacts / "prepared"
    if not (folder / "train.json").is_file():
        raise FileNotFoundError("Run prepare first")
    return folder


def _adapter(artifacts: Path, name: str) -> Path:
    path = artifacts / "checkpoints" / name / "final" / "adapter"
    if not (path / "adapter_config.json").is_file():
        raise FileNotFoundError(f"Adapter missing: {path}")
    return path


def main() -> None:
    args = parser().parse_args()
    cfg = load_config(args.config.resolve())
    root = ROOT
    artifacts = root / "artifacts"
    stage = args.stage
    if stage == "smoke":
        from .smoke import run_smoke

        print(json.dumps(run_smoke(cfg), indent=2))
        return
    if stage == "fetch":
        from .sources import fetch

        for url in args.urls:
            meta = fetch(root, url, keep_video=args.keep_video, overwrite=args.overwrite)
            print(json.dumps({k: meta[k] for k in ("video_id", "title", "uploader", "duration",
                                                    "rights", "platform_license", "audio_path",
                                                    "video_path")}, indent=2))
        return
    if stage == "segment":
        from .sources import merge_into_manifest, segment, video_id

        instruments = [i.strip() for i in args.instruments.split(",") if i.strip()]
        for item in args.video_ids:
            summary = segment(root, cfg, video_id(item), clip_seconds=args.clip_seconds,
                              overlap_seconds=args.overlap_seconds, use_chapters=args.chapters,
                              role=args.role, instruments=instruments,
                              silence_db=args.silence_db, min_active=args.min_active,
                              use_tracks=args.tracks, gap_db=args.gap_db,
                              min_gap_seconds=args.min_gap_seconds,
                              min_track_seconds=args.min_track_seconds)
            print(json.dumps(summary, indent=2))
            if args.merge and summary["manifest"]:
                print(json.dumps(merge_into_manifest(root, cfg, Path(summary["manifest"]))))
        return
    if stage == "sources":
        from .sources import list_sources

        print(json.dumps(list_sources(root), indent=2))
        return
    if stage == "caption":
        from .sources import set_caption

        instruments = [i.strip() for i in (args.instruments or "").split(",") if i.strip()]
        row = set_caption(root, cfg, args.clip_id, text=args.text, bpm=args.bpm,
                          keyscale=args.keyscale, timesignature=args.timesignature,
                          instruments=instruments or None, role=args.role)
        print(json.dumps(row, indent=2))
        return
    if stage == "import":
        from .sources import import_local, merge_into_manifest, segment

        metas = import_local(root, args.paths, overwrite=args.overwrite)
        print(f"Imported {len(metas)} source(s)")
        instruments = [i.strip() for i in args.instruments.split(",") if i.strip()]
        for meta in metas:
            line = {"id": meta["video_id"], "title": meta["title"], "artist": meta["artist"],
                    "album": meta["album"], "seconds": round(meta["duration"], 1)}
            if args.segment:
                summary = segment(root, cfg, meta["video_id"], clip_seconds=args.clip_seconds,
                                  role=args.role, instruments=instruments)
                line["clips"] = summary["clips"]
                if args.merge and summary["manifest"]:
                    line["merged"] = merge_into_manifest(root, cfg, Path(summary["manifest"]))["added"]
            print(json.dumps(line))
        return
    if stage == "autolabel":
        from .autolabel import autolabel

        result = autolabel(root, cfg, ids=args.ids or None, force=args.force,
                           use_clap=not args.no_clap, device=args.device)
        print(json.dumps({k: len(v) for k, v in result.items()}))
        return
    if stage == "web":
        from .web import serve

        serve(root, args.config.resolve(), host=args.host, port=args.port)
        return
    if stage == "pending":
        from .sources import pending_captions

        rows = pending_captions(root, cfg)
        print(json.dumps(rows, indent=2))
        print(f"{len(rows)} caption(s) still TODO")
        return
    if stage == "doctor":
        import shutil

        from .data import load_prompts

        try:
            import yt_dlp

            downloader = f"yt-dlp {yt_dlp.version.__version__}"
        except ImportError:
            downloader = None
        prompts = load_prompts(root, cfg)
        status = {"experiment": root.name, "config": str(args.config.resolve()),
                  "ffmpeg": shutil.which("ffmpeg"), "yt_dlp": downloader,
                  "allow_unverified_rights": cfg.data.allow_unverified_rights,
                  "ace_revision": cfg.runtime.ace_revision,
                  "recordings_manifest": (root / cfg.data.manifest).is_file(),
                  "prepared": (artifacts / "prepared/train.json").is_file(),
                  "sft_adapter": (artifacts / "checkpoints/sft/final/adapter/adapter_config.json").is_file(),
                  "feedback_prompts": len(prompts["feedback"]), "eval_prompts": len(prompts["eval"]),
                  "ace_root": str(args.ace_root) if args.ace_root else None,
                  "checkpoints": str(args.checkpoints) if args.checkpoints else None}
        print(json.dumps(status, indent=2))
        return
    if stage == "prepare":
        from .data import prepare

        result = prepare(root, cfg, artifacts / "prepared")
        write_json(artifacts / "prepared/summary.json", result)
        print(json.dumps(result, indent=2))
        return
    if stage == "report":
        from .report import report

        print(json.dumps(report(root, cfg, artifacts), indent=2))
        return
    if stage == "rank":
        from .preferences import make_ai_pairs, make_human_pairs

        candidate_file = artifacts / "generations/feedback/sft/candidates.jsonl"
        output = artifacts / "preferences" / args.source / "pairs.jsonl"
        if args.source == "human":
            if not args.ballots:
                raise ValueError("--ballots is required for human ranking")
            pairs = make_human_pairs(candidate_file, args.ballots, output)
        else:
            pairs = make_ai_pairs(candidate_file, output, cfg)
        print(f"Wrote {len(pairs)} {args.source} pairs to {output}")
        return

    _require_gpu_args(args, cfg)
    from .ace import preprocess

    if stage == "preprocess":
        prepared = _prepared(artifacts)
        for split in ("train", "validation"):
            result = preprocess(args.ace_root, args.checkpoints, cfg, prepared / f"{split}.json",
                                artifacts / "tensors" / split)
            print(split, result)
    elif stage == "sft":
        from .train import run_sft

        _prepared(artifacts)
        if not (artifacts / "tensors/train").is_dir():
            raise FileNotFoundError("Run preprocess first")
        run_sft(args.checkpoints, cfg, artifacts / "tensors/train",
                artifacts / "tensors/validation",
                artifacts / "checkpoints/sft")
    elif stage == "generate":
        from .generate import generate

        adapter = None if args.model == "base" else _adapter(artifacts, args.model)
        rows = generate(root, args.ace_root, args.checkpoints, cfg,
                        args.model, adapter, args.split,
                        artifacts / "generations" / args.split / args.model)
        print(f"Generated {len(rows)} audio candidates")
    elif stage == "preprocess-pairs":
        from .preferences import make_preprocess_manifest

        pair_root = artifacts / "preferences" / args.source
        count = make_preprocess_manifest(
            artifacts / "generations/feedback/sft/candidates.jsonl",
            pair_root / "pairs.jsonl", pair_root / "ace_samples.json")
        result = preprocess(args.ace_root, args.checkpoints, cfg,
                            pair_root / "ace_samples.json", pair_root / "tensors")
        print(f"Preprocessed {count} paired candidates: {result}")
    elif stage == "preference":
        from .train import run_preference

        pair_root = artifacts / "preferences" / args.source
        run_preference(args.checkpoints, cfg, _adapter(artifacts, "sft"),
                       pair_root / "pairs.jsonl", pair_root / "tensors",
                       artifacts / "checkpoints" / args.source)
    else:
        raise AssertionError(stage)


if __name__ == "__main__":
    main()
