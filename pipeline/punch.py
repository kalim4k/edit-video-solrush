# -*- coding: utf-8 -*-
"""Genere et place un commentaire punchline. (texte, ancre, cible, punch)
La derniere replique peut etre calee a la main, par-dessus le meme final."""
import sys, json, voix, chrono, accents

VOIX = "Lfiz1ywD0WNNzhXjTPc8"          # vieux homme script seedance

def faire(tag, lignes, prefixe, fixe_derniere=None):
    textes = [l[0] for l in lignes]
    accents.verifier(textes)
    durees, cout = voix.generer(textes, VOIX, prefixe)
    murs, memes, total, _ = chrono.timeline("cfg_%s.json" % tag)
    if fixe_derniere is None:
        pos = voix.placer([l[2] for l in lignes], durees, memes, total,
                          ancres=[l[1] for l in lignes])
    else:
        pos = voix.placer([l[2] for l in lignes[:-1]], durees[:-1], memes[:-1], total,
                          ancres=[l[1] for l in lignes[:-1]])
        pos.append(fixe_derniere)
    json.dump({"pos": pos, "dur": durees, "punch": [l[3] for l in lignes],
               "total": total, "cout": cout}, open("punch_%s.json" % tag, "w"))

    print("\n-- controle de placement --")
    ok = True
    for i, (p, d, l) in enumerate(zip(pos, durees, lignes)):
        pb = []
        if p < l[1] - 0.01: pb.append("AVANT SON FAIT")
        for j, (m0, m1) in enumerate(memes):
            if p < m1 and p + d > m0 and not (fixe_derniere is not None and i == len(lignes)-1):
                pb.append("CHEVAUCHE MEME %.1f-%.1f" % (m0, m1))
        if p + d > total + 0.01: pb.append("DEPASSE LA FIN")
        if pb: ok = False
        print("  L%-2d %6.2f -> %6.2f  (ancre %6.2f) %s %s"
              % (i, p, p + d, l[1], "PUNCH" if l[3] else "     ", " ".join(pb) or "ok"))
    print("  => %s | %d caracteres" % ("tout est valide" if ok else "A CORRIGER", cout))
    return pos, durees
