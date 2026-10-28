"""Construit les chaînes de filtres ffmpeg d'un montage à partir d'un cfg_<tag>.json.
   Produit fv_<tag>.txt (vidéo), fa_<tag>.txt (audio) et in_<tag>.txt (liste d'entrées).
   usage : py -3 gen.py <dossier> <cfg.json> <tag>

   Le cfg contient : base (vidéo normalisée), nframes, memes[] et walls[].
   Un mème avec pause=1 gèle le gameplay pendant sa durée : tout ce qui suit est
   décalé, et c'est cette chronologie décalée qui sert à poser les sons et la voix."""
import env
import sys, json, os
MEM = os.path.join(env.MEMES, "")       # dossier des clips, separateur final inclus
BOX_W, BOX_H, BOX_X, BOX_Y = 630, 358, 225, 1510
INNER_W, INNER_H = 620, 348

def build(cfg, tag):
    base = cfg["base"]; nframes = cfg["nframes"]
    memes = cfg["memes"]; walls = cfg["walls"]
    pauses = [(m["F"], m["dur"]) for m in memes if m["pause"]]
    def shift(F):                      # secondes ajoutees avant l'image F d'origine
        return sum(d for pf, d in pauses if F > pf)
    # ---------- entrees ----------
    inputs = ['-i "%s"' % base]
    vparts, aparts = [], []
    # expression de gel
    expr = "PTS" + "".join("+(%.2f/TB)*gte(N,%d)" % (d, pf + 1) for pf, d in pauses)
    vparts.append("[0:v]setpts='%s',fps=30[y0]" % expr)
    idx = 1; cur = "y0"
    for i, m in enumerate(memes, 1):
        T = m["F"] / 30.0 + shift(m["F"])          # debut de l'incrustation, en sortie
        m["T"] = T
        inputs.append('-ss %.2f -t %.2f -i "%s%s.mp4"' % (m["src"], m["dur"], MEM, m["file"]))
        if m.get("key"):
            chain = ("chromakey=0x14FF09:0.26:0.05,scale=-2:400")
            x, y = "(W-w)/2", 1500
        else:
            bw, bh, bx, by = m.get("box", [BOX_W, BOX_H, BOX_X, BOX_Y])
            iw, ih = bw - 10, bh - 10
            pre = (m["pre"] + ",") if m.get("pre") else ""
            chain = ("%sscale=%d:%d:force_original_aspect_ratio=decrease,"
                     "pad=%d:%d:(ow-iw)/2:(oh-ih)/2:white" % (pre, iw, ih, bw, bh))
            x, y = bx, by
        vparts.append("[%d:v]fps=30,%s,setpts=PTS-STARTPTS+%.4f/TB[m%d]" % (idx, chain, T, i))
        nxt = "y%d" % i
        vparts.append("[%s][m%d]overlay=x=%s:y=%s:eof_action=pass:shortest=0:"
                      "enable='between(t,%.4f,%.4f)'[%s]" % (cur, i, x, y, T, T + m["dur"], nxt))
        cur = nxt
        if not m.get("silent"):
            aparts.append("[%d:a]aformat=sample_rates=44100:channel_layouts=stereo,"
                          "asetpts=PTS-STARTPTS,volume=%.1fdB,adelay=%d|%d[a%d]"
                          % (idx, m["gain"], round(T * 1000), round(T * 1000), i))
        idx += 1
    vparts.append("[%s]format=yuv420p[vout]" % cur)
    open(os.path.join(S, "fv_%s.txt" % tag), "w").write(";\n".join(vparts) + "\n")

    # ---------- audio : impacts de murs ----------
    OFF = {1: 5998, 2: 573}            # decalage d'attaque propre a chaque sfx, en echantillons
    n1 = sum(1 for w in walls if w["s"] == 1)
    n2 = len(walls) - n1
    afx = []
    afx.append("[%d:a]asplit=%d%s" % (idx, n1, "".join("[s1_%d]" % k for k in range(n1))))
    afx.append("[%d:a]asplit=%d%s" % (idx + 1, n2, "".join("[s2_%d]" % k for k in range(n2))))
    inputs.append('-i "%s"' % os.path.join(env.SFX, "sfx1.wav"))
    inputs.append('-i "%s"' % os.path.join(env.SFX, "sfx2.wav"))
    c1 = c2 = 0; labels = []
    for w in walls:
        out_f = w["F"] + round(shift(w["F"]) * 30)
        d = out_f * 1470 - OFF[w["s"]]
        if w["s"] == 1: lab, src, c1 = "w1_%d" % c1, "s1_%d" % c1, c1 + 1
        else:           lab, src, c2 = "w2_%d" % c2, "s2_%d" % c2, c2 + 1
        afx.append("[%s]adelay=%dS|%dS[%s]" % (src, d, d, lab))
        labels.append(lab)
    labels += ["a%d" % i for i, m in enumerate(memes, 1) if not m.get("silent")]
    mix = "".join("[%s]" % l for l in labels)
    total = nframes / 30.0 + sum(d for _, d in pauses)
    # apad=whole_dur : apad seul genere du silence a l'infini et ne signale jamais EOF
    afx.append("%samix=inputs=%d:normalize=0:duration=longest:dropout_transition=0,"
               "alimiter=limit=0.95:attack=5:release=60,"
               "apad=whole_dur=%.4f,asetpts=N/SR/TB[aout]" % (mix, len(labels), total))
    open(os.path.join(S, "fa_%s.txt" % tag), "w").write(";\n".join(aparts + afx) + "\n")
    open(os.path.join(S, "in_%s.txt" % tag), "w").write(" ".join(inputs))
    print("%s: %d memes, %d pauses, %d walls, out=%.2fs (%d frames)"
          % (tag, len(memes), len(pauses), len(walls), total, round(total * 30)))
    for m in memes:
        print("   T=%6.2fs  %-45s pause=%s" % (m["T"], m["file"][:45], m["pause"]))

S = sys.argv[1]
cfg = json.load(open(sys.argv[2]))
build(cfg, sys.argv[3])
