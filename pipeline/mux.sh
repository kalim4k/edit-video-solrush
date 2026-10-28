#!/usr/bin/env bash
# Montage AVEC voix off — fonction abandonnée le 28/10/2026, conservée pour mémoire.
# Pour un montage normal, utiliser muxnu.sh.
#
#   bash mux.sh <tag> <préfixe des voix> <nombre de répliques> <durée> <nom de sortie>
set -u
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"

T=$1; P=$2; N=$3; DUR=$4; OUT=$5
mkdir -p "$SORTIE"

V=""; i=0
while [ $i -lt "$N" ]; do V="$V -i ${P}_${i}.wav"; i=$((i+1)); done

# shellcheck disable=SC2086
"$FF/ffmpeg" -v error -y -i "aud_$T.wav" $V -i "$SFX/sfx2.wav" -/filter_complex "fx_$T.txt" \
  -map "[aout]" -t "$DUR" -c:a pcm_s16le -ar 44100 -ac 2 "mx_$T.wav"
"$FF/ffmpeg" -v error -y -i "vid_$T.mp4" -i "mx_$T.wav" -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart "$SORTIE/$OUT"

$PY "$(dirname "${BASH_SOURCE[0]}")/check.py" "$PWD" "cfg_$T.json" "$(echo "$T" | tr '[:lower:]' '[:upper:]')" "mx_$T.wav" | tail -1
"$FF/ffprobe" -v error -show_entries format=duration -of csv=p=0 "$SORTIE/$OUT"
