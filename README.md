# Maestro

**Building Music Kitchen in public: a personal arranging studio for human-led music creation.**

> Play the part you know. Shape the rest.

Bring piano, lyrics, and musical ideas; direct the rest of the arrangement through sound,
examples, and gestures. The product comes first. Research follows the problems encountered
while making that experience work.

- **[Try the studio](https://htansetiawan.github.io/maestro/studio/)** — a playable browser
  experiment with phrase selection, contour drawing, rhythm tapping, an editable recipe,
  before/after comparison, undo, and WAV/project export. It uses procedural synthesis;
  trained multimodal generation and humming transcription are not connected.
- **[Explore Music Anatomy](https://htansetiawan.github.io/maestro/anatomy/)** — an interactive
  ACE-Step pipeline atlas, representation explorer, flow-matching lab, and symbolic compiler
  with playback and MIDI/MusicXML export. Includes the recorded vocal experiment and primary sources.
- **[Weekly journal](https://htansetiawan.github.io/maestro/journal/)** — dated decisions,
  positioning, findings, open questions, experiments, and frozen artifact snapshots.
- **[Hear the first ACE vocal experiment](experiments/002_ace_piano_vocals/README.md)**
  — a generated singer over a supplied solo piano recording, with original lyrics
  about the Yard, downloadable audio, and the generation record.
- **[Current product brief](https://htansetiawan.github.io/maestro/artifacts/music-kitchen-product.html)**
  — the intended experience and first product milestone.
- **[Maestro landing page](https://htansetiawan.github.io/maestro/)** — current state and
  the full set of working artifacts. **[Atom feed](https://htansetiawan.github.io/maestro/journal/feed.xml)**.

## Run the prototype locally

The studio is plain HTML, CSS, and JavaScript. From the repository root, run:

```bash
python3 -m http.server 8000
```

Open [the studio](http://localhost:8000/studio/) or [the landing page](http://localhost:8000/).
Generated pages are committed, so previewing the existing site requires no build step.

## Project structure

| Path | Purpose |
|---|---|
| `studio/` | Playable browser prototype with procedural synthesis |
| `anatomy/` | Interactive ACE-Step research atlas and symbolic music compiler |
| `research/MUSIC-KITCHEN-PRODUCT.md` | Current product brief |
| `research/STUDIO-EXPERIMENT.md` | Implemented prototype behavior and limitations |
| `journal/entries/` | Source for dated progress updates |
| `journal/content.json` | Journal metadata and artifact registry |
| `journal/snapshots/` | Frozen artifacts attached to published entries |
| `artifacts/` | Generated pages for current working documents |
| `research/` | Research sources, evidence notes, and generation scripts |
| `survey/` | Generated literature survey pages |
| `scripts/` | Journal builder and site checks |

To publish an update, follow **[the journal publishing guide](journal/README.md)**.
Publishing an entry freezes its attached documents, renders pages, and updates the landing
page and feed. It does not automatically write weekly entries.

## Research foundation

The project began with the following literature survey. It remains a research foundation;
the product brief and weekly journal carry the current direction.

| Resource | Contents |
|---|---|
| **[Literature review](https://htansetiawan.github.io/maestro/survey/literature-review.html)** | 43,900 words · 398 works cited · thirteen sections following the loop |
| **[Taxonomy](https://htansetiawan.github.io/maestro/survey/taxonomy.html)** | 49 nodes, 10 coding dimensions — the frame the review follows |
| **[Annotated bibliography](https://htansetiawan.github.io/maestro/survey/annotated-bibliography.html)** | 394 records with evidence and verification level |
| **[references.bib](research/references.bib)** | 398 BibTeX entries; every key resolves through pandoc citeproc |

Corpus: **463 annotated entries, 1957–2026**, assembled across eight research clusters in
September 2026.

### Working material

- `research/notes/01–08*.md` — the eight raw research clusters. **This is the ground truth.**
  Every claim in the review traces to an entry here, and each entry carries a verification
  level: *verified* (a primary source was fetched), *partial* (secondary sources only), or
  *unverified* (recall, not re-confirmed). 373 verified, 85 partial, 5 unverified.
- `research/taxonomy-map.{md,csv}` — every entry assigned to a primary node (462 hand-coded).
- `research/VERIFICATION.md` — an independent pass re-checking 34 high-stakes claim clusters
  against primary sources. 16 corrections, all applied.
- `research/AUDIT.md` — internal-consistency audit: claim traceability, hedging discipline,
  contradictions, redundancy, citation hygiene. 70 findings.
- `research/CHANGELOG.md` — exactly which of the 56 fixes were applied, and which were left.
- `research/bib/` — per-cluster BibTeX before merging.

### Earlier survey findings

These are historical survey conclusions, not the current product specification. Some broad
claims below were challenged by later evidence; consult the [positioning evidence](research/AI-MUSIC-POSITIONING-EVIDENCE.md)
and the [product brief](research/MUSIC-KITCHEN-PRODUCT.md) for the updated framing.

1. **Infilling under hard constraints — not generation from scratch — is the primitive that
   implements the loop.** Mature since Coconet (2017), which framed it as modelling how
   composers "write music in a nonlinear fashion, scribbling motifs here and there, often
   revisiting choices previously made." The best deployment evidence is Hookpad Aria's: ~23%
   of 318,000 span-level suggestions accepted by ~3,000 users inside a notation editor.
2. **Interface steerability moves control and ownership at least as much as model capability
   does.** The two controlled studies that varied both found the gains complementary, not
   substitutable.
3. **Every input modality that works routes through an editable symbolic representation.**
   Straight-to-audio is impressive and uncorrectable.
4. **The annotation layer is the field's genuine white space.** The pieces exist — MEI and
   Dezrann anchoring, analysis models that propose labels, a converged control vocabulary,
   ExpressEdit's reference grammar — and have never been assembled for music.
5. **Symbolic-first, human-authored work sits on materially better legal ground** than
   prompt-to-audio, and licence-clean symbolic training data genuinely exists.

### Earlier research directions

The original survey identified twelve gaps, each naming the nearest prior art —
**[full list on the site](https://htansetiawan.github.io/maestro/#directions)**.
These are historical research questions; the product brief carries the current priorities.
Examples from that survey:

- **G1** Annotations as a compilable instruction set on notation *(S2.4 — 4 entries in the
  corpus, none of them music)*
- **G2** A lossless bridge between an LLM-friendly text IR and engraving-grade notation
  *(no verified system generates MusicXML or MEI natively)*
- **G5** A return channel: the compiler's build log *(S4.4 — 2 entries)*
- **G7** Composer-controllable audio rendering *(no commercial system takes MIDI or chords as
  a generation condition)*

## Link previews

`index.html` and the survey pages carry a full Open Graph + Twitter card set, so links
unfurl properly in iMessage, WhatsApp, Signal, Slack, Discord, LinkedIn and X.

- **Card image:** `assets/og-cover.png` — 1200×630, 62 KB (comfortably under WhatsApp's limit).
- **Source:** `assets/og-image.html`. Icons come from `assets/icon.html`.
- **Regenerate:** `./build-og.sh` (needs `npm i playwright` and ImageMagick).

Two things to know. `og:image` **must be an absolute URL** — scrapers do not resolve relative
paths — so it is hard-coded to `https://htansetiawan.github.io/maestro/`; change it in
`index.html` and `assets/doc.template.html` if the site ever moves. And the shipped PNG was
rendered without network access, so it uses Charter rather than Newsreader; re-running
`./build-og.sh` on a machine that can reach Google Fonts produces the card in the real faces.

**Previews are cached hard.** After the first share, iMessage and WhatsApp will keep serving the
old card. To force a refresh: share `...maestro/?v=2`, or clear the cache — Facebook's
[sharing debugger](https://developers.facebook.com/tools/debug/) re-scrapes for most platforms,
and [opengraph.xyz](https://www.opengraph.xyz/) is a quick way to see what a scraper sees.

## Building the site

The site is served as static HTML through GitHub Pages. To rebuild the journal and current
artifact pages, install the Python dependency and run:

```bash
python3 -m pip install -r requirements-site.txt
./build.sh --journal
python3 scripts/check_site.py
python3 scripts/test_journal.py
```

This also rebuilds the journal archive, dated entries, snapshot pages, Atom feed, and the
marked current-state block in `index.html`. It requires no pandoc. The studio has no build step.

To additionally render the literature review, taxonomy, annotated bibliography, and positioning
document into `survey/`, install pandoc 3 or later and run:

```bash
./build.sh
```

`assets/site.css` carries the shared identity; `assets/doc.template.html` is the survey's
pandoc template. GitHub Pages serves from the repository root (`.nojekyll` is present so
nothing is filtered). Review and commit generated pages along with their source changes.

Browser regression setup and commands are in the [journal guide](journal/README.md).

To regenerate the research artefacts themselves from the source notes:

```bash
cd research
python3 merge_bib.py       # bib/*.bib     → references.bib + bib_aliases.json
python3 build_map.py       # notes/*.md    → taxonomy-map.{md,csv}
python3 build_annobib.py   # notes/*.md    → annotated-bibliography.md
python3 assemble.py        # sections/*.md → literature-review.md
```

## Contributing

**Corrections are the most valuable contribution.** Every claim is traceable to a source note,
so a correction can be checked rather than argued. Open an issue with the section, the claim as
written, and the primary source that contradicts it.

Also welcome: works the survey missed (say which taxonomy node they belong to), disagreement
with the gap analysis, and replication of anything in §10.

## Citing

See [`CITATION.cff`](CITATION.cff).

```bibtex
@misc{tan2026maestro,
  author = {Tan, Henry},
  title  = {Maestro: Human-Centered {AI} for Composition --- A Literature Review and Taxonomy},
  year   = {2026},
  url    = {https://htansetiawan.github.io/maestro/},
  note   = {Survey of 463 works, 1957--2026}
}
```

## Licence

Prose, survey and research notes: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code, scripts and templates: Apache 2.0 (see [`LICENSE`](LICENSE)). Full detail: [`LICENSE-TEXT.md`](LICENSE-TEXT.md).

---

Henry Tan · Harvard University · survey compiled September 2026
