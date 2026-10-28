# -*- coding: utf-8 -*-
"""Trouve l'instant où une bille atteint la zone d'arrivée, donc qui gagne.

   Piège résolu : les murs de la même couleur traversent aussi cette zone.
   On distingue par la forme — après mise à l'échelle un mur fait ~22 px
   d'épaisseur, une bille ~48. D'où le seuil `epais`, et un seuil de largeur
   `large` pour écarter un mur vertical (~14 px de large).

   usage : py -3 arrivee.py <video_normalisee.mp4> <t_debut> <duree> <R|B>
"""
import env
import subprocess, glob, os, shutil, sys
from PIL import Image

def scan(video, t0, dur, coul, epais=34, large=24, y0=335, y1=475):
    tmp = "arr_tmp"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run([env.FFMPEG, "-v", "error", "-y", "-ss", str(t0), "-t", str(dur),
                    "-i", video, "-vf", "crop=880:%d:100:%d,fps=10" % (y1 - y0, y0),
                    os.path.join(tmp, "a%04d.png")], check=True)
    out, trace = None, []
    for f in sorted(glob.glob(os.path.join(tmp, "a*.png"))):
        im = Image.open(f); p = im.convert("RGB").load(); w, h = im.size
        n = 0
        for x in range(0, w, 2):
            c = 0
            for y in range(0, h, 2):
                r, g, b = p[x, y]
                if coul == "R":
                    if r > 110 and r > g + 35 and r > b + 35: c += 2
                else:
                    if b > 100 and b > r + 25 and b > g + 10: c += 2
            if c >= epais: n += 2
        t = t0 + (int(f[-8:-4]) - 1) / 10.0
        trace.append((t, n))
        if n >= large and out is None: out = t
    shutil.rmtree(tmp, ignore_errors=True)
    return out, trace

if __name__ == "__main__":
    video, t0, dur, coul = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    r, tr = scan(video, t0, dur, coul)
    print("arrivee : %s" % (("%.2f s" % r) if r else "non trouvee"))
    print("largeur detectee :",
          " ".join("%.0fs:%d" % (t, n) for t, n in tr if abs(t - round(t)) < 0.02))
