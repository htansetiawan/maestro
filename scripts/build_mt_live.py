#!/usr/bin/env python3
"""Build the live Music Transformer page: the reproduced model running in the browser.

python3 scripts/build_mt_live.py

Reads experiment 020 (prompt set v1, the model pool, the real continuations,
the evaluation records, the ONNX export record, the piano samples) and writes
artifacts/music-transformer-live.html plus the files it needs under
artifacts/music-transformer/ (model, piano samples, blind-test clips). Nothing
on the page is chosen by ear: the blind test uses each prompt's first model
candidate in seed order against the pianist's own continuation.
"""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E020 = ROOT / "experiments/020_music_transformer_reproduction"
POOL = E020 / "pools/baseline-stage1-v1"
REAL = E020 / "pools/real-v1"
OUT_HTML = ROOT / "artifacts/music-transformer-live.html"
OUT_DIR = ROOT / "artifacts/music-transformer"
MODEL_FILE = "model/music-transformer-step984k-fp16.onnx"
ORT_DIR = "assets/vendor/onnxruntime-web-1.30.0"
CANONICAL = "https://htansetiawan.github.io/maestro/artifacts/music-transformer-live.html"
PAPER_RELATIVE = 1.835


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def copy(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or dest.stat().st_size != src.stat().st_size:
        shutil.copy2(src, dest)
    return dest.stat().st_size


def mmss(seconds):
    seconds = int(round(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def main():
    prompt_set = read_json(E020 / "prompts/v1.json")
    pool = read_json(POOL / "manifest.json")
    real = read_json(REAL / "manifest.json")
    best = read_json(E020 / "record/evaluation-baseline-stage1-best.json", {})
    last = read_json(E020 / "record/evaluation-baseline-stage1-last.json", {})
    export = read_json(E020 / "record/onnx-export.json", {})
    piano = read_json(OUT_DIR / "piano/index.json")
    status = read_json(E020 / "runs/baseline-stage1/status.json", {})
    config = read_json(E020 / "config.json", {})
    model_path = OUT_DIR / MODEL_FILE
    assert model_path.exists(), model_path
    assert export.get("onnx_sha256") == sha256(model_path), "export record does not match the model file"
    pool_by_name = {s["name"]: s for s in pool["samples"]}
    real_by_prompt = {s["prompt_id"]: s for s in real["samples"]}
    copied_bytes = 0
    prompts = []
    for p in prompt_set["prompts"]:
        pid = p["id"]
        model_clip = f"{pid}_c00"
        copied_bytes += copy(POOL / f"{model_clip}.mp3", OUT_DIR / f"{model_clip}.mp3")
        copied_bytes += copy(POOL / f"{model_clip}.mid", OUT_DIR / f"{model_clip}.mid")
        copied_bytes += copy(REAL / f"real_{pid}.mp3", OUT_DIR / f"real_{pid}.mp3")
        copied_bytes += copy(POOL / f"prompt_{pid}.mp3", OUT_DIR / f"prompt_{pid}.mp3")
        r = real_by_prompt[pid]
        prompts.append({
            "id": pid, "composer": p["composer"], "title": p["title"], "placeholder": bool(p.get("placeholder", False)),
            "tokens": p["tokens"], "openingSeconds": r["opening_seconds"],
            "real": {"file": f"music-transformer/real_{pid}.mp3", "seconds": r["seconds"], "notes": r["notes"]},
            "model": {"file": f"music-transformer/{model_clip}.mp3", "midi": f"music-transformer/{model_clip}.mid",
                      "seconds": pool_by_name[model_clip]["seconds"], "notes": pool_by_name[model_clip]["notes"]},
            "prompt": {"file": f"music-transformer/prompt_{pid}.mp3"},
        })
    data = {
        "model": {"file": f"music-transformer/{MODEL_FILE}", "bytes": model_path.stat().st_size, "sha256": export["onnx_sha256"],
                  "step": export["checkpoint_step"], "checkpointSha256": export["checkpoint_sha256"],
                  "layers": config["layers"], "heads": config["heads"], "depth": config["width"] // config["heads"],
                  "context": config["context"], "vocab": config["vocab_size"]},
        "ort": {"dir": f"../{ORT_DIR}/", "script": f"../{ORT_DIR}/ort.wasm.min.js", "version": "1.30.0",
                "wasmBytes": (ROOT / ORT_DIR / "ort-wasm-simd-threaded.wasm").stat().st_size},
        "piano": {"dir": "music-transformer/piano/", "pitches": piano["pitches"], "velocities": piano["velocities"],
                  "bytes": piano["total_bytes"], "rate": piano["rate"]},
        "sampling": pool["settings"],
        "prompts": prompts,
    }
    check = export.get("check", {})
    built = datetime.now(timezone.utc).strftime("%B %d, %Y").replace(" 0", " ")
    description = ("The reproduced Music Transformer runs inside this page. Give it a MAESTRO opening or silence and hear it "
                   "continue, then test your ear: pianist or model?")
    val128 = best.get("validation_fixed_128_windows", {}).get("nll_nats_per_token")
    valfull = best.get("validation_chunks", {}).get("nll_nats_per_token")
    test = best.get("test_chunks", {}).get("nll_nats_per_token")
    last_full = last.get("validation_chunks", {}).get("nll_nats_per_token")
    total_mb = (data["model"]["bytes"] + data["ort"]["wasmBytes"] + piano["total_bytes"]) / 1e6
    prompt_options = "".join(
        f'<option value="{i}">{escape(p["id"])} · {escape(p["composer"])}, {escape(p["title"])}</option>'
        for i, p in enumerate(prompts))
    template = (ROOT / "scripts/mt_live_template.html").read_text()
    page = (template
            .replace("@@DESCRIPTION@@", escape(description))
            .replace("@@CANONICAL@@", CANONICAL)
            .replace("@@BUILT@@", built)
            .replace("@@STEP@@", f"{data['model']['step']:,}")
            .replace("@@VAL128@@", f"{val128:.3f}" if val128 else "—")
            .replace("@@VALFULL@@", f"{valfull:.3f}" if valfull else "—")
            .replace("@@TEST@@", f"{test:.3f}" if test else "—")
            .replace("@@LASTFULL@@", f"{last_full:.3f}" if last_full else "—")
            .replace("@@PAPER@@", f"{PAPER_RELATIVE:.3f}")
            .replace("@@MODEL_MB@@", f"{data['model']['bytes'] / 1e6:.0f}")
            .replace("@@WASM_MB@@", f"{data['ort']['wasmBytes'] / 1e6:.0f}")
            .replace("@@PIANO_MB@@", f"{piano['total_bytes'] / 1e6:.1f}")
            .replace("@@TOTAL_MB@@", f"{total_mb:.0f}")
            .replace("@@PROMPT_OPTIONS@@", prompt_options)
            .replace("@@N_PROMPTS@@", str(len(prompts)))
            .replace("@@CHECK_POSITIONS@@", str(check.get("positions", "—")))
            .replace("@@CHECK_LOGIT@@", f"{check.get('max_abs_logit_error', float('nan')):.3f}")
            .replace("@@CHECK_AGREE@@", f"{100 * check.get('argmax_agreement', 0):.0f}")
            .replace("@@CHECK_NLL_TORCH@@", f"{check.get('nll_torch', float('nan')):.5f}")
            .replace("@@CHECK_NLL_ONNX@@", f"{check.get('nll_onnx', float('nan')):.5f}")
            .replace("@@MODEL_SHA@@", data["model"]["sha256"][:16])
            .replace("@@CKPT_SHA@@", data["model"]["checkpointSha256"][:16])
            .replace("@@PROMPTS_SHA@@", sha256(E020 / "prompts/v1.json")[:16])
            .replace("@@TOPP@@", f"{pool['settings']['top_p']:g}")
            .replace("@@SEED@@", str(pool["settings"]["seed"]))
            .replace("@@DATA@@", json.dumps(data, separators=(",", ":"))))
    OUT_HTML.write_text(page)
    record = {"built_utc": datetime.now(timezone.utc).isoformat(), "html": str(OUT_HTML.relative_to(ROOT)),
              "html_bytes": OUT_HTML.stat().st_size, "model": data["model"], "ort": data["ort"]["version"],
              "piano_samples": len(piano["samples"]), "prompts": len(prompts), "clip_bytes_copied": copied_bytes}
    (OUT_DIR / "live-build.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
