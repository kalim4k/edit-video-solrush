# -*- coding: utf-8 -*-
import json, mk
# V20 : User6781 (rouge) vs araliomar47 (bleu). Premier mur = rouge (5.57 s) -> rouge = son 1.
# Arrivee : la bille rouge entre dans la zone a 100.37 s source -> 106.37 s en sortie. User6781 gagne.
MEMES = [("joe",500,0),("tension",760,0),("supa",1290,1),("narstie",1610,0),("mutahar",1840,0),
         ("cut",2070,0),("pleure",2460,1),("housew",2750,0),("applaud",3011,0)]
cfg = {"base":"norm_v20.mp4","nframes":3080,
       "memes":[mk.meme(k,F,p) for k,F,p in MEMES],
       "walls":mk.walls("v20","R")}
cfg["memes"][-1]["dur"] = 2.30          # applaudissements cales pile sur l'arrivee, sans depasser la fin
json.dump(cfg, open("cfg_v20.json","w"), indent=1)
