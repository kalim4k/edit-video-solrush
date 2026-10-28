# -*- coding: utf-8 -*-
"""Refuse d'envoyer a ElevenLabs du francais desaccentue.
La voix lit litteralement ce qu'on lui donne : "capte" sort au present au lieu
de "capté", et "ca" est epele "KA" au lieu de "ça"."""
import re, unicodedata

# Mots dont TOUTES les orthographes francaises valides portent un accent :
# les rencontrer sans accent est forcement une faute. -> blocant.
TOUJOURS = {
 "ca":"ça", "deja":"déjà", "voila":"voilà", "au-dela":"au-delà",
 "tres":"très", "apres":"après", "pres":"près", "expres":"exprès",
 "succes":"succès", "acces":"accès", "proces":"procès", "exces":"excès",
 "progres":"progrès", "des":"dès", "regle":"règle", "regles":"règles",
 "meme":"même", "memes":"mêmes", "etre":"être", "etait":"était",
 "etais":"étais", "etaient":"étaient", "ete":"été", "etes":"êtes",
 "arrete":"arrête", "arretes":"arrêtes", "arreter":"arrêter",
 "depense":"dépense", "depenses":"dépenses", "depenser":"dépenser",
 "fenetre":"fenêtre", "tete":"tête", "bete":"bête", "pret":"prêt",
 "derniere":"dernière", "premiere":"première", "maniere":"manière",
 "derriere":"derrière", "entiere":"entière", "lumiere":"lumière",
 "annee":"année", "annees":"années", "idee":"idée", "idees":"idées",
 "cle":"clé", "cles":"clés", "cote":"côté", "gout":"goût",
 "probleme":"problème", "systeme":"système", "theme":"thème",
 "secondes":"secondes", "numero":"numéro", "resultat":"résultat",
 "reponse":"réponse", "repondre":"répondre", "decale":"décalé",
 "termine":"terminé", "terminee":"terminée", "prefere":"préfère",
}
# Participes en -e qui existent AUSSI au present : ambigus, donc simple avis.
DOUTEUX = ("capt", "cram", "gagn", "pieg", "bloqu", "enchain", "cass",
           "prepar", "expliqu", "commenc", "lach", "lanc", "vid", "remplac")
SUFF = ("e", "es", "ee", "ees")

def _nu(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

def _mots(t):
    for bloc in re.findall(r"[A-Za-zÀ-ÿ'’-]+", t):
        for mot in re.split(r"['’-]", bloc):
            if mot: yield mot

def verifier(lignes, strict=True):
    """Affiche le texte exact envoye, bloque sur les fautes certaines,
    signale les participes douteux. Renvoie (fautes, avis)."""
    fautes, avis = [], []
    print("  texte envoye a ElevenLabs :")
    for i, t in enumerate(lignes):
        print("    %2d | %s" % (i, t))
        for mot in _mots(t):
            if _nu(mot) != mot: continue          # deja accentue
            bas = mot.lower()
            if bas in TOUJOURS:
                fautes.append((i, mot, TOUJOURS[bas]))
            elif any(bas.startswith(v) and bas[len(v):] in SUFF for v in DOUTEUX):
                avis.append((i, mot))
    for i, mot, corr in fautes:
        print('  ! FAUTE  ligne %d : "%s" doit s\'ecrire "%s"' % (i, mot, corr))
    for i, mot in avis:
        print('  ? a verifier  ligne %d : "%s" — participe passe attendu ?' % (i, mot))
    if fautes and strict:
        raise SystemExit("texte desaccentue : corrige avant de depenser des caracteres")
    return fautes, avis
