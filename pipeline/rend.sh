#!/usr/bin/env bash
# Rendu de l'image et du son d'un montage, à partir des filtres écrits par gen.py.
#
#   bash rend.sh <tag> <nombre d'images> <durée en secondes>
#
# Les deux comptes affichés doivent correspondre exactement aux valeurs attendues.
set -u
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"

T=$1; NF=$2; DUR=$3
IN=$(cat "in_$T.txt")

eval "\"\$FF/ffmpeg\" -v error -y $IN -/filter_complex fv_$T.txt -map '[vout]' -r 30 -frames:v $NF -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -an vid_$T.mp4"
echo "video : $("$FF/ffprobe" -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "vid_$T.mp4") images (attendu $NF)"

eval "\"\$FF/ffmpeg\" -v error -y $IN -/filter_complex fa_$T.txt -map '[aout]' -t $DUR -c:a pcm_s16le -ar 44100 -ac 2 aud_$T.wav"
echo "audio : $("$FF/ffprobe" -v error -show_entries format=duration -of csv=p=0 "aud_$T.wav") s (attendu $DUR)"
