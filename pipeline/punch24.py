# -*- coding: utf-8 -*-
"""V24 — Clever dude (bleu, son 1) perd. 15 murs chacun.
   Quick Otter arrive à 95.70 s en sortie."""
import punch

LIGNES = [
 ("Je mène six murs à trois. Et je vais perdre quand même.",               0.00,  0.25, 1),
 ("Six murs à trois. Je pars devant.",                                    13.73, 18.50, 0),
 ("Puis plus rien pendant quinze secondes.",                              28.73, 30.00, 0),
 ("Onze contre huit. Je suis encore devant.",                             42.97, 47.20, 1),
 ("Douze à neuf. Ça sent bon.",                                           52.03, 57.30, 0),
 ("Et là il enchaîne. Quatre murs de suite, je ne réponds pas.",          66.90, 70.90, 1),
 ("Il vide tout. Il n'a plus un seul mur.",                               74.53, 75.00, 0),
 ("Moi il m'en reste un. Un seul.",                                       76.77, 79.00, 1),
 ("Je le pose. Trop tard.",                                               87.20, 88.00, 0),
 ("Quinze partout. Et c'est lui qui passe.",                              95.70, 95.75, 1),
]
punch.faire("v24", LIGNES, "u", fixe_derniere=95.75)
