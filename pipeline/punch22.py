# -*- coding: utf-8 -*-
"""V22 — point de vue de Silent Bear (rouge, son 2), vainqueur.
   Wild Fox vide ses dix murs a 33.40 s ; il en reste quatre a Silent Bear."""
import punch

LIGNES = [
 ("Il va vider ses dix murs. Moi j'en garde quatre pour la fin. Regarde.",  0.00,  0.25, 1),
 ("Il attaque, je réponds. Deux partout.",                                  9.47, 10.00, 0),
 ("Six murs pour lui, trois pour moi. Il croit me noyer.",                 16.83, 17.30, 1),
 ("Huit contre quatre. Je le laisse faire.",                               24.33, 24.70, 0),
 ("Chaque mur qu'il pose, c'est un mur qu'il n'aura plus.",                28.57, 29.50, 0),
 ("Et voilà. Son dixième. Il n'a plus rien.",                              33.40, 36.90, 1),
 ("J'en ai encore trois. Et il ne peut plus répondre.",                    37.50, 40.50, 1),
 ("Je ferme tout.",                                                        48.10, 49.20, 0),
 ("Plus un seul mur.",                                                     50.60, 54.10, 0),
 ("Il était à une case. Une.",                                             55.90, 55.95, 1),
]
punch.faire("v22", LIGNES, "s", fixe_derniere=55.95)
