# -*- coding: utf-8 -*-
import json, mk
# Clever dude = bleu = l'utilisateur. Premier mur bleu dans les deux -> bleu = son 1.
# V23 : bleu 15 murs / rouge 12. Le bleu gagne, arrivee a 85.70 s (91.70 s en sortie).
# V24 : 15-15. Le rouge gagne, arrivee a 89.70 s (95.70 s en sortie).
SPEC = {
 "v23": ("norm_v23.mp4", 2639, [("joe",490,0),("tension",780,0),("supa",1160,0),
         ("narstie",1680,0),("cut",1900,1),("mutahar",2240,1),("applaud",2571,0)], 2.27),
 "v24": ("norm_v24.mp4", 2777, [("joe",460,0),("tension",800,0),("housew",1320,0),
         ("narstie",1620,0),("pleure",2030,1),("vertic",2350,1),("martin",2691,0)], 2.87),
}
for tag, (base, nf, ms, dfin) in SPEC.items():
    cfg = {"base":base, "nframes":nf,
           "memes":[mk.meme(k,F,p) for k,F,p in ms],
           "walls":mk.walls(tag, "B")}
    cfg["memes"][-1]["dur"] = dfin        # dernier meme cale pile sur l'arrivee
    json.dump(cfg, open("cfg_%s.json" % tag, "w"), indent=1)
