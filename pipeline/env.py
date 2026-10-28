# -*- coding: utf-8 -*-
"""Résolution des chemins, pour que la chaîne tourne aussi bien sur une machine
   Windows locale que dans une session Claude Code sous Linux.

   Rien n'est codé en dur : tout se règle par variable d'environnement, avec un
   repli sur la structure du dépôt (ce fichier vit dans `pipeline/`).

     SOLRUSH_RACINE  racine du dépôt            (défaut : le parent de pipeline/)
     SOLRUSH_MEMES   dossier des clips de mèmes (défaut : <racine>/memes video)
     SOLRUSH_SORTIE  dossier de livraison       (défaut : <racine>/SORTIE)
     SOLRUSH_SOURCES dossier des captures       (défaut : <racine>/SOURCES)
     FFMPEG_BIN      dossier contenant ffmpeg   (défaut : celui du PATH)
"""
import os, shutil

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.environ.get("SOLRUSH_RACINE") or os.path.dirname(ICI)

def _exe(nom):
    """Chemin complet de ffmpeg/ffprobe : FFMPEG_BIN, sinon le PATH."""
    d = os.environ.get("FFMPEG_BIN")
    if d:
        for ext in ("", ".exe"):
            p = os.path.join(d, nom + ext)
            if os.path.isfile(p): return p
    p = shutil.which(nom)
    if p: return p
    raise RuntimeError(
        "%s est introuvable. Installe ffmpeg, ou indique son dossier "
        "avec la variable FFMPEG_BIN." % nom)

FFMPEG  = _exe("ffmpeg")
FFPROBE = _exe("ffprobe")
FFBIN   = os.path.dirname(FFMPEG)

MEMES   = os.environ.get("SOLRUSH_MEMES")   or os.path.join(RACINE, "memes video")
SORTIE  = os.environ.get("SOLRUSH_SORTIE")  or os.path.join(RACINE, "SORTIE")
SOURCES = os.environ.get("SOLRUSH_SOURCES") or os.path.join(RACINE, "SOURCES")
SFX     = os.path.join(ICI, "sfx")
CLE_TTS = os.environ.get("ELEVENLABS_KEY_FILE") or os.path.join(RACINE, ".elevenlabs_key")

def chrome():
    """Chemin de Chrome : CHROME_BIN, sinon le PATH, sinon les emplacements usuels."""
    d = os.environ.get("CHROME_BIN")
    if d and os.path.isfile(d): return d
    for n in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(n)
        if p: return p
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              "/usr/bin/google-chrome", "/usr/bin/chromium"):
        if os.path.isfile(p): return p
    raise RuntimeError("Chrome est introuvable. Indique son chemin avec CHROME_BIN.")


if __name__ == "__main__":
    for n in ("RACINE", "FFMPEG", "FFPROBE", "MEMES", "SORTIE", "SOURCES", "SFX"):
        v = globals()[n]
        print("%-8s %-70s %s" % (n, v, "ok" if os.path.exists(v) else "ABSENT"))
