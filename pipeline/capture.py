# -*- coding: utf-8 -*-
"""Capture image par image un rejeu SolRush depuis son lien partage.
   usage : py -3 capture.py <token> <dossier>"""
import env
import cdp, time, os, sys, json

CH = env.chrome()
token, dossier = sys.argv[1], sys.argv[2]
os.makedirs(dossier, exist_ok=True)

c = cdp.Chrome(CH)
try:
    c.cmd("Page.enable"); c.cmd("Runtime.enable")
    c.cmd("Emulation.setDeviceMetricsOverride", width=430, height=932,
          deviceScaleFactor=2, mobile=True)
    c.cmd("Page.navigate", url="https://solrush.site/r/" + token)

    ecran = ""
    for _ in range(60):
        time.sleep(0.5)
        ecran = c.js("([...document.querySelectorAll('[id^=screen-]')]"
                     ".find(e=>getComputedStyle(e).display!=='none')||{}).id")
        if ecran == "screen-game": break
    if ecran != "screen-game":
        raise SystemExit("le rejeu ne s'est pas ouvert (ecran = %s)" % ecran)
    time.sleep(1.5)

    titre = c.js("document.getElementById('rp-title').textContent")
    # la barre de lecture ne doit pas apparaitre a l'image ; les clics passent quand meme
    c.js("document.getElementById('rp-close').closest('div').style.visibility='hidden'")
    c.js("document.getElementById('rp-start').click()")
    time.sleep(0.8)

    total = int(c.js("document.getElementById('rp-count').textContent").split("/")[1])
    print("rejeu : %s  |  %d positions" % (titre.strip(), total))

    etats = []
    for i in range(total + 1):
        pos = c.js("document.getElementById('rp-count').textContent")
        murs = c.js("""[...document.querySelectorAll('[id^=screen-] .chip, .pcard, .player')]
                       .length""")
        c.capture(os.path.join(dossier, "f%04d.png" % i))
        etats.append(pos)
        if i % 10 == 0: print("   %s" % pos, flush=True)
        if i < total:
            c.js("document.getElementById('rp-next').click()")
            time.sleep(0.10)
    json.dump({"titre": titre.strip(), "total": total, "etats": etats},
              open(os.path.join(dossier, "etats.json"), "w"))
    print("termine : %d images dans %s" % (total + 1, dossier))
finally:
    c.fermer()
