# -*- coding: utf-8 -*-
"""V19 — version punchline. (texte, ancre, cible, punch)"""
import voix, chrono, accents, json

VOIX = "Lfiz1ywD0WNNzhXjTPc8"     # vieux homme script seedance
LIGNES = [
 ("Regarde bien. Je vais le laisser gagner pendant vingt secondes. Exprès.", 0.0,  0.25, 1),
 ("Lui, il attaque comme si la partie durait dix secondes.",                 4.53, 4.80, 0),
 ("Moi je pose trois murs, et j'arrête. Il a rien capté.",                   8.30, 9.40, 0),
 ("Sept murs cramés d'un coup. Il lui en reste trois. Merci.",              15.07, 20.00, 1),
 ("Là, plus personne ne pose rien. Lui il court. Moi je compte.",           20.00, 27.00, 1),
 ("Presque vingt secondes qu'il court tout seul.",                          33.00, 33.50, 0),
 ("Retour à l'envoyeur.",                                                   35.33, 35.45, 1),
 ("Il croyait vraiment que j'avais tout dépensé.",                          36.93, 40.50, 0),
 ("Lui c'est fini, il est à sec. Moi il m'en reste trois.",                 49.60, 50.00, 1),
 ("Dix partout. Plus un mur sur le terrain. Maintenant c'est la course.",   54.80, 59.00, 0),
 ("Et c'est pour ça qu'on garde ses murs.",                                 70.00, 73.95, 1),
]
textes = [l[0] for l in LIGNES]
accents.verifier(textes)                       # bloque si le texte est desaccentue
durees, cout = voix.generer(textes, VOIX, "p")
murs, memes, total, _ = chrono.timeline("cfg_v19.json")
pos = voix.placer([l[2] for l in LIGNES], durees, memes, total,
                  ancres=[l[1] for l in LIGNES])
json.dump({"pos": pos, "dur": durees, "punch": [l[3] for l in LIGNES],
           "total": total, "cout": cout}, open("punch19.json", "w"))
print("placements :", pos)
