# -*- coding: utf-8 -*-
"""V22 — rejeu SolRush capture image par image.
   Rythme : pion rapide, mur tenu, derniere position tenue longtemps.
   Produit la liste concat et le tableau des murs (image de sortie + joueur)."""
import json

D_DEBUT, D_PION, D_MUR, D_FIN = 45, 14, 33, 90      # en images a 30 i/s

d = json.load(open("replay.json", encoding="utf-8"))
ml = d["move_log"]
n = len(ml)

duree = [D_DEBUT] + [D_MUR if m["type"] == "wall" else D_PION for m in ml]
duree[-1] = D_FIN                                    # on tient l'arrivee

depart, s = [], 0
for x in duree:
    depart.append(s); s += x
total = s

# murs : le mur du coup i apparait sur l'image depart[i+1]
murs = []
for i, m in enumerate(ml):
    if m["type"] != "wall": continue
    joueur = i % 2                                   # p0 commence
    murs.append({"F": depart[i + 1], "s": 1 if joueur == 0 else 2})
murs.sort(key=lambda w: w["F"])

with open("in22.txt", "w") as f:
    for i, x in enumerate(duree):
        f.write("file 'v22/f%04d.png'\nduration %.6f\n" % (i, x / 30.0))
    f.write("file 'v22/f%04d.png'\n" % n)

json.dump({"nframes": total, "walls": murs, "depart": depart}, open("plan22.json", "w"))

n1 = sum(1 for w in murs if w["s"] == 1)
print("%s (p0, son 1) vs %s (p1, son 2)" % (d["p0_nick"], d["p1_nick"]))
print("vainqueur : %s" % (d["p1_nick"] if d["winner"] else d["p0_nick"]))
print("%d images de sortie = %.2f s | %d murs (son1=%d son2=%d)"
      % (total, total / 30.0, len(murs), n1, len(murs) - n1))
print("\nmurs sur la chronologie de sortie :")
for w in murs:
    print("   %6.2f s  son%d" % (w["F"] / 30.0, w["s"]))
print("\narrivee (derniere position) : %.2f s" % (depart[n] / 30.0))
