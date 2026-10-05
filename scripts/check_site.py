#!/usr/bin/env python3
"""Check local links, anchors, duplicate IDs, and metadata on the published surfaces."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.ids, self.duplicates, self.meta = [], set(), [], set()
        self.canonical = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        if tag in {"a", "link", "script", "img"}:
            href = attrs.get("href") or attrs.get("src")
            if href:
                self.links.append(href)
        if tag == "meta":
            self.meta.add(attrs.get("name") or attrs.get("property"))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = True


def main():
    paths = [ROOT / "index.html"] + sorted((ROOT / "journal").rglob("*.html"))
    paths += sorted((ROOT / "artifacts").glob("*.html")) + [ROOT / "studio/index.html", ROOT / "anatomy/index.html"]
    parsed, errors = {}, []
    for path in paths:
        page = parsed.setdefault(path, Page(path))
        if page.duplicates:
            errors.append(f"{path.relative_to(ROOT)}: duplicate IDs {page.duplicates}")
        if not page.canonical or not {"viewport", "description", "og:title", "og:description", "og:image"}.issubset(page.meta):
            errors.append(f"{path.relative_to(ROOT)}: incomplete share metadata")
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing {href}")
            elif url.fragment and target.suffix == ".html":
                other = parsed.setdefault(target, Page(target))
                if unquote(url.fragment) not in other.ids:
                    errors.append(f"{path.relative_to(ROOT)}: missing anchor {href}")
    ET.parse(ROOT / "journal/feed.xml")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked {len(paths)} pages: local links, anchors, IDs, sharing metadata, and Atom XML passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
