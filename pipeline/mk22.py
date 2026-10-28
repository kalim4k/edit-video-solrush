# -*- coding: utf-8 -*-
import json, mk
# V22 : Wild Fox (p0, bleu, son 1 car premier mur a 4.30 s) vs Silent Bear (p1, rouge, son 2).
# L'utilisateur est Silent Bear. Il gagne : arrivee a 52.90 s source -> 55.90 s en sortie.
plan = json.load(open("plan22.json"))
MEMES = [("kevin",200,0),("joe",420,0),("housew",640,0),("supa",1012,1),
         ("narstie",1290,0),("mutahar",1440,0),("applaud",1587,0)]
cfg = {"base":"norm_v22.mp4","nframes":plan["nframes"],
       "memes":[mk.meme(k,F,p) for k,F,p in MEMES],
       "walls":plan["walls"]}
cfg["memes"][-1]["dur"] = 2.80        # applaudissements cales sur l'arrivee
json.dump(cfg, open("cfg_v22.json","w"), indent=1)
