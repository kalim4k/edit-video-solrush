# -*- coding: utf-8 -*-
import json
def timeline(cfg_path, fin_frame=None):
    c = json.load(open(cfg_path))
    pauses = [(m["F"], m["dur"]) for m in c["memes"] if m["pause"]]
    def t(F): return F/30.0 + sum(d for pf,d in pauses if F > pf)
    murs = sorted(((t(w["F"]), w["s"]) for w in c["walls"]))
    memes = [(t(m["F"]), t(m["F"])+m["dur"]) for m in c["memes"]]
    total = c["nframes"]/30.0 + sum(d for _,d in pauses)
    return murs, memes, total, (t(fin_frame) if fin_frame else None)
