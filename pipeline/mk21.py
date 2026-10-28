# -*- coding: utf-8 -*-
import json, mk
# V21 : User6781 (rouge) vs lis42 (bleu). Premier mur = rouge (6.70 s) -> rouge = son 1.
# Arrivee : la bille bleue entre dans la zone a 106.60 s source -> 112.60 s en sortie. lis42 gagne.
MEMES = [("joe",600,0),("cut",1060,1),("housew",1620,0),("supa",1930,0),("tension",2250,0),
         ("narstie",2530,0),("vertic",2800,1),("pleure",3000,0),("martin",3198,0)]
cfg = {"base":"norm_v21.mp4","nframes":3258,
       "memes":[mk.meme(k,F,p) for k,F,p in MEMES],
       "walls":mk.walls("v21","R")}
cfg["memes"][-1]["dur"] = 2.00          # le meme de defaite tombe pile sur l'arrivee adverse
json.dump(cfg, open("cfg_v21.json","w"), indent=1)
