# Publishing the Maestro journal

The landing page shows the newest published entry’s state and links to the current artifacts.
Each dated entry gets a permanent URL, an Atom item, and frozen copies of its attached documents.
This workflow publishes actual progress; it does not automatically invent or schedule weekly updates.

Install the small journal builder dependency once:

```bash
python3 -m pip install -r requirements-site.txt
```

Start an entry for a real publication date:

```bash
python3 scripts/build_journal.py new 2026-09-17 --title "What changed this week"
```

Write `journal/entries/2026-09-17.md`. Fill its summary, stage, focus, and next step in
`journal/content.json`. Include what changed, current thinking, findings with evidence,
artifacts, open questions, and the next experiment. Mark intended work as planned and
measurements as measured. New entries remain drafts and do not appear on the site or feed.
Draft source files follow the repository’s visibility; drafts are not access-controlled documents.

Update the current artifact Markdown files if the position has changed. New artifacts can be
registered in the `artifacts` list in `journal/content.json`; use a stable ID and repository-relative
source path. Choose which IDs to attach to the entry. A standalone HTML page with its own media (a listening page, a live demo) is registered with `page` (its repository-relative HTML path) instead of `source`; it gets a card but is not frozen into snapshots.

Put a short “find the work” section near the top of technical entries with direct
GitHub links to code, configuration, and a public results index. Artifact cards
automatically link both to the rendered site page and its GitHub Markdown source;
dated cards link to the frozen snapshot source. When audio is available, add
rights-cleared listening links to the experiment's public results index and link
that index from the entry. Mark missing recordings or results as pending rather
than linking to ignored local `artifacts/` paths.
The newest entry may also define a short `links` list (`label` and HTTPS `url`) in
`journal/content.json`; those links appear immediately on the journal landing
page and homepage. Refresh that list as the public experiment advances.

Publish and freeze that week’s artifact versions:

```bash
python3 scripts/build_journal.py publish 2026-09-17
```

This creates `journal/snapshots/2026-09-17/`, marks the entry published, and rebuilds the site.
It does not commit or push. Review the generated pages, then commit and push to publish through
GitHub Pages. Do not edit snapshot Markdown or snapshot metadata to reflect later changes;
write the next entry instead. If correcting an earlier entry, clearly date the correction in its text.

To rebuild without publishing another entry:

```bash
./build.sh --journal
```

This builds current artifact pages, the archive, dated entries, snapshots, the Atom feed, and
the marked current-state block in `index.html`. It leaves the older survey pages alone.
`./build.sh` additionally rebuilds the survey and requires pandoc. The studio is ordinary HTML,
CSS, and JavaScript with no separate build step.

Before pushing, check internal links and browse the pages at desktop and mobile widths:

```bash
python3 scripts/check_site.py
python3 -m http.server 8000
```

Open `http://localhost:8000/`, `journal/`, and `studio/`. Share the dated journal URL to discuss a
particular week; share an artifact URL for its current version or a snapshot URL for the historical
version. Generated HTML is committed so the site works with GitHub Pages’ static branch publishing.

The browser regression script checks phrase preservation, pinning, drawing controls, tapping,
recipe execution, undo, version comparison, saved sessions, downloads, and mobile layout:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/test_studio.py
```

Run it while the local server is active. `MAESTRO_BASE_URL` changes the server URL;
`MAESTRO_CHROMIUM_PATH` optionally selects a local Chromium binary. Screenshots and sample
downloads go to `/tmp/maestro-browser-check`, or `MAESTRO_TEST_OUTPUT` when specified.
