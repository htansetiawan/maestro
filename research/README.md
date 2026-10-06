# Research working material

Ground truth for everything published on the [Maestro site](https://htansetiawan.github.io/maestro/).

| Path | What it is |
|---|---|
| [CORE-MUSIC-GENERATION-REFERENCES.md](CORE-MUSIC-GENERATION-REFERENCES.md) | A curated 52-reference reading list for understanding music generation, with primary links, a 17-paper first pass, and symbolic score ↔ audio foundations. |
| `notes/01–08*.md` | The eight raw research clusters, 463 entries. Every claim in the review traces to an entry here. Each carries a **verification level** — *verified* (primary source fetched), *partial* (secondary only), *unverified* (recall). |
| `literature-review.md` | The assembled review, 13 sections. Rendered to `../survey/`. |
| `taxonomy.md` | 49 nodes, 10 dimensions, the studio's design position, 12 gaps. |
| `annotated-bibliography.md` | 394 merged records, generated from `notes/` by `build_annobib.py`. |
| `references.bib` | 398 records, merged from `bib/` by `merge_bib.py`. |
| `taxonomy-map.{md,csv}` | Every entry assigned to a primary node (462 hand-coded, 1 auto). |
| `VERIFICATION.md` | Independent primary-source re-check of 34 high-stakes claim clusters. |
| `AUDIT.md` | Internal-consistency audit: traceability, hedging, contradictions, redundancy, citations. |
| `CHANGELOG.md` | The 56 applied fixes, and what was deliberately left. |
| `sections/` | The review split by section — edit here, then `assemble.py`. |

## Regenerating

```bash
python3 merge_bib.py       # bib/*.bib     → references.bib + bib_aliases.json
python3 build_map.py       # notes/*.md    → taxonomy-map.{md,csv}
python3 build_annobib.py   # notes/*.md    → annotated-bibliography.md
python3 assemble.py        # sections/*.md → literature-review.md
```

Then `../build.sh` renders the HTML.

## Reading the verification levels

Treat figures from *partial* and *unverified* entries as indicative. The review hedges them in
prose; `AUDIT.md` §2 lists every place that discipline was checked. 373 entries are verified,
85 partial, 5 unverified.
