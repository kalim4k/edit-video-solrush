# -*- coding: utf-8 -*-
"""Genere des repliques ElevenLabs, detecte les hallucinations et regenere si besoin."""
import env
import subprocess, statistics, el2
def _dur(f):
    return float(subprocess.run([env.FFPROBE,"-v","error","-show_entries","format=duration",
        "-of","csv=p=0",f], capture_output=True, text=True).stdout.strip())
def _gaps(f):
    r = subprocess.run([env.FFMPEG,"-v","info","-nostats","-i",f,"-af",
        "silencedetect=noise=-32dB:d=0.12","-f","null","-"], capture_output=True, text=True).stderr
    return max(0, r.count("silence_start") - 2)
def _rendre(txt, voix, base):
    ok, info = el2.say(txt, voix, base+".mp3", stab=0.75, style=0.0, sim=0.8)
    if not ok: raise RuntimeError(info)
    subprocess.run([env.FFMPEG,"-v","error","-y","-i",base+".mp3","-af",
        "loudnorm=I=-15:TP=-1.5:LRA=9","-ar","44100","-ac","2",base+".wav"], check=True)
    return _dur(base+".wav"), _gaps(base+".wav"), len(txt)

def generer(lignes, voix, prefixe, essais=3):
    infos, cout = [], 0
    for i, t in enumerate(lignes):
        d, g, n = _rendre(t, voix, "%s_%d" % (prefixe, i)); cout += n
        infos.append([d, g, len(t)/14.0])
    med = statistics.median(d/a for d, g, a in infos)
    for i, t in enumerate(lignes):
        for k in range(essais):
            d, g, att = infos[i]
            if d/att <= med*1.45 and g < 2: break
            d, g, n = _rendre(t, voix, "%s_%d" % (prefixe, i)); cout += n
            infos[i] = [d, g, att]
            print("     reprise %d de la ligne %d" % (k+1, i))
    print("  duree des repliques :", " ".join("%.2f" % d for d, _, _ in infos))
    reste = [i for i,(d,g,a) in enumerate(infos) if d/a > med*1.45 or g >= 2]
    print("  lignes encore suspectes : %s | caracteres consommes : %d" % (reste or "aucune", cout))
    return [d for d, _, _ in infos], cout

def placer(debuts, durees, fenetres, total, marge=0.15):
    """Recale chaque replique pour qu'elle ne morde sur aucun meme."""
    out = []
    for s, d in zip(debuts, durees):
        fin = s + d
        for (a, b) in fenetres:
            if s < b and fin > a:               # chevauchement
                s = max(0.25, a - d - marge)    # on recule avant le meme
                fin = s + d
        out.append(round(min(s, total - d - 0.05), 2))
    return out
