#!/usr/bin/env bash
# Détection des murs + normalisation, en UN SEUL décodage de la source.
# Produit raw_<tag>{R,B}.txt, ac_<tag>.txt, les .tsv associés et <sortie>.mp4
#
#   bash job2.sh <source.mp4> "<crop-plateau>" "<crop-cadrage>" <tag> <sortie>
#
# La source est cherchée dans $SOLRUSH_SOURCES, ou prise telle quelle si c'est
# un chemin existant. Les fichiers de travail sont écrits dans le dossier courant.
set -u
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"

SRCF="$1"
[ -f "$SRCF" ] || SRCF="$SOURCES/$1"
[ -f "$SRCF" ] || { echo "source introuvable : $1" >&2; exit 1; }

RED="colorchannelmixer=rr=1:rg=-0.5:rb=-0.5:gr=1:gg=-0.5:gb=-0.5:br=1:bg=-0.5:bb=-0.5"
BLU="colorchannelmixer=rr=-0.5:rg=-0.5:rb=1:gr=-0.5:gg=-0.5:gb=1:br=-0.5:bg=-0.5:bb=1"

"$FF/ffmpeg" -v error -y -i "$SRCF" -filter_complex "[0:v]split=2[pl][cad];[pl]$2,fps=30,split=3[r][b][a];[r]$RED,format=gray,signalstats,metadata=print:file=raw_$4R.txt[ro];[b]$BLU,format=gray,signalstats,metadata=print:file=raw_$4B.txt[bo];[a]tblend=all_mode=difference,format=gray,signalstats,metadata=print:file=ac_$4.txt[ao];[cad]$3,scale=900:-2,pad=1080:1920:90:100:white,fps=30,format=yuv420p[vo]" -map "[ro]" -f null - -map "[bo]" -f null - -map "[ao]" -f null - -map "[vo]" -fps_mode cfr -r 30 -c:v libx264 -preset veryfast -crf 16 -an "$5.mp4"

for c in R B; do
  awk -F'[ =]+' '/^frame:/{split($1,b,":");f=b[2]} /YAVG/{print f"\t"$2}' "raw_$4$c.txt" \
    | sed 's/lavfi.signalstats.YAVG\t//' > "y_$4$c.tsv"
done
awk -F'[ =]+' '/^frame:/{split($1,b,":");f=b[2]} /YAVG/{print f"\t"$2}' "ac_$4.txt" \
  | sed 's/lavfi.signalstats.YAVG\t//' > "ac_$4.tsv"

echo "$4: $(wc -l < "y_$4R.tsv") images analysees | $5.mp4 $("$FF/ffprobe" -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$5.mp4") images"
