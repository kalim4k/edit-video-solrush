# -*- coding: utf-8 -*-
"""V25 — Clever dude (bleu) contre Sly Tiger (rouge, son 1 car il pose le plus de murs).
   Sly Tiger vide ses 15 murs à 58.30 s ; Clever dude n'en pose que 11 et gagne à 89.20 s."""
import punch

LIGNES = [
 ("Il va poser quinze murs. Moi onze. Devine qui passe.",              0.00,  0.25, 1),
 ("J'ouvre. Il répond deux fois.",                                     7.33,  7.70, 0),
 ("Quatre partout. Puis neuf secondes sans un mur.",                  15.57, 24.90, 0),
 ("Huit pour lui, six pour moi. Il prend le contrôle.",               32.83, 38.60, 0),
 ("Neuf murs posés. Il n'a plus que six.",                            38.80, 45.00, 0),
 ("Il enchaîne. Douze, treize, il ne s'arrête plus.",                 53.90, 54.30, 1),
 ("Ça y est. Quinze murs. Il est à sec, et il reste trente secondes.", 58.30, 62.90, 1),
 ("Moi il m'en reste sept. Et lui plus rien.",                        65.17, 66.80, 1),
 ("Je ferme tranquillement.",                                         69.67, 76.00, 0),
 ("Onze murs. Quatre encore dans la poche.",                          84.57, 85.20, 1),
 ("Il en a posé quinze. Et c'est moi qui passe.",                     89.20, 89.25, 1),
]
punch.faire("v25", LIGNES, "v", fixe_derniere=89.25)
