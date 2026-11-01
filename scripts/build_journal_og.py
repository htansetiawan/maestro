#!/usr/bin/env python3
"""Link-preview cards (1200x630 PNG) for journal entries, so a shared entry shows its own
title in iMessage, WhatsApp and Slack instead of the site cover.

    python3 scripts/build_journal_og.py            # every published entry without a card
    python3 scripts/build_journal_og.py --force    # redraw them all

Writes journal/og/<date>.png. An entry with its own `og_image` in journal/content.json
keeps that image and gets no card. Needs Chrome or Chromium (set CHROME to its path).
Run before ./build.sh --journal, which points each page's og:image at its card.
"""
import argparse, json, os, re, shutil, subprocess, tempfile
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CARD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>
:root{--paper:#F2F3EF;--ink:#14161A;--ink-2:#545962;--ink-3:#838892;--rule:#CDD1CA;--annot:#A5352B}
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:630px}
body{background:var(--paper);color:var(--ink);font-family:"Archivo","TeX Gyre Heros","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
.card{width:1200px;height:630px;padding:62px 72px 0;position:relative}
.eyebrow{font-family:"IBM Plex Mono","DejaVu Sans Mono",Menlo,monospace;font-size:17px;letter-spacing:.19em;text-transform:uppercase;color:var(--ink-3)}
h1{font-family:"Newsreader","Bitstream Charter","Charter",Georgia,serif;font-weight:500;font-size:__SIZE__px;line-height:1.04;letter-spacing:-.015em;margin:22px 0 26px;max-width:1056px}
p{font-family:"Newsreader","Bitstream Charter","Charter",Georgia,serif;font-size:30px;line-height:1.32;color:var(--ink-2);max-width:1040px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.foot{position:absolute;left:72px;right:72px;bottom:40px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono","DejaVu Sans Mono",Menlo,monospace;font-size:18px;color:var(--ink-3);border-top:1px solid var(--rule);padding-top:16px}
.foot b{color:var(--ink-2);font-weight:500}
</style></head><body><div class="card">
<div class="eyebrow">Maestro · Weekly journal · __DATE__</div>
<h1>__TITLE__</h1>
<p>__LEDE__</p>
<div class="foot"><span><b>Henry Tan</b> · htansetiawan.github.io/maestro</span><span>journal</span></div>
</div></body></html>"""


def lede(summary):
    first = re.split(r"(?<=[.;])\s", summary.strip(), maxsplit=1)[0].rstrip(";")
    return first if len(first) <= 230 else first[:227].rsplit(" ", 1)[0] + "…"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    chrome = os.environ.get("CHROME") or next((shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
    if not chrome:
        raise SystemExit("needs Chrome or Chromium; set CHROME")
    entries = [e for e in json.loads((ROOT / "journal/content.json").read_text())["entries"] if e.get("published") and not e.get("og_image")]
    out = ROOT / "journal/og"; out.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for e in entries:
            png = out / f"{e['date']}.png"
            if png.exists() and not a.force:
                continue
            title = e["title"]
            size = 72 if len(title) <= 48 else 60 if len(title) <= 80 else 50
            html = (CARD.replace("__SIZE__", str(size)).replace("__TITLE__", escape(title))
                    .replace("__LEDE__", escape(lede(e.get("summary", ""))))
                    .replace("__DATE__", date.fromisoformat(e["date"]).strftime("%B %-d, %Y")))
            src = Path(tmp) / f"{e['date']}.html"; src.write_text(html)
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,630",
                            "--virtual-time-budget=2000", f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
            print("  →", png.relative_to(ROOT))


if __name__ == "__main__":
    main()
