# -*- coding: utf-8 -*-
"""Construit le filtre de mixage de la voix off pour un montage.
   usage : py -3 mkfx.py <tag> <prefixe> [--stings]

   Les stings de punchline sont DESACTIVES par defaut : l'utilisateur y a
   renonce le 26/09/2026 ("pour les prochaines videos oublie les effets
   sonores a chaque punchline"). Ne les reactiver que sur demande explicite."""
import sys, json, chrono

tag, pre = sys.argv[1], sys.argv[2]
stings = "--stings" in sys.argv[3:]

d = json.load(open("punch_%s.json" % tag))
pos, dur, punch, total = d["pos"], d["dur"], d["punch"], d["total"]
murs, memes, _, _ = chrono.timeline("cfg_%s.json" % tag)
SD = 0.29

def caler(x):
    """Recule le sting tant qu'il chevauche l'impact d'un mur."""
    for _ in range(40):
        c = [w for w, _s in murs if x - 0.10 < w < x + SD + 0.10]
        if not c: return round(x, 2)
        x = min(c) - SD - 0.12
    return round(x, 2)

st = [caler(p + dd - 0.12) for p, dd, k in zip(pos, dur, punch) if k] if stings else []
if st:
    print("stings :", st)
    for s in st:
        w = min(murs, key=lambda m: abs(m[0] - s))
        print("   %6.2f s  -> mur le plus proche %6.2f s (ecart %.2f s)" % (s, w[0], abs(w[0] - s)))
else:
    print("sans sting (%d punchlines reperees dans le script, aucune sonorisee)"
          % sum(1 for k in punch if k))

nv = len(pos)
L = []
for i, p in enumerate(pos):
    L.append("[%d:a]adelay=%d|%d[q%d];" % (i + 1, round(p * 1000), round(p * 1000), i))
if st:
    L.append("[%d:a]asplit=%d%s;" % (nv + 1, len(st), "".join("[z%d]" % j for j in range(len(st)))))
    for j, s in enumerate(st):
        L.append("[z%d]adelay=%d|%d[t%d];" % (j, round(s * 1000), round(s * 1000), j))
L.append("%samix=inputs=%d:normalize=0:duration=longest:dropout_transition=0,apad=whole_dur=%.4f[vall];"
         % ("".join("[q%d]" % i for i in range(nv)), nv, total))
L.append("[vall]asplit=2[vmix][vsc];")
L.append("[0:a][vsc]sidechaincompress=threshold=0.025:ratio=9:attack=15:release=350:makeup=1[duck];")
if st:
    L.append("%samix=inputs=%d:normalize=0:duration=longest:dropout_transition=0,apad=whole_dur=%.4f[sall];"
             % ("".join("[t%d]" % j for j in range(len(st))), len(st), total))
    fin = "[duck][vmix][sall]amix=inputs=3"
else:
    fin = "[duck][vmix]amix=inputs=2"
L.append(fin + ":normalize=0:duration=first:dropout_transition=0,"
         "alimiter=limit=0.95:attack=5:release=60[aout]")
open("fx_%s.txt" % tag, "w").write("\n".join(L))
print("fx_%s.txt ecrit (%d repliques, %d stings)" % (tag, nv, len(st)))
