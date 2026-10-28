# -*- coding: utf-8 -*-
"""Briques de construction d'une config de montage.

   MM      : catalogue des clips de memes (fichier, debut, duree, gain, options)
   meme()  : fabrique une entree de meme pour le cfg
   walls() : lit st_<tag>{R,B}.tsv, ignore la 1re ligne (apparition du plateau)
             et les amplitudes < 0.15 (artefacts de billes), puis attribue
             le son 1 a la couleur donnee.

   Module d'aide : il ne fait rien a l'import. Voir mk25.py pour un exemple.
"""
import json

MM = {
 "joe":     ("vlipsy-joe-rogan-shocking-reaction-hQOOp7nb",0.25,3.0,1.8,{}),
 "cut":     ("vlipsy-you-didnt-have-to-cut-me-off-6QFdjMjw",4.00,3.0,-2.9,{}),
 "cri":     ("video_2026-09-15_19-22-12",0.25,3.0,-2.9,{}),
 "memeee":  ("memeee",1.50,3.0,3.6,{}),
 "kevin":   ("video_2026-09-15_19-21-53",0.00,3.0,0,{"silent":1}),
 "tension": ("video_2026-09-15_19-22-05",5.75,3.0,-4.1,{}),
 "supa":    ("vlipsy-supa-hot-fire-ohhhhhhh-uNzTGgUT",0.00,3.0,-6.8,{}),
 "vertic":  ("video_2026-09-15_19-21-59",0.75,3.0,-0.4,{"pre":"crop=574:620:0:90","box":[408,440,336,1465]}),
 "bureau":  ("video_2026-09-15_19-21-47",0.00,2.40,6.9,{}),
 "narstie": ("vlipsy-the-big-narstie-show-big-narstie-laugh-fiPa5SFG",0.25,3.0,-1.8,{}),
 "pleure":  ("vlipsy-man-crying-oTGPrv7m",3.50,3.0,-2.0,{}),
 "mutahar": ("vlipsy-mutahar-extreme-laugh-UlELJLF8",0.75,3.0,-0.9,{}),
 "applaud": ("video_2026-09-15_19-21-41",0.00,2.92,-4.4,{}),
 "martin":  ("vlipsy-martin-lawrence-noooooo-RA293NP1",2.50,3.0,-7.6,{}),
 "vert":    ("vlipsy-green-screen-meme-black-guy-crying-jFvD7W8l",5.25,3.0,2.0,{"key":1}),
 "housew":  ("vlipsy-real-housewives-of-beverly-hills-you-have-no-idea-what-ive-been-through-FJZ9wRuW",2.00,3.0,6.6,{}),
}
def meme(k,F,pause):
    f,s,d,g,ex = MM[k]
    m = {"file":f,"src":s,"dur":d,"gain":g,"pause":pause,"F":F}; m.update(ex); return m

def walls(tag, son1_colour):
    """Murs detectes, tries. Ignore la 1re ligne (apparition du plateau) et les
       marches d'amplitude < 0.15, qui sont des artefacts de billes en mouvement."""
    out = []
    for c in ("R", "B"):
        for i, l in enumerate(open("st_%s%s.tsv" % (tag, c))):
            if i == 0: continue
            F, _, amp = l.split("	")
            if float(amp) < 0.15: continue
            out.append({"F": int(F), "s": 1 if c == son1_colour else 2})
    return sorted(out, key=lambda w: w["F"])
