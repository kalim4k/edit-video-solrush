#!/usr/bin/env bash
# Montage SANS voix off — c'est le cas normal depuis le 28/10/2026.
# aud_<tag>.wav contient déjà les impacts de murs et le son des mèmes : on le muxe tel quel.
#
#   bash muxnu.sh <tag> "montage_V<NN>_<Joueur1>-vs-<Joueur2>.mp4"
set -u
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"

T=$1; OUT=$2
mkdir -p "$SORTIE"

"$FF/ffmpeg" -v error -y -i "vid_$T.mp4" -i "aud_$T.wav" -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart "$SORTIE/$OUT"

$PY "$(dirname "${BASH_SOURCE[0]}")/check.py" "$PWD" "cfg_$T.json" "$(echo "$T" | tr '[:lower:]' '[:upper:]')" "aud_$T.wav" | tail -1
"$FF/ffprobe" -v error -show_entries format=duration -of csv=p=0 "$SORTIE/$OUT"
