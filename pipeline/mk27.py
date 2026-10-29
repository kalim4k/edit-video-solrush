# -*- coding: utf-8 -*-
import json, mk
# V27 : kalim (bleu) vs Iron Wolf (rouge), duel (rejeu appli 1080x2436, 81 coups).
# 10 murs chacun -> egalite : le ROUGE pose le premier (image 197) et prend le son 1.
# Le rouge gagne : arrivee en bas image 1866 (62.20 s). Bandeau de l'enregistreur
# a partir de l'image 1908 -> coupe a 1905.
# Gels : rouge epuise ses murs (919), puis l'arrivee elle-meme : il ne reste que
# 1.3 s apres l'arrivee, trop peu pour un meme final sans gel.
MEMES = [("joe",210,0),("tension",480,0),("mutahar",945,1),
         ("cut",1270,0),("cri",1680,0),("pleure",1866,1)]
cfg = {"base":"norm_v27.mp4","nframes":1905,
       "memes":[mk.meme(k,F,p) for k,F,p in MEMES],
       "walls":mk.walls("v27","R")}
json.dump(cfg, open("cfg_v27.json","w"), indent=1)
