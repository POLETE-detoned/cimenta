#!/usr/bin/env bash
# Extrae de set05.mp4 los cuatro fragmentos reales de la app que usa la escena «Es la beta»
# y el render de la tarjeta de licitación. Requiere ffmpeg en $FFMPEG (o en el PATH).
set -euo pipefail
cd "$(dirname "$0")"
FF="${FFMPEG:-ffmpeg}"
mkdir -p clip
i=0
for ss in 0.5 8.5 26 57.5; do            # feed · data room · mesa de ofertas · matriz
  i=$((i+1))
  "$FF" -loglevel error -y -ss "$ss" -t 1.5 -i ../set05.mp4 -vf fps=30 -q:v 3 "clip/c${i}_%03d.jpg"
done
"$FF" -loglevel error -y -i clip/c1_001.jpg -vf "crop=478:268:1037:142,scale=956:536:flags=lanczos" -q:v 2 obra.jpg
