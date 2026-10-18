#!/usr/bin/env bash
set -uo pipefail
D=/home/henrytan/git/maestro/experiments/017_omr_benchmark
cd "$D"; export CUDA_VISIBLE_DEVICES="" PYTHONWARNINGS=ignore
AUD=~/maestro-runtime/audiveris/extracted/opt/audiveris/bin/Audiveris
for cond in clean degraded; do
  mkdir -p outputs/$cond/homr outputs/$cond/oemer outputs/$cond/audiveris
  for p in pages/$cond/*.png; do b=$(basename "${p%.png}")
    cp "$p" outputs/$cond/homr/$b.png
    ( time nice ~/maestro-runtime/analysis-venv/bin/homr outputs/$cond/homr/$b.png ) >> outputs/$cond/homr/run.log 2>&1 || echo "homr failed $b" >> outputs/$cond/homr/run.log
    rm -f outputs/$cond/homr/$b.png
    ( time nice ~/maestro-runtime/oemer-venv/bin/oemer "$p" -o outputs/$cond/oemer --without-deskew ) >> outputs/$cond/oemer/run.log 2>&1 || echo "oemer failed $b" >> outputs/$cond/oemer/run.log
  done
  ( time "$AUD" -batch -export -output outputs/$cond/audiveris pages/$cond/*.png ) > outputs/$cond/audiveris/run.log 2>&1
done
echo OMR17_DONE >> outputs/clean/homr/run.log
