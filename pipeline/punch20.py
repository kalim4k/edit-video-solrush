# -*- coding: utf-8 -*-
"""V20 — User6781 (son 1) vs araliomar47. Victoire de User6781, arrivée à 106.37 s."""
import punch

LIGNES = [
 ("Quinze murs chacun. Lui, il va en garder trois pour la fin. Grosse erreur.",   0.00,   0.25, 1),
 ("J'ouvre. Il répond dans la seconde.",                                          6.13,   6.60, 0),
 ("Quatre partout en dix secondes. Personne ne lâche.",                          15.97,  19.80, 0),
 ("Et là, plus rien. Personne ne bouge.",                                        20.00,  29.50, 1),
 ("Ça repart d'un coup.",                                                        34.00,  34.40, 1),
 ("Neuf murs en huit secondes. Et j'en mène un.",                                42.23,  46.20, 1),
 ("Il me reste cinq murs, lui six. Ça se joue à rien.",                          55.10,  59.90, 0),
 ("Je déroule. Il subit.",                                                       62.50,  67.50, 1),
 ("Quatorze murs posés. Il ne m'en reste qu'un.",                                70.07,  75.20, 1),
 ("J'ai tout donné. Zéro mur. Lui il en garde trois.",                           83.50,  88.20, 1),
 ("Il les sort maintenant, pendant que je cours à vide.",                        91.90,  93.50, 0),
 ("Plus un seul mur sur le terrain. Et devant, c'est moi.",                      96.27, 101.00, 0),
 ("Trois murs gardés pour rien.",                                               106.37, 106.50, 1),
]
punch.faire("v20", LIGNES, "q", fixe_derniere=106.50)
