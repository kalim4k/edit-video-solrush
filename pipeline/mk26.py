# -*- coding: utf-8 -*-
import json, mk
# V26 : kalim (bleu) vs Noble Panther (rouge), rejeu lu dans l'appli (1080x2436, ~8 img/s).
# Rouge pose 10 murs, bleu 9 -> ROUGE prend le son 1 (il en pose le plus).
# Le bleu gagne : arrivee image 1743 (58.10 s source). Bandeau de l'enregistreur
# a partir de l'image 1824 -> coupe a 1820.
# Gels : rouge pose son dernier mur (1313), mur bleu decisif (1563).
MEMES = [("joe",200,0),("tension",500,0),("cut",930,0),
         ("martin",1340,1),("supa",1590,1),("applaud",1743,0)]
cfg = {"base":"norm_v26.mp4","nframes":1820,
       "memes":[mk.meme(k,F,p) for k,F,p in MEMES],
       "walls":mk.walls("v26","R")}
cfg["memes"][-1]["dur"] = 2.55
json.dump(cfg, open("cfg_v26.json","w"), indent=1)
