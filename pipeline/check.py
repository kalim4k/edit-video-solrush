"""Vérifie que chaque mur a bien un impact sonore net : la crête doit dépasser
   -25 dB dans les 45 ms autour de l'instant du mur, sur la chronologie DE SORTIE
   (gels compris). usage : py -3 check.py <dossier> <cfg.json> <TAG> <audio.wav>"""
import env
import sys, json, subprocess, os
S, cfgf, tag, wav = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
FF = env.FFMPEG
cfg = json.load(open(cfgf))
pauses = [(m["F"], m["dur"]) for m in cfg["memes"] if m["pause"]]
def shift(F): return sum(d for pf, d in pauses if F > pf)
ok = 0
for w in cfg["walls"]:
    t = (w["F"] + round(shift(w["F"]) * 30)) / 30.0
    st = max(0, t - 0.045)
    r = subprocess.run([FF, "-v", "info", "-nostats", "-ss", "%.4f" % st, "-t", "0.09",
                        "-i", wav, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    mx = [l.split()[-2] for l in r.splitlines() if "max_volume" in l]
    mx = float(mx[0]) if mx else -99
    good = mx > -25
    ok += good
    print("  mur f%-5d son%d  t=%6.2fs  crete=%6.1f dB  %s" % (w["F"], w["s"], t, mx, "OK" if good else "!! FAIBLE"))
print("%s : %d/%d impacts nets" % (tag, ok, len(cfg["walls"])))
