#!/usr/bin/env bash
set -uo pipefail
D=/home/henrytan/git/maestro/experiments/016_she_sheet_to_voice
cd "$D"; mkdir -p outputs/homr outputs/oemer outputs/audiveris
export CUDA_VISIBLE_DEVICES="" PYTHONWARNINGS=ignore
for p in source-private/page-*.png; do b=$(basename "${p%.png}"); cp "$p" outputs/homr/$b.png
  ( time nice ~/maestro-runtime/analysis-venv/bin/homr outputs/homr/$b.png ) >> outputs/homr/run.log 2>&1 || echo "homr failed $b" >> outputs/homr/run.log; rm -f outputs/homr/$b.png; done
AUD=~/maestro-runtime/audiveris/extracted/opt/audiveris/bin/Audiveris
( time "$AUD" -batch -export -output outputs/audiveris source-private/page-1.png source-private/page-2.png source-private/page-3.png ) > outputs/audiveris/run.log 2>&1
for p in source-private/page-*.png; do ( time nice ~/maestro-runtime/oemer-venv/bin/oemer "$p" -o outputs/oemer --without-deskew ) >> outputs/oemer/run.log 2>&1 || echo "oemer failed $p" >> outputs/oemer/run.log; done
echo OMR16_DONE >> outputs/homr/run.log
