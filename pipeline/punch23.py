# -*- coding: utf-8 -*-
"""V23 — Clever dude (bleu, son 1) gagne. Quick Otter finit avec 3 murs jamais posés.
   Arrivée à 91.70 s en sortie."""
import punch

LIGNES = [
 ("Il va finir la partie avec trois murs dans les mains. Trois. Regarde.",  0.00,  0.25, 1),
 ("J'ouvre. Il réplique aussitôt.",                                         5.27,  5.60, 0),
 ("Quatre partout en quinze secondes. Puis plus rien.",                    15.83, 19.50, 0),
 ("Plus un mur depuis quinze secondes. On se regarde.",                    25.00, 31.00, 0),
 ("Ça repart. Sept murs pour moi, six pour lui.",                          37.47, 41.90, 1),
 ("Dix contre neuf. Je garde un mur d'avance.",                            54.73, 59.20, 0),
 ("Il pose son douzième. Ce sera le dernier.",                             71.27, 71.60, 1),
 ("Moi je vide tout. Quinze murs posés.",                                  76.57, 80.90, 0),
 ("Lui, il en garde trois. Il ne les posera jamais.",                      76.57, 84.50, 1),
 ("Trois murs pour rien.",                                                 91.70, 91.75, 1),
]
punch.faire("v23", LIGNES, "t", fixe_derniere=91.75)
