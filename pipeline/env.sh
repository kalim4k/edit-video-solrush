# Résolution des chemins pour les scripts shell. À sourcer en tête de chaque script.
# Mêmes variables que env.py ; voir ce fichier pour le détail.

ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RACINE="${SOLRUSH_RACINE:-$(dirname "$ICI")}"

if [ -n "${FFMPEG_BIN:-}" ] && [ -x "$FFMPEG_BIN/ffmpeg" ]; then
  FF="$FFMPEG_BIN"
elif [ -n "${FFMPEG_BIN:-}" ] && [ -x "$FFMPEG_BIN/ffmpeg.exe" ]; then
  FF="$FFMPEG_BIN"
elif command -v ffmpeg >/dev/null 2>&1; then
  FF="$(dirname "$(command -v ffmpeg)")"
else
  echo "ffmpeg est introuvable. Installe-le, ou indique son dossier avec FFMPEG_BIN." >&2
  exit 1
fi

MEMES="${SOLRUSH_MEMES:-$RACINE/memes video}"
SORTIE="${SOLRUSH_SORTIE:-$RACINE/SORTIE}"
SOURCES="${SOLRUSH_SOURCES:-$RACINE/SOURCES}"
SFX="$ICI/sfx"
TRAVAIL="${SOLRUSH_TRAVAIL:-$PWD}"
PY="${PYTHON:-py -3}"
command -v py >/dev/null 2>&1 || PY="${PYTHON:-python3}"
