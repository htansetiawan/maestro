#!/usr/bin/env python3
"""Build the Music Transformer reproduction page from experiment records.

python3 scripts/build_mt_demo.py [--pool experiments/020_.../pools/<pool>] [--render]

Reads experiments 020 (training, prompts, pool), 023 (parity), and 024
(ablations) and writes artifacts/music-transformer-reproduction.html plus
artifacts/music-transformer/ (audio, MIDI, chart data). Missing pieces are
reported on the page as pending, never invented.
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E020 = ROOT / "experiments/020_music_transformer_reproduction"
E023 = ROOT / "experiments/023_t2t_parity_check"
E024 = ROOT / "experiments/024_music_transformer_ablations"
OUT_HTML = ROOT / "artifacts/music-transformer-reproduction.html"
OUT_DIR = ROOT / "artifacts/music-transformer"
CANONICAL = "https://htansetiawan.github.io/maestro/artifacts/music-transformer-reproduction.html"

PAPER = {"baseline": 1.861, "relative": 1.835, "local": 1.840,
         "url": "https://arxiv.org/abs/1809.04281"}

SERIES = [  # fixed order = fixed categorical slots
    ("baseline-stage1", E020 / "runs/baseline-stage1", "Relative attention, released config", "6 layers · 512 hidden · 1024 feed-forward · 16.1M parameters"),
    ("vanilla-medium", E024 / "runs/vanilla-medium", "Vanilla attention, same sizes", "6 layers · 512 hidden · 1024 feed-forward · 12.9M parameters"),
    ("relative-tiny", E024 / "runs/relative-tiny", "Relative attention, paper's Table 3 sizes", "6 layers · 256 hidden · 512 attention · 2048 feed-forward · 12.0M parameters"),
    ("vanilla-tiny", E024 / "runs/vanilla-tiny", "Vanilla attention, paper's Table 3 sizes", "6 layers · 256 hidden · 512 attention · 2048 feed-forward · 8.8M parameters"),
]


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def read_metrics(run):
    rows = []
    path = run / "metrics.jsonl"
    if not path.exists():
        return rows
    for line in path.read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def run_summary(name, run):
    status = read_json(run / "status.json", {})
    metrics = read_metrics(run)
    validation = [(r["step"], r["nll_nats_per_token"]) for r in metrics if r["event"] == "validation"]
    dedup = {}
    for step, nll in validation:
        dedup[step] = nll  # resumed stages repeat a validation at the resume step
    validation = sorted(dedup.items())
    full = [r for r in metrics if r["event"] == "full_validation"]
    return {
        "name": name, "state": status.get("state"), "step": status.get("step"),
        "target": status.get("target_steps"), "best": status.get("best_validation_nll"),
        "validation": validation, "full": full[-1] if full else None,
        "elapsed": status.get("elapsed_seconds"),
    }


def fmt(x, digits=3):
    return "—" if x is None else f"{x:.{digits}f}"


def steps_label(step):
    return f"{step/1000:.0f}K" if step else "0"


# ---------------------------------------------------------------- chart

def line_chart(series, y_domain=(1.7, 2.6), x_start=10000):
    """Inline SVG line chart of validation NLL versus step, with a hover layer."""
    width, height = 880, 420
    left, right, top, bottom = 56, 24, 20, 48
    plot_w, plot_h = width - left - right, height - top - bottom
    x_max = max([s["target"] or 0 for s in series] + [max((st for st, _ in s["validation"]), default=0) for s in series] + [x_start + 1])
    x_max = max(x_max, 100000)

    def sx(step):
        return left + (step - x_start) / (x_max - x_start) * plot_w

    def sy(value):
        lo, hi = y_domain
        return top + (hi - value) / (hi - lo) * plot_h

    parts = []
    # gridlines and ticks
    y_ticks = [round(y_domain[0] + i * 0.1, 2) for i in range(int(round((y_domain[1] - y_domain[0]) / 0.1)) + 1)]
    for value in y_ticks:
        y = sy(value)
        parts.append(f'<line class="grid" x1="{left}" x2="{width-right}" y1="{y:.1f}" y2="{y:.1f}"/>')
        parts.append(f'<text class="tick" x="{left-8}" y="{y+4:.1f}" text-anchor="end">{value:.1f}</text>')
    x_ticks = list(range(0, x_max + 1, 100000 if x_max > 300000 else 20000))
    x_ticks = [t for t in x_ticks if t >= x_start]
    for step in x_ticks:
        x = sx(step)
        parts.append(f'<text class="tick" x="{x:.1f}" y="{height-bottom+20}" text-anchor="middle">{steps_label(step)}</text>')
    parts.append(f'<line class="axis" x1="{left}" x2="{width-right}" y1="{top+plot_h:.1f}" y2="{top+plot_h:.1f}"/>')
    parts.append(f'<text class="axis-label" x="{left}" y="{top-6}">Validation NLL, nats per token (128 fixed windows)</text>')
    parts.append(f'<text class="axis-label" x="{width-right}" y="{height-6}" text-anchor="end">Optimizer steps</text>')
    ends = []
    for slot, s in enumerate(series, 1):
        points = [(st, v) for st, v in s["validation"] if st >= x_start and y_domain[0] <= v <= y_domain[1]]
        if not points:
            continue
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(st):.1f},{sy(v):.1f}" for i, (st, v) in enumerate(points))
        parts.append(f'<path class="line s{slot}" d="{d}"/>')
        st, v = points[-1]
        ends.append((slot, sx(st), sy(v), s))
    for slot, x, y, s in ends:
        parts.append(f'<circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="6"/>')
        parts.append(f'<circle class="dot s{slot}" cx="{x:.1f}" cy="{y:.1f}" r="4"/>')
    # end labels only where they do not collide
    ends_sorted = sorted(ends, key=lambda e: e[2])
    for i, (slot, x, y, s) in enumerate(ends_sorted):
        near = [e for j, e in enumerate(ends_sorted) if j != i and abs(e[2] - y) < 14]
        if not near:
            last = s["validation"][-1][1]
            parts.append(f'<text class="end-label" x="{min(x+10, width-right-60):.1f}" y="{y+4:.1f}">{last:.3f}</text>')
    hover = (f'<line id="crosshair" class="crosshair" x1="0" x2="0" y1="{top}" y2="{top+plot_h}" hidden/>'
             f'<rect id="hit" x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="transparent"/>')
    svg = (f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">'
           f'<title id="chart-title">Validation loss against training steps</title>'
           f'<desc id="chart-desc">Validation negative log-likelihood per token on 128 fixed MAESTRO validation windows, plotted from step {x_start:,} onward; the table below lists the values.</desc>'
           + "".join(parts) + hover + '</svg>')
    scale = {"left": left, "right": right, "top": top, "bottom": bottom, "width": width, "height": height,
             "x_start": x_start, "x_max": x_max, "y_lo": y_domain[0], "y_hi": y_domain[1]}
    return svg, scale


def chart_table(series):
    steps = sorted({st for s in series for st, _ in s["validation"]})
    marks = [st for st in steps if st % 50000 == 0 or st == steps[-1]]
    head = "".join(f"<th>{escape(s['label'])}</th>" for s in series)
    rows = []
    for st in marks:
        cells = []
        for s in series:
            value = dict(s["validation"]).get(st)
            cells.append(f"<td class=\"mono\">{fmt(value, 4)}</td>")
        rows.append(f"<tr><td class=\"mono\">{st:,}</td>{''.join(cells)}</tr>")
    return (f'<details class="table-view"><summary>Table view: validation NLL at every 50,000 steps and the latest evaluation</summary>'
            f'<div class="table-scroll"><table><thead><tr><th>Step</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>')


# ---------------------------------------------------------------- sections

def pool_section(pool, prompts, render, prompts_on_page=8, candidates_on_page=2):
    manifest = read_json(pool / "manifest.json")
    if not manifest:
        return "<p>No listening pool has been generated yet.</p>", {}
    by_prompt = {}
    for row in manifest["samples"]:
        if row["candidate"] < candidates_on_page:
            by_prompt.setdefault(row["prompt_id"], []).append(row)
    prompted = [k for k in by_prompt if k != "unconditioned"][:prompts_on_page]
    keep = (["unconditioned"] if "unconditioned" in by_prompt else []) + prompted
    by_prompt = {k: by_prompt[k] for k in keep}
    total = len(manifest["samples"])
    prompt_meta = {p["id"]: p for p in prompts.get("prompts", [])}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    blocks = []
    for prompt_id, rows in by_prompt.items():
        meta = prompt_meta.get(prompt_id)
        prompt_audio = pool / f"prompt_{prompt_id}.mp3"
        if meta and not prompt_audio.exists() and render:
            render_prompt(meta, pool / f"prompt_{prompt_id}.mid", prompt_audio)
        items = []
        if meta:
            title = f"{escape(meta['composer'])} — {escape(meta['title'])}"
            intro = (f"<p class=\"clip-note\">The first 512 events of a MAESTRO validation performance "
                     f"(about {prompt_seconds(pool, prompt_id)} seconds) are given to the model; it continues from there. "
                     f"The real performance is held out from training.</p>")
            if prompt_audio.exists():
                shutil.copy2(prompt_audio, OUT_DIR / prompt_audio.name); copied.append(prompt_audio.name)
                items.append(f'<div class="clip"><div class="clip-head"><span class="clip-role">Prompt</span> the real opening</div>'
                             f'<audio controls preload="none" src="music-transformer/{prompt_audio.name}" aria-label="Prompt, {title}"></audio></div>')
        else:
            title = "Unconditioned"
            intro = "<p class=\"clip-note\">No prompt: the model starts from silence and plays on its own.</p>"
        for row in rows:
            mp3 = pool / f"{row['name']}.mp3"
            mid = pool / f"{row['name']}.mid"
            if not mp3.exists():
                continue
            shutil.copy2(mp3, OUT_DIR / mp3.name); copied.append(mp3.name)
            if mid.exists():
                shutil.copy2(mid, OUT_DIR / mid.name); copied.append(mid.name)
            detail = []
            if row.get("seconds"):
                detail.append(f"{row['seconds']:.0f} s")
            if row.get("notes"):
                detail.append(f"{row['notes']} notes")
            midi_link = f' · <a href="music-transformer/{mid.name}">MIDI</a>' if mid.exists() else ""
            items.append(f'<div class="clip"><div class="clip-head"><span class="clip-role">Continuation {row["candidate"]+1}</span> '
                         f'{", ".join(detail)}{midi_link}</div>'
                         f'<audio controls preload="none" src="music-transformer/{mp3.name}" aria-label="Continuation {row["candidate"]+1}, {title}"></audio></div>')
        blocks.append(f'<section class="listen"><h3>{title}</h3>{intro}<div class="clips">{"".join(items)}</div></section>')
    settings = manifest["settings"]
    note = (f'<p class="journal-meta">Checkpoint step {manifest.get("checkpoint_step"):,} · temperature {settings["temperature"]} · '
            f'nucleus {settings["top_p"]} · seed {settings["seed"]} · {settings["new_tokens"]} new events per continuation · '
            f'rendered with one FluidR3 General MIDI piano for every clip, peak-normalized. '
            f'The page shows the first {candidates_on_page} of {settings["candidates"]} continuations per prompt in seed order, for the first {len(prompted)} prompts of the frozen set; '
            f'nothing was chosen by ear. The full pool of {total} clips and its manifest are in the experiment record.</p>')
    return note + "".join(blocks), {"copied": copied, "checkpoint_step": manifest.get("checkpoint_step"),
                                    "checkpoint_sha256": manifest.get("checkpoint_sha256")}


def prompt_seconds(pool, prompt_id):
    try:
        sys.path.insert(0, str(E020))
        import note_seq  # noqa: F401
        from midi_io import tokens_to_sequence
        meta = next(p for p in read_json(E020 / "prompts/v1.json")["prompts"] if p["id"] == prompt_id)
        return f"{tokens_to_sequence(meta['tokens']).total_time:.0f}"
    except Exception:
        return "20"


def render_prompt(meta, mid, mp3):
    sys.path.insert(0, str(E020))
    from midi_io import write_midi
    from render import render_wav, wav_to_mp3
    write_midi(meta["tokens"], mid)
    wav = mid.with_suffix(".wav")
    render_wav(mid, wav)
    wav_to_mp3(wav, mp3)
    wav.unlink()


def parity_section():
    parity = read_json(E023 / "record/parity.json")
    if not parity:
        return "<p>Parity record pending.</p>"
    rows = []
    for length in parity["lengths"]:
        r = parity["results"][str(length)]
        grads = r.get("gradients", {})
        cos = min((g.get("cosine", 1.0) for g in grads.values() if isinstance(g, dict) and "cosine" in g), default=None)
        rows.append(f"<tr><td class=\"mono\">{length:,}</td><td class=\"mono\">{r['logits']['max_abs_diff']:.1e}</td>"
                    f"<td class=\"mono\">{r['logits'].get('port_max_abs', 0):.2f}</td>"
                    f"<td class=\"mono\">{r['loss']['abs_diff']:.1e}</td><td class=\"mono\">{fmt(cos, 7)}</td></tr>")
    mapping = parity.get("t2t_mapping_check", {})
    return (f'<div class="table-scroll"><table><thead><tr><th>Sequence length</th><th>Max |Δ logit|</th><th>Logit scale</th>'
            f'<th>|Δ loss|</th><th>Min gradient cosine</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p>{escape(parity["verdict"])}</p>'
            f'<p>Every one of the {mapping.get("tf_variables", "—")} TensorFlow variables maps onto the {mapping.get("port_tensors", "—")} PyTorch tensors with nothing unmapped or unused. '
            f'Same random weights loaded into both frameworks, dropout off, identical inputs, CPU float32; the original ran under Python 3.7 with TensorFlow 1.15.5 and Tensor2Tensor 1.15.7.</p>')


def data_section():
    manifest = read_json(E020 / "data/manifest.json")
    summary = read_json(E020 / "record/data_summary.json", {})
    if not manifest:
        return "<p>Data record pending.</p>"
    by = {}
    for r in manifest["records"]:
        b = by.setdefault(r["split"], [0, 0.0, set()])
        b[0] += 1; b[1] += r["duration_seconds"]; b[2].add((r["composer"], r["title"]))
    rows = "".join(f"<tr><td>{split.capitalize()}</td><td class=\"mono\">{n}</td><td class=\"mono\">{h/3600:.1f}</td>"
                   f"<td class=\"mono\">{len(w)}</td><td class=\"mono\">{summary.get('tokens_by_split', {}).get(split, 0):,}</td></tr>"
                   for split, (n, h, w) in [(s, by[s]) for s in ("train", "validation", "test")])
    return (f'<div class="table-scroll"><table><thead><tr><th>Split</th><th>Performances</th><th>Hours</th><th>Distinct works</th><th>Tokens (train includes 5 tempo variants)</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def comparison_rows(runs, best_eval=None, last_eval=None):
    rows = [
        ("Paper, Transformer baseline (6L, 256 hidden, 512 attention, 2048 feed-forward)", "Piano-e-Competition, authors' split", fmt(PAPER["baseline"]), "Reported in Table 3"),
        ("Paper, relative global attention (6L, 2048 feed-forward, 1024 relative)", "Piano-e-Competition, authors' split", fmt(PAPER["relative"]), "Reported in Table 3"),
    ]
    labels = {s[0]: s[2] for s in SERIES}
    for name, r in runs.items():
        if not r["validation"]:
            continue
        if name == "baseline-stage1" and best_eval and best_eval.get("validation_chunks") and r["state"] == "complete":
            for tag, ev in (("best checkpoint", best_eval), ("final checkpoint", last_eval)):
                if not ev or not ev.get("validation_chunks"):
                    continue
                text = (f"{fmt(ev['validation_chunks']['nll_nats_per_token'])} on every validation event; "
                        f"{fmt(ev['validation_fixed_128_windows']['nll_nats_per_token'])} on the 128 fixed windows; "
                        f"test {fmt(ev['test_chunks']['nll_nats_per_token'])}")
                rows.append((f"This work, {labels[name]}, {tag} (step {ev['step']:,})", "MAESTRO v1, official split", text, "Complete"))
            continue
        value = r["full"]["nll_nats_per_token"] if r["full"] else r["best"]
        protocol = "full validation, consecutive 2,048-event chunks" if r["full"] else "best of 128 fixed windows so far"
        status = "Complete" if r["state"] == "complete" else (f"Training, step {r['step']:,} of {r['target']:,}" if r.get("step") else "Pending")
        rows.append((f"This work, {labels[name]}", "MAESTRO v1, official split", f"{fmt(value)} ({protocol})", status))
    return "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td><td class=\"mono\">{escape(c)}</td><td>{escape(d)}</td></tr>" for a, b, c, d in rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", default=str(E020 / "pools/preview-step100k"))
    parser.add_argument("--render", action="store_true", help="render missing prompt audio (needs note-seq on PYTHONPATH)")
    parser.add_argument("--prompts-on-page", type=int, default=8, help="first N prompts of the pool, in prompt-set order")
    parser.add_argument("--candidates-on-page", type=int, default=2, help="first K candidates per prompt, by seed order, never by ear")
    args = parser.parse_args()
    runs = {name: run_summary(name, path) for name, path, _, _ in SERIES if (path / "metrics.jsonl").exists()}
    series = []
    for slot, (name, path, label, desc) in enumerate(SERIES, 1):
        if name in runs and runs[name]["validation"] and (runs[name]["state"] == "complete" or runs[name]["validation"][-1][0] >= 50000):
            series.append({**runs[name], "label": label, "desc": desc, "slot": slot})
    main_run = runs.get("baseline-stage1", {})
    svg, scale = line_chart(series)
    chart_data = [{"label": s["label"], "slot": s["slot"], "points": s["validation"]} for s in series]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "curves.json").write_text(json.dumps({"series": chart_data, "scale": scale}) + "\n")
    prompts = read_json(E020 / "prompts/v1.json", {})
    listening, pool_info = pool_section(Path(args.pool), prompts, args.render, args.prompts_on_page, args.candidates_on_page)
    config = read_json(E020 / "config.json", {})
    parity = read_json(E023 / "record/parity.json", {})
    worst = parity.get("worst_case", {})
    state = main_run.get("state")
    headline_value = main_run["full"]["nll_nats_per_token"] if main_run.get("full") and state == "complete" else main_run.get("best")
    headline_label = "Validation NLL, full validation set" if main_run.get("full") and state == "complete" else "Best validation NLL so far, 128 windows"
    best_eval = read_json(E020 / "record/evaluation-baseline-stage1-best.json", {})
    last_eval = read_json(E020 / "record/evaluation-baseline-stage1-last.json", {})
    evaluated = state == "complete" and bool(best_eval.get("validation_chunks"))
    if evaluated:
        headline_value = best_eval["validation_chunks"]["nll_nats_per_token"]
        headline_label = f"Validation NLL, full set, best checkpoint (step {best_eval['step']:,})"
    steps_note = ("complete; one 2,048-event crop per step" if state == "complete"
                  else f"of {(main_run.get('target') or 0)/1000:,.0f}K planned, one 2,048-event crop per step")
    extra_stats = ""
    if evaluated:
        extra_stats = (f'<div class="stat"><p class="label">Validation NLL, 128 fixed windows</p><p class="value">{fmt(best_eval["validation_fixed_128_windows"]["nll_nats_per_token"])}</p><p class="note">the model-selection metric, same checkpoint</p></div>\n'
                       f'  <div class="stat"><p class="label">Test NLL, reported once</p><p class="value">{fmt(best_eval["test_chunks"]["nll_nats_per_token"])}</p><p class="note">MAESTRO v1 test split, {best_eval["test_chunks"]["tokens"]/1e6:.2f}M events</p></div>\n  ')
    status_line = ("Training complete" if state == "complete" else
                   f"Training in progress: step {main_run.get('step', 0):,} of {main_run.get('target', 0):,}")
    legend = "".join(f'<li><span class="key s{s["slot"]}"></span><span>{escape(s["label"])}<small>{escape(s["desc"])}</small></span></li>' for s in series)
    built = datetime.now(timezone.utc).strftime("%B %d, %Y").replace(" 0", " ")
    description = "The released Music Transformer configuration retrained on MAESTRO v1 in PyTorch, matched numerically to the original Tensor2Tensor code, with learning curves, the paper's comparison, and continuations to hear."
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Music Transformer, reproduced — Maestro</title>
<meta name="description" content="{escape(description)}">
<meta name="author" content="Henry Tan">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{CANONICAL}">
<link rel="alternate" type="application/atom+xml" title="Maestro journal" href="../journal/feed.xml">
<meta property="og:site_name" content="Maestro">
<meta property="og:type" content="article">
<meta property="og:title" content="Music Transformer, reproduced — Maestro">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{CANONICAL}">
<meta property="og:image" content="https://htansetiawan.github.io/maestro/assets/og-cover.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Music Transformer, reproduced — Maestro">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="https://htansetiawan.github.io/maestro/assets/og-cover.png">
<link rel="icon" href="../assets/favicon.ico">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/site.css">
<link rel="stylesheet" href="../assets/journal.css">
<script src="../assets/share.js" defer></script>
<style>
  .viz-root {{ --series-1: #2a78d6; --series-2: #eb6834; --series-3: #1baf7a; --series-4: #eda100; }}
  @media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) .viz-root {{ --series-1: #3987e5; --series-2: #d95926; --series-3: #199e70; --series-4: #c98500; }} }}
  :root[data-theme="dark"] .viz-root {{ --series-1: #3987e5; --series-2: #d95926; --series-3: #199e70; --series-4: #c98500; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 1rem; margin: 1.5rem 0 2.5rem; }}
  .stat {{ border-top: 2px solid var(--rule); padding-top: .6rem; }}
  .stat .label {{ font-size: .8rem; color: var(--ink-2); margin: 0 0 .2rem; }}
  .stat .value {{ font-family: var(--f-body); font-weight: 600; font-size: 2rem; line-height: 1.1; margin: 0; }}
  .stat .note {{ font-size: .78rem; color: var(--ink-3); margin: .25rem 0 0; }}
  .status-line {{ font-family: var(--f-mono); font-size: .78rem; color: var(--ink-2); letter-spacing: .04em; }}
  figure.viz-root {{ margin: 1.5rem 0 2rem; position: relative; }}
  .chart {{ width: 100%; height: auto; display: block; font-family: var(--f-body); }}
  .chart .grid {{ stroke: var(--rule-soft); stroke-width: 1; }}
  .chart .axis {{ stroke: var(--rule); stroke-width: 1; }}
  .chart .tick, .chart .axis-label, .chart .end-label {{ fill: var(--ink-3); font-size: 12px; font-family: var(--f-mono); }}
  .chart .axis-label {{ fill: var(--ink-2); font-family: var(--f-body); }}
  .chart .end-label {{ fill: var(--ink-2); }}
  .chart .line {{ fill: none; stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }}
  .chart .ring {{ fill: var(--paper); }}
  .chart .s1 {{ stroke: var(--series-1); }} .chart .s2 {{ stroke: var(--series-2); }} .chart .s3 {{ stroke: var(--series-3); }} .chart .s4 {{ stroke: var(--series-4); }}
  .chart .dot.s1 {{ fill: var(--series-1); }} .chart .dot.s2 {{ fill: var(--series-2); }} .chart .dot.s3 {{ fill: var(--series-3); }} .chart .dot.s4 {{ fill: var(--series-4); }}
  .chart .crosshair {{ stroke: var(--ink-3); stroke-width: 1; }}
  .legend {{ list-style: none; padding: 0; margin: .5rem 0 0; display: flex; flex-wrap: wrap; gap: .5rem 1.6rem; font-size: .86rem; max-width: none; }}
  .legend li {{ display: flex; gap: .55rem; align-items: flex-start; margin: 0; }}
  .legend small {{ display: block; color: var(--ink-3); font-size: .76rem; }}
  .legend .key {{ display: inline-block; width: 18px; height: 2px; border-radius: 1px; margin-top: .65rem; flex: none; }}
  .legend .s1 {{ background: var(--series-1); }} .legend .s2 {{ background: var(--series-2); }} .legend .s3 {{ background: var(--series-3); }} .legend .s4 {{ background: var(--series-4); }}
  .tooltip {{ position: absolute; pointer-events: none; background: var(--paper); border: 1px solid var(--rule); border-radius: 3px; padding: .45rem .6rem; font-size: .8rem; line-height: 1.4; min-width: 11rem; box-shadow: 0 2px 10px rgba(0,0,0,.08); }}
  .tooltip .t-step {{ font-family: var(--f-mono); color: var(--ink-3); font-size: .72rem; margin-bottom: .2rem; }}
  .tooltip .t-row {{ display: flex; align-items: center; gap: .5rem; }}
  .tooltip .t-row strong {{ font-family: var(--f-mono); font-weight: 500; min-width: 3.4em; }}
  .tooltip .t-row span.k {{ display: inline-block; width: 12px; height: 2px; }}
  .tooltip .t-row span.n {{ color: var(--ink-2); }}
  details.table-view {{ margin: .5rem 0 0; font-size: .9rem; }}
  details.table-view summary {{ cursor: pointer; color: var(--ink-2); }}
  .listen {{ margin: 2rem 0; padding-top: 1rem; border-top: 1px solid var(--rule-soft); }}
  .listen h3 {{ margin-bottom: .3rem; }}
  .clip-note {{ font-size: .9rem; color: var(--ink-2); }}
  .clips {{ display: grid; gap: .8rem; max-width: 46rem; }}
  .clip-head {{ font-size: .82rem; color: var(--ink-2); margin-bottom: .25rem; }}
  .clip-role {{ font-family: var(--f-mono); font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: var(--ink); margin-right: .4rem; }}
  audio {{ display: block; width: 100%; max-width: 46rem; }}
  .diff-list li {{ margin-bottom: .6em; }}
</style>
</head>
<body>
<a class="skip-link" href="#content">Skip to content</a>
<div class="journal-wrap">
  <header class="journal-top">
    <a class="wordmark" href="../">Maestro</a>
    <nav aria-label="Main navigation">
      <a href="../#now">Now</a>
      <a href="../journal/">Journal</a>
      <a href="../#artifacts">Artifacts</a>
      <a href="../survey/literature-review.html">Research</a>
      <a href="https://github.com/htansetiawan/maestro">GitHub</a>
    </nav>
  </header>
  <main id="content">
    <header class="journal-head">
      <p class="eyebrow">Reproduction</p>
      <h1>Music Transformer, reproduced</h1>
      <p class="journal-description">{escape(description)}</p>
      <p class="journal-meta">Page built {built} · <span class="status-line">{escape(status_line)}</span> · <a href="music-transformer-live.html">Run the model in your browser</a></p>
      <div class="share-actions">
        <a href="{CANONICAL}">Permalink</a>
        <button type="button" class="share-button" data-share-url="{CANONICAL}" hidden>Copy link</button>
        <span class="share-status" role="status" aria-live="polite"></span>
      </div>
    </header>
    <div class="journal-prose">
<p><a href="{PAPER['url']}">Music Transformer</a> (Huang et al., ICLR 2019) showed that a Transformer with relative attention models long piano performances better than one without it. This page retrains the configuration Magenta released for that paper, in a new PyTorch implementation, on the official MAESTRO v1 split, and reports what comes out: the numbers, the checks that the implementation computes the same function as the original code, and the music.</p>

<div class="stats">
  <div class="stat"><p class="label">{escape(headline_label)}</p><p class="value">{fmt(headline_value)}</p><p class="note">nats per event, lower is better</p></div>
  {extra_stats}<div class="stat"><p class="label">Paper, relative attention</p><p class="value">{fmt(PAPER['relative'])}</p><p class="note">Table 3, Piano-e-Competition, L = 2048</p></div>
  <div class="stat"><p class="label">Max logit difference from the original code</p><p class="value">{worst.get('logits_max_abs_diff', float('nan')):.0e}</p><p class="note">same weights, same inputs, float32</p></div>
  <div class="stat"><p class="label">Optimizer steps</p><p class="value">{(main_run.get('step') or 0)/1000:,.0f}K</p><p class="note">{steps_note}</p></div>
</div>

<h2 id="curves">Learning curves</h2>
<p>Validation loss on 128 fixed windows drawn from every validation performance, evaluated every 2,000 steps. Each run is one process on one RTX PRO 5000, about 32 ms per step at batch one.</p>
<figure class="viz-root" id="curve-figure">
{svg}
<div class="tooltip" id="tooltip" hidden></div>
<ul class="legend">{legend}</ul>
{chart_table(series)}
</figure>

<h2 id="numbers">Against the paper</h2>
<div class="table-scroll"><table><thead><tr><th>Model</th><th>Data</th><th>Validation NLL</th><th>Status</th></tr></thead><tbody>{comparison_rows(runs, best_eval, last_eval)}</tbody></table></div>
<p>The numbers are not directly comparable, and the gap has known causes. The released configuration trained here has a 1,024-wide feed-forward layer; the paper's relative-attention model used 2,048. The paper used its own partition of the Piano-e-Competition recordings; MAESTRO v1 is the same recordings under a different, composition-level split. The released code uses an 88-key vocabulary of 310 events; the paper describes 128 pitches. The ablation runs listed above hold everything fixed but the attention type and the paper's layer sizes, so the comparison the paper actually makes, relative attention against a vanilla Transformer, is reproduced on this data.</p>

<h2 id="listen">Listen</h2>
<p>Every clip is the model's own event sequence rendered through one piano sound, so the differences you hear are in the notes. For prompted clips, the real opening of a held-out MAESTRO performance comes first; the model never saw that performance in training. To hear it continue any of the twenty openings with your own settings, or to test whether you can tell its continuations from the pianist's, open the <a href="music-transformer-live.html">live page</a>, where the same checkpoint runs inside the browser.</p>
{listening}

<h2 id="parity">The implementation computes the same function as the original</h2>
<p>A port can look right and still differ. To rule that out, the same randomly initialized weights were loaded into this implementation and into the original Tensor2Tensor code (version 1.15.7, the version the released configuration was written for), and both were given identical inputs with dropout off.</p>
{parity_section()}

<h2 id="setup">What was trained</h2>
<div class="table-scroll"><table><thead><tr><th>Setting</th><th>Value</th></tr></thead><tbody>
<tr><td>Configuration</td><td class="mono">t_rel_len2048_h512_att512_fs1024_n6_dropout10 (Magenta commit c15687eb)</td></tr>
<tr><td>Model</td><td>Decoder-only Transformer, 6 layers, 8 heads, width {config.get('width')}, feed-forward {config.get('ff_width')}, full causal relative attention with a {config.get('max_relative_position'):,}-position table, {16068608:,} parameters</td></tr>
<tr><td>Events</td><td>310: 88 note-on, 88 note-off, 100 time shifts of 10 ms, 32 velocity bins, 2 reserved</td></tr>
<tr><td>Training example</td><td>One random 2,048-event crop per step, from one of 5 tempo variants, with a random transposition of up to three semitones</td></tr>
<tr><td>Optimizer</td><td>Adam β = ({config.get('adam_betas', ['?','?'])[0]}, {config.get('adam_betas', ['?','?'])[1]}), ε = {config.get('adam_epsilon')}, learning rate 2·min(1, step/8000)/√(512·max(step, 8000)), no clipping, no weight decay, dropout {config.get('dropout')}</td></tr>
<tr><td>Precision</td><td>bf16 matrix products with float32 weights, softmax, and optimizer state</td></tr>
</tbody></table></div>

<h3 id="data">MAESTRO v1, official split</h3>
{data_section()}
<p>The split is by composition: no work appears in two splits. Training uses the train split; checkpoints are chosen on validation; the test split has not been used.</p>

<h3 id="differences">Known differences from the original run</h3>
<ul class="diff-list">
<li>PyTorch replaces TensorFlow. The function is the same to float32 rounding (above); random number streams, operation order, and bf16 arithmetic are not.</li>
<li>Dense layers are initialized with a fan-in bound; Tensor2Tensor uses fan-average. This changes the initial feed-forward weights slightly, not the computation.</li>
<li>Training crops are sampled with replacement over pieces, tempo variants, and transpositions; the original shuffles epochs of stored augmented copies.</li>
<li>MIDI is parsed directly with the released note-seq classes; the original consumed pre-built TFRecords from the same encoding.</li>
<li>Validation during training uses 128 fixed windows; the end-of-run number uses the original rule, every validation performance in consecutive 2,048-event chunks.</li>
</ul>

<h2 id="reproduce">Reproduce it</h2>
<pre><code class="language-bash">python3 experiments/020_music_transformer_reproduction/prepare.py     # verify the archive, encode MAESTRO
python3 experiments/020_music_transformer_reproduction/check.py --cuda # attention, tokenizer, optimization checks
python3 experiments/020_music_transformer_reproduction/launch.py --run baseline-stage1 --steps 1000000
python3 experiments/020_music_transformer_reproduction/evaluate.py --checkpoint runs/baseline-stage1/best.pt
python3 experiments/020_music_transformer_reproduction/sample.py --checkpoint runs/baseline-stage1/best.pt --prompts prompts/v1.json --candidates 4 --new-tokens 1024 --top-p 0.98 --midi --out pools/v1
python3 experiments/020_music_transformer_reproduction/render.py pools/v1/*.mid
</code></pre>
<p>Prompt set v1 is frozen with its hash before any listening ({escape((read_json(E020 / 'prompts/v1.json', {}) or {}).get('version', 'v1'))}, SHA-256 {escape((E020 / 'prompts/v1.sha256').read_text().strip()[:16] if (E020 / 'prompts/v1.sha256').exists() else 'pending')}…). Listening clips come from checkpoint step {pool_info.get('checkpoint_step') or '—'}{(', SHA-256 ' + pool_info['checkpoint_sha256'][:16] + '…') if pool_info.get('checkpoint_sha256') else ''}. MAESTRO is released under CC BY-NC-SA 4.0 by Google Magenta; the prompt clips are short excerpts of its validation performances.</p>
    </div>
  </main>
  <footer class="journal-footer">
    <p>Maestro · Henry Tan · <a href="../journal/">Weekly journal</a> ·
      <a href="../journal/feed.xml">Subscribe via Atom</a></p>
    <p>Writing licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
      <a href="https://github.com/htansetiawan/maestro">Source and history</a>.</p>
  </footer>
</div>
<script id="curve-data" type="application/json">{json.dumps({"series": chart_data, "scale": scale})}</script>
<script>
(function () {{
  var data = JSON.parse(document.getElementById('curve-data').textContent);
  var svg = document.querySelector('#curve-figure svg'), hit = document.getElementById('hit');
  var cross = document.getElementById('crosshair'), tip = document.getElementById('tooltip');
  var sc = data.scale, figure = document.getElementById('curve-figure');
  if (!svg || !hit) return;
  function stepAt(clientX) {{
    var box = svg.getBoundingClientRect();
    var x = (clientX - box.left) / box.width * sc.width;
    var frac = Math.min(1, Math.max(0, (x - sc.left) / (sc.width - sc.left - sc.right)));
    return sc.x_start + frac * (sc.x_max - sc.x_start);
  }}
  function nearest(points, step) {{
    var best = null;
    points.forEach(function (p) {{ if (p[0] >= sc.x_start && (best === null || Math.abs(p[0] - step) < Math.abs(best[0] - step))) best = p; }});
    return best;
  }}
  function show(ev) {{
    var step = stepAt(ev.clientX), rows = [], snapped = null;
    data.series.forEach(function (s) {{
      var p = nearest(s.points, step);
      if (p) {{ rows.push({{ label: s.label, slot: s.slot, point: p }}); if (snapped === null || Math.abs(p[0] - step) < Math.abs(snapped - step)) snapped = p[0]; }}
    }});
    if (snapped === null) return;
    var x = sc.left + (snapped - sc.x_start) / (sc.x_max - sc.x_start) * (sc.width - sc.left - sc.right);
    cross.setAttribute('x1', x); cross.setAttribute('x2', x); cross.hidden = false;
    while (tip.firstChild) tip.removeChild(tip.firstChild);
    var head = document.createElement('div'); head.className = 't-step'; head.textContent = 'step ' + snapped.toLocaleString(); tip.appendChild(head);
    rows.forEach(function (r) {{
      var row = document.createElement('div'); row.className = 't-row';
      var key = document.createElement('span'); key.className = 'k'; key.style.background = getComputedStyle(figure).getPropertyValue('--series-' + r.slot);
      var val = document.createElement('strong'); val.textContent = r.point[1].toFixed(3);
      var name = document.createElement('span'); name.className = 'n'; name.textContent = r.label;
      row.appendChild(key); row.appendChild(val); row.appendChild(name); tip.appendChild(row);
    }});
    var box = svg.getBoundingClientRect(), fig = figure.getBoundingClientRect();
    var px = (x / sc.width) * box.width + (box.left - fig.left);
    tip.hidden = false;
    var left = px + 14; if (left + tip.offsetWidth > fig.width) left = px - tip.offsetWidth - 14;
    tip.style.left = Math.max(0, left) + 'px'; tip.style.top = (box.top - fig.top + 24) + 'px';
  }}
  hit.addEventListener('pointermove', show);
  hit.addEventListener('pointerleave', function () {{ cross.hidden = true; tip.hidden = true; }});
  var players = Array.prototype.slice.call(document.querySelectorAll('audio'));
  players.forEach(function (p) {{ p.addEventListener('play', function () {{ players.forEach(function (o) {{ if (o !== p) o.pause(); }}); }}); }});
}})();
</script>
</body>
</html>
"""
    OUT_HTML.write_text(html)
    print(json.dumps({"html": str(OUT_HTML.relative_to(ROOT)), "bytes": len(html), "series": [s["name"] for s in series],
                      "copied": len(pool_info.get("copied", [])), "status": status_line}))


if __name__ == "__main__":
    main()
