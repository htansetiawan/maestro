#!/usr/bin/env bash
set -uo pipefail
D=/home/henrytan/git/maestro/experiments/013_score_reading_fidelity
cd "$D"
py=~/maestro-runtime/analysis-venv/bin/python
export CUDA_VISIBLE_DEVICES=""
mkdir -p outputs/homr outputs/oemer
for p in source-private/pages/page-*.png; do
  b=$(basename "${p%.png}")
  cp "$p" "outputs/homr/$b.png"
  ( time PYTHONWARNINGS=ignore nice ~/maestro-runtime/analysis-venv/bin/homr "outputs/homr/$b.png" ) >> outputs/homr/run.log 2>&1 || echo "homr failed on $b" >> outputs/homr/run.log
  rm -f "outputs/homr/$b.png"
done
ls outputs/homr >> outputs/homr/run.log
for p in source-private/pages/page-*.png; do
  ( time PYTHONWARNINGS=ignore nice ~/maestro-runtime/analysis-venv/bin/oemer "$p" -o outputs/oemer --without-deskew ) >> outputs/oemer/run.log 2>&1 || echo "oemer failed on $p" >> outputs/oemer/run.log
done
ls outputs/oemer >> outputs/oemer/run.log
echo HOMR_OEMER_DONE >> outputs/homr/run.log
