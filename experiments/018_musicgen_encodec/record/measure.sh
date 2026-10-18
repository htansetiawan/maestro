#!/usr/bin/env bash
# Top-line melody recall with the 014 pipeline (piano transcription -> skyline -> alignment).
# MusicGen clips are 30 s, so they are graded against the first 30 s of each written line;
# EnCodec round trips carry the whole 46 s excerpt and are graded against all 51 notes.
set -euo pipefail
D=/home/henrytan/git/maestro/experiments/018_musicgen_encodec
M=/home/henrytan/git/maestro/experiments/014_yue2_excerpt_ablation/record/measure.py
PY=/home/henrytan/maestro-runtime/yue2-venv/bin/python
export MEASURE_DEVICE=cuda PYTHONWARNINGS=ignore
cd "$D"
$PY "$M" --events inputs/cp-events.json --melody-key melody_30s --output outputs/measure-cp-30s.json \
  --audio outputs/cp-guide/audio.mp3 outputs/cp-recording/audio.mp3 outputs/cp-text-only/audio.mp3 --labels cp-guide cp-recording cp-text-only
$PY "$M" --events inputs/she-events.json --melody-key melody_30s --output outputs/measure-she-30s.json \
  --audio outputs/she-guide/audio.mp3 --labels she-guide
$PY "$M" --events inputs/cp-events.json --melody-key melody --output outputs/measure-encodec.json \
  --audio outputs/encodec24-1.5kbps/audio.mp3 outputs/encodec24-3kbps/audio.mp3 outputs/encodec24-6kbps/audio.mp3 outputs/encodec24-12kbps/audio.mp3 outputs/encodec24-24kbps/audio.mp3 outputs/encodec32-musicgen/audio.mp3 \
  --labels encodec24-1.5kbps encodec24-3kbps encodec24-6kbps encodec24-12kbps encodec24-24kbps encodec32-musicgen
echo MEASURE18_DONE
