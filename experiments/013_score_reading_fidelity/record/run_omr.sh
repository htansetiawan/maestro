#!/usr/bin/env bash
# Run three optical music recognition engines on the five scanned pages and
# collect MusicXML per engine. CPU only. Outputs: ../outputs/<engine>/page-N.musicxml
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd); root=$(cd "$here/.." && pwd)
pages=${PAGES_DIR:-$root/source-private/pages}
out=$root/outputs; mkdir -p "$out"
py=~/maestro-runtime/analysis-venv/bin/python
export CUDA_VISIBLE_DEVICES=""          # keep OMR off the shared GPU

echo "== audiveris"
AUD=$(find ~/maestro-runtime/audiveris/extracted -type f -name Audiveris -path "*bin*" | head -1)
if [ -n "$AUD" ]; then
  mkdir -p "$out/audiveris"
  ( time "$AUD" -batch -export -output "$out/audiveris" "$root/source-private/theme_from_the_color_purple.pdf" ) > "$out/audiveris/run.log" 2>&1
  echo "exit $?"; find "$out/audiveris" -name "*.mxl" -o -name "*.xml" | head
else
  echo "Audiveris launcher not found"
fi

echo "== homr"
mkdir -p "$out/homr"
for p in "$pages"/page-*.png; do
  ( time $py -m homr "$p" ) >> "$out/homr/run.log" 2>&1 || echo "homr failed on $p"
  mv -f "${p%.png}.musicxml" "$out/homr/" 2>/dev/null || mv -f "${p%.png}"*.musicxml "$out/homr/" 2>/dev/null
done
ls "$out/homr"

echo "== oemer"
mkdir -p "$out/oemer"
for p in "$pages"/page-*.png; do
  ( time $py -m oemer "$p" -o "$out/oemer" --without-deskew ) >> "$out/oemer/run.log" 2>&1 || echo "oemer failed on $p"
done
ls "$out/oemer"
echo OMR_DONE
