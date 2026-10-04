#!/usr/bin/env bash
# Maestro — render the research documents into the Pages site.
# Requires pandoc >= 3. Source markdown lives in research/ ; output goes to survey/.
set -euo pipefail
cd "$(dirname "$0")"

# The journal and studio are static; this path needs Python, not pandoc.
python3 scripts/build_journal.py
if [[ "${1:-}" == "--journal" ]]; then
  exit 0
fi

SRC=research
OUT=survey
TPL=assets/doc.template.html
BIB=$SRC/references.bib

mkdir -p "$OUT"
cp -f "$BIB" "$OUT/references.bib"

render () {  # render <src.md> <out.html> [--toc]
  local src="$1" out="$2"; shift 2
  pandoc "$src" \
    --from markdown+smart \
    --to html5 \
    --standalone \
    --template "$TPL" \
    --citeproc \
    --bibliography "$BIB" \
    --section-divs \
    --wrap=preserve \
    "$@" \
    --output "$OUT/$out"
  echo "  → $OUT/$out"
}

echo "Rendering:"
render "$SRC/literature-review.md"      literature-review.html      --toc --toc-depth=2
render "$SRC/taxonomy.md"               taxonomy.html               --toc --toc-depth=2
render "$SRC/annotated-bibliography.md" annotated-bibliography.html --toc --toc-depth=1
render "$SRC/POSITIONING.md"             positioning.html            --toc --toc-depth=1
render "$SRC/TECHNICAL-REPORT.md"        technical-report.html       --toc --toc-depth=2 --mathjax
echo "Done. Open index.html."
