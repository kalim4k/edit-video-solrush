# -*- coding: utf-8 -*-
import json, mk
# V25 : Clever dude (bleu, l'utilisateur) vs Sly Tiger (rouge).
# Rouge pose 15 murs, bleu 11 -> ROUGE prend le son 1 (il en pose le plus).
# Le bleu gagne quand meme : arrivee a 83.20 s source -> 89.20 s en sortie.
MEMES = [("joe",490,0),("tension",650,0),("housew",1060,0),("cut",1250,0),
         ("supa",1790,1),("narstie",2080,1),("applaud",2496,0)]
cfg = {"base":"norm_v25.mp4","nframes":2597,
       "memes":[mk.meme(k,F,p) for k,F,p in MEMES],
       "walls":mk.walls("v25","R")}
cfg["memes"][-1]["dur"] = 3.00
json.dump(cfg, open("cfg_v25.json","w"), indent=1)
