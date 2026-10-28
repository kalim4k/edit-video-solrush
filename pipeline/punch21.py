# -*- coding: utf-8 -*-
"""V21 — User6781 (son 1) vs lis42. Défaite de User6781, arrivée bleue à 112.60 s."""
import punch

LIGNES = [
 ("Je mène six murs à quatre. Et je vais quand même perdre. Regarde comment.",    0.00,   0.25, 1),
 ("Je pars devant. Deux murs avant qu'il en pose un.",                            8.10,   8.60, 0),
 ("Six contre quatre. Je tiens la partie.",                                      18.70,  23.20, 0),
 ("Et là il lâche tout. Cinq murs d'affilée, je ne réponds pas une seule fois.",  32.87,  38.50, 1),
 ("Neuf pour lui, six pour moi. J'ai perdu la main sans m'en rendre compte.",     32.87,  42.00, 1),
 ("Douze à sept. Il me noie.",                                                   55.47,  60.20, 0),
 ("Je me réveille. Quatre murs coup sur coup.",                                  65.13,  70.50, 1),
 ("Onze-douze. Je suis revenu à un mur.",                                        65.13,  74.00, 0),
 ("Quatorze partout. Tout se joue sur le dernier.",                              86.20,  90.50, 1),
 ("Je pose mon quinzième. Je n'ai plus rien. Lui il en garde un.",               95.13,  99.50, 1),
 ("Un mur. Gardé quatorze secondes. Posé juste devant moi.",                    109.43, 109.50, 1),
 ("Tout ça pour ça.",                                                          112.60, 112.70, 1),
]
punch.faire("v21", LIGNES, "r", fixe_derniere=112.70)
