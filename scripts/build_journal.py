#!/usr/bin/env python3
"""Build static journal pages, current artifacts, immutable artifact snapshots, and Atom.

python3 scripts/build_journal.py
python3 scripts/build_journal.py new 2026-09-17 --title 'What changed this week'
python3 scripts/build_journal.py publish 2026-09-17
"""
import argparse
from datetime import date, datetime, time, timedelta
from html import escape
import json
import os
from pathlib import Path
import re
from string import Template
from urllib.parse import quote, unquote, urlsplit, urlunsplit
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "journal/content.json"
BASE = "https://htansetiawan.github.io/maestro/"
GITHUB_BLOB = "https://github.com/htansetiawan/maestro/blob/main/"
BEGIN = "<!-- JOURNAL:START -->"
END = "<!-- JOURNAL:END -->"


def load():
    data = json.loads(CATALOG.read_text())
    ids = [a["id"] for a in data["artifacts"]]
    dates = [e["date"] for e in data["entries"]]
    if len(set(ids)) != len(ids) or len(set(dates)) != len(dates):
        raise ValueError("Artifact IDs and journal dates must be unique")
    for artifact in data["artifacts"]:
        if not re.fullmatch(r"[a-z0-9-]+", artifact["id"]):
            raise ValueError("Artifact IDs must be lowercase URL slugs")
        if not (ROOT / artifact["source"]).resolve().is_relative_to(ROOT):
            raise ValueError("Artifact sources must be inside the repository")
    for entry in data["entries"]:
        if date.fromisoformat(entry["date"]).isoformat() != entry["date"]:
            raise ValueError("Journal dates must use YYYY-MM-DD")
        if not set(entry["artifacts"]).issubset(ids):
            raise ValueError(f"Unknown artifact in {entry['date']}")
        for link in entry.get("links", []):
            url = urlsplit(link["url"])
            if not link["label"].strip() or url.scheme != "https" or not url.netloc:
                raise ValueError(f"Invalid quick link in {entry['date']}")
    return data


def save(data):
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def relative(output, target):
    return Path(os.path.relpath(ROOT / target, (ROOT / output).parent)).as_posix()


def label(day):
    return date.fromisoformat(day).strftime("%B %d, %Y").replace(" 0", " ")


def week(day):
    d = date.fromisoformat(day)
    return label((d - timedelta(days=d.weekday())).isoformat())


def write_page(output, title, description, eyebrow, meta, body):
    template = Template((ROOT / "assets/journal.template.html").read_text())
    values = {k: escape(v, quote=True) for k, v in {
        "title": title, "description": description, "eyebrow": eyebrow,
        "canonical": BASE + output, "root": relative(output, "."),
    }.items()}
    values.update(meta=meta, body=body)
    path = ROOT / output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template.substitute(values))


def markdown(source, output, mapping, origin=None):
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    md.renderer.rules["table_open"] = lambda *args: '<div class="table-scroll" role="region" aria-label="Comparison table" tabindex="0"><table>\n'
    md.renderer.rules["table_close"] = lambda *args: '</table></div>\n'
    tokens = md.parse((ROOT / source).read_text())
    if tokens and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
        tokens = tokens[3:]  # The template renders the document title once.
    slugs = set()
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            base = re.sub(r"[^a-z0-9]+", "-", tokens[i + 1].content.lower()).strip("-") or "section"
            slug, n = base, 2
            while slug in slugs:
                slug, n = f"{base}-{n}", n + 1
            slugs.add(slug)
            token.attrSet("id", slug)
        for child in token.children or []:
            attr = "href" if child.type == "link_open" else "src" if child.type == "image" else None
            if not attr:
                continue
            raw = child.attrGet(attr)
            url = urlsplit(raw)
            if url.scheme or url.netloc or not url.path:
                continue
            target = ((ROOT / (origin or source)).parent / unquote(url.path)).resolve()
            destination = mapping.get(target, target)
            child.attrSet(attr, urlunsplit(("", "", relative(output, destination), url.query, url.fragment)))
    return '<div class="journal-prose">' + md.renderer.render(tokens, md.options, {}) + "</div>"


def state(entry):
    fields = [("Stage", "stage"), ("Current focus", "focus"), ("Next experiment", "next_step")]
    return '<dl class="state-grid">' + "".join(
        f"<div><dt>{title}</dt><dd>{escape(entry[key])}</dd></div>" for title, key in fields
    ) + "</dl>"


def entry_list(entries, output):
    items = []
    for e in entries:
        href = relative(output, f"journal/{e['date']}.html")
        items.append(f'<li><time class="journal-date" datetime="{e["date"]}">{label(e["date"])}</time>'
                     f'<h3><a href="{href}">{escape(e["title"])}</a></h3>'
                     f'<p>{escape(e["summary"])}</p><a href="{href}">Read this week’s entry →</a></li>')
    return '<ol class="journal-list">' + "".join(items) + "</ol>"


def quick_links(entry):
    links = entry.get("links", [])
    if not links:
        return ""
    items = "".join(
        f'<li><a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a></li>'
        for link in links
    )
    return ('<nav class="quick-links" aria-label="Open the current work">'
            '<p class="quick-links-title">Open the work</p><ul>' + items + '</ul></nav>')


def artifact_list(artifacts, output, snapshot=None):
    items = []
    for a in artifacts:
        target = f"journal/snapshots/{snapshot}/{a['id']}.html" if snapshot else f"artifacts/{a['id']}.html"
        source = f"journal/snapshots/{snapshot}/{a['id']}.md" if snapshot else a["source"]
        source_url = escape(GITHUB_BLOB + quote(source, safe="/"), quote=True)
        source_label = "Frozen source on GitHub" if snapshot else "Source on GitHub"
        items.append(f'<article class="artifact-item"><p class="artifact-status">{escape(a["status"])}</p>'
                       f'<h3><a href="{relative(output, target)}">{escape(a["title"])}</a></h3>'
                       f'<p>{escape(a["description"])}</p>'
                       f'<p class="artifact-source"><a href="{source_url}">{source_label} ↗</a></p></article>')
    return '<div class="artifact-list">' + "".join(items) + "</div>"


def build():
    data = load()
    entries = sorted((e for e in data["entries"] if e["published"]), key=lambda e: e["date"], reverse=True)
    if not entries:
        raise ValueError("Publish an entry before building the public journal")
    artifacts, latest = data["artifacts"], entries[0]
    mapping = {(ROOT / a["source"]).resolve(): ROOT / f"artifacts/{a['id']}.html" for a in artifacts}
    for a in artifacts:
        output = f"artifacts/{a['id']}.html"
        meta = escape(a["status"]) + f' · <a href="{relative(output, a["source"])}">Markdown source</a>'
        write_page(output, a["title"], a["description"], "Working artifact", meta,
                   markdown(a["source"], output, mapping))
    for i, e in enumerate(entries):
        day, output = e["date"], f"journal/{e['date']}.html"
        snapshot_dir = ROOT / f"journal/snapshots/{day}"
        # Metadata and prose are read from the frozen copy, not today's working artifact.
        frozen = json.loads((snapshot_dir / "catalog.json").read_text())
        frozen_mapping = {(ROOT / a["source"]).resolve(): snapshot_dir / f"{a['id']}.html" for a in frozen}
        for a in frozen:
            dest = f"journal/snapshots/{day}/{a['id']}.html"
            src = f"journal/snapshots/{day}/{a['id']}.md"
            note = (f'<aside class="snapshot-note"><strong>Snapshot from {label(day)}.</strong> '
                    f'This preserves the artifact for <a href="../../{day}.html">this journal entry</a>. '
                    f'<a href="../../../artifacts/{a["id"]}.html">Read the current version</a>.</aside>')
            write_page(dest, a["title"], a["description"], "Dated artifact snapshot",
                       f'{label(day)} · {escape(a["status"])} · <a href="{a["id"]}.md">Snapshot source</a>',
                       note + markdown(src, dest, frozen_mapping, origin=a["source"]))
        body = state(e) + markdown(f"journal/entries/{day}.md", output, frozen_mapping)
        body += '<section aria-labelledby="snapshots"><h2 id="snapshots">Artifacts at this point</h2>'
        body += artifact_list(frozen, output, day) + "</section>"
        body += '<nav class="entry-navigation" aria-label="Journal entries">'
        if i + 1 < len(entries):
            older = entries[i + 1]
            body += f'<a href="{older["date"]}.html">← Earlier: {escape(older["title"])}</a>'
        body += '<a href="./">All entries</a>'
        if i:
            newer = entries[i - 1]
            body += f'<a href="{newer["date"]}.html">Later: {escape(newer["title"])} →</a>'
        body += "</nav>"
        write_page(output, e["title"], e["summary"], f"Weekly journal · week of {week(day)}",
                   f'<time datetime="{day}">{label(day)}</time> · Henry Tan · <a href="entries/{day}.md">Entry source</a>', body)
    write_page("journal/index.html", "The Maestro journal",
               "Weekly notes on building Music Kitchen: the current state, changing positions, findings, experiments, and artifacts.",
               "Working in public", f'Latest entry: {label(latest["date"])} · <a href="feed.xml">Subscribe via Atom</a>',
               '<p>Each entry records what changed, what the evidence supports, what remains open, and what comes next. '
               'Dated artifact snapshots preserve the thinking behind each update.</p>'
               + quick_links(latest) + entry_list(entries, "journal/index.html"))
    homepage = ROOT / "index.html"
    html = homepage.read_text()
    if html.count(BEGIN) != 1 or html.count(END) != 1:
        raise ValueError("Homepage must contain one pair of journal markers")
    generated = (f'<section id="now"><p class="eyebrow">Current state · {label(latest["date"])}</p>'
                 '<h2>Building toward Music Kitchen</h2><p>A personal arranging studio: play piano, write lyrics, '
                 'and shape the rest of the band through sound, examples, and gestures.</p>' + state(latest)
                 + quick_links(latest)
                 + f'<p><a href="journal/{latest["date"]}.html">Read the latest update →</a></p></section>'
                 + '<section id="journal"><h2>The weekly journal</h2><p>A dated record of the work: decisions, '
                 'findings, open questions, experiments, and artifacts you can revisit and share.</p>'
                 + entry_list(entries[:3], "index.html")
                 + '<p><a href="journal/">All journal entries</a> · <a href="journal/feed.xml">Subscribe via Atom</a></p></section>'
                 + '<section id="artifacts"><h2>Positioning and working artifacts</h2>'
                 + '<p>Start with the product brief for the current direction. Earlier positions are kept visible '
                 'so the reasoning can be followed. Weekly entries link to frozen versions.</p>'
                 + artifact_list(artifacts, "index.html") + "</section>")
    before, rest = html.split(BEGIN)
    _, after = rest.split(END)
    homepage.write_text(before + BEGIN + "\n" + generated + "\n" + END + after)
    atom(entries)
    print(f"Built {len(entries)} journal entries, {len(artifacts)} current artifacts, snapshots, homepage, and Atom feed.")


def atom(entries):
    ns = "http://www.w3.org/2005/Atom"
    ET.register_namespace("", ns)
    def add(parent, name, text=None, **attrs):
        node = ET.SubElement(parent, f"{{{ns}}}{name}", attrs)
        node.text = text
        return node
    feed = ET.Element(f"{{{ns}}}feed")
    add(feed, "title", "Maestro weekly journal")
    add(feed, "id", BASE + "journal/")
    add(feed, "link", href=BASE + "journal/", rel="alternate")
    add(feed, "link", href=BASE + "journal/feed.xml", rel="self", type="application/atom+xml")
    timestamp = lambda day: datetime.combine(date.fromisoformat(day), time(), ZoneInfo("America/Los_Angeles")).isoformat()
    add(feed, "updated", timestamp(entries[0]["date"]))
    add(add(feed, "author"), "name", "Henry Tan")
    for e in entries:
        node = add(feed, "entry")
        add(node, "title", e["title"])
        add(node, "id", BASE + f"journal/{e['date']}.html")
        add(node, "link", href=BASE + f"journal/{e['date']}.html")
        add(node, "updated", timestamp(e["date"]))
        add(node, "published", timestamp(e["date"]))
        add(node, "summary", e["summary"])
    ET.indent(feed)
    ET.ElementTree(feed).write(ROOT / "journal/feed.xml", encoding="utf-8", xml_declaration=True)


def new_entry(day, title):
    if date.fromisoformat(day).isoformat() != day:
        raise ValueError("Use YYYY-MM-DD")
    data = load()
    if any(e["date"] == day for e in data["entries"]):
        raise ValueError("An entry already exists for that date")
    path = ROOT / f"journal/entries/{day}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as f:
        f.write(f"# {title}\n\n" + "\n\n".join(f"## {heading}\n\nTODO: Record this week’s actual work." for heading in
                ["What changed", "Current thinking", "Findings and evidence", "Artifacts completed", "Open questions", "Next experiment"]) + "\n")
    data["entries"].append(dict(date=day, title=title, summary="", stage="", focus="", next_step="",
                                artifacts=[a["id"] for a in data["artifacts"]], published=False))
    save(data)
    print(f"Created draft {path.relative_to(ROOT)}. Fill its prose and metadata in journal/content.json, then publish {day}.")


def publish(day):
    data = load()
    e = next((e for e in data["entries"] if e["date"] == day), None)
    if not e or e["published"]:
        raise ValueError("Choose an existing unpublished entry")
    if date.fromisoformat(day) > date.today():
        raise ValueError("Future entries remain drafts until their publication date")
    source = ROOT / f"journal/entries/{day}.md"
    if any(not e[k].strip() for k in ["title", "summary", "stage", "focus", "next_step"]) or "TODO:" in source.read_text():
        raise ValueError("Complete the entry and its state metadata before publishing")
    artifacts = [a for a in data["artifacts"] if a["id"] in e["artifacts"]]
    copies = [(a, (ROOT / a["source"]).read_text()) for a in artifacts]
    destination = ROOT / f"journal/snapshots/{day}"
    destination.mkdir(parents=True, exist_ok=False)
    for a, text in copies:
        (destination / f"{a['id']}.md").write_text(text.rstrip("\n") + "\n")
    (destination / "catalog.json").write_text(json.dumps(artifacts, indent=2, ensure_ascii=False) + "\n")
    e["published"] = True
    save(data)
    build()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("build")
    draft = commands.add_parser("new")
    draft.add_argument("date")
    draft.add_argument("--title", required=True)
    publication = commands.add_parser("publish")
    publication.add_argument("date")
    args = parser.parse_args()
    try:
        if args.command == "new":
            new_entry(args.date, args.title)
        elif args.command == "publish":
            publish(args.date)
        else:
            build()
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"Journal build failed: {exc}\n")
