# Mode d'emploi — monter une partie SolRush

Ce fichier s'adresse à un assistant qui reprend le travail. Il décrit **les décisions**,
pas seulement les commandes ; l'outillage est décrit dans le README.

**Prérequis : un shell, ffmpeg et Python 3 avec Pillow.** Sans ffmpeg il est impossible de
produire une vidéo — se limiter alors à conseiller et à préparer les commandes.

**Ne pas copier les scripts.** Se placer dans un dossier de travail vide et les appeler
**par leur chemin** : c'est ainsi qu'ils retrouvent la racine du dépôt, donc les mèmes et les
sons d'impact. Tous les fichiers intermédiaires sont écrits dans le dossier courant.

```bash
P=/chemin/vers/le/depot/pipeline
mkdir -p travail && cd travail
python3 "$P/env.py"          # verifie que tout se resout avant de commencer
```

`env.py` règle les chemins par variables d'environnement, avec un repli sur la structure du
dépôt : `FFMPEG_BIN` si ffmpeg n'est pas dans le `PATH`, `SOLRUSH_MEMES`, `SOLRUSH_SORTIE`,
`SOLRUSH_SOURCES`, `SOLRUSH_RACINE`. Rien n'est codé en dur.

---

## 1. Identifier la partie

Deux cas.

**La personne envoie un lien `solrush.site/r/<token>`** — c'est le cas le plus sûr :

```bash
curl -s "https://solrush.site/api/replay?t=<token>" -o replay.json
```

Le JSON donne `p0_nick`, `p1_nick`, `winner`, `reason` et `move_log` (chaque coup : `type`
valant `pawn` ou `wall`, plus `c`, `r`, `o`). **Les joueurs alternent et p0 commence**, donc
le joueur d'un coup est `index % 2`. Aucune détection n'est alors nécessaire : on connaît
exactement les murs, leur couleur, leur ordre et le vainqueur. `capture.py` récupère ensuite
l'image en pilotant le lecteur de rejeu, et `monter22.py` assemble au rythme voulu.

**La personne envoie une capture d'écran** — il faut tout déduire de l'image (section 2).

## 2. Mesurer avant de lancer quoi que ce soit

Une passe de détection coûte une dizaine de minutes : ne jamais la lancer sur un cadrage
supposé. Extraire une image en pleine résolution au milieu de la partie, repérer la bande
verte d'arrivée et l'étendue des murs, puis **vérifier le cadrage à l'œil** en dessinant la
zone de détection par-dessus (`drawbox`) avant de lancer. Le README donne les cadrages déjà
validés par disposition ; une disposition identique au pixel près se réutilise telle quelle.

Le cadrage image doit contenir **les badges des joueurs avec leurs compteurs de murs** et le
plateau entier, et exclure le chrome du navigateur, la barre d'état du téléphone et la barre
de lecture. Après `scale=900:-2,pad=1080:1920:90:100:white`, le contenu doit se terminer
**au-dessus de y=1510**, où commence la bande à mèmes.

## 3. Détecter, puis recouper — les deux, toujours

```bash
bash "$P/job2.sh" <source.mp4> "<crop-plateau>" "<crop-cadrage>" <tag> norm_<tag>
for c in R B; do python3 "$P/steps.py" y_<tag>$c.tsv > st_<tag>$c.tsv; done
```

La première ligne de chaque fichier `st_` est l'apparition du plateau : elle ne compte pas.
`mk.walls()` l'ignore déjà et filtre les amplitudes sous 0,15 (artefacts de billes).

**Recouper systématiquement** le nombre de murs trouvés avec les compteurs affichés en jeu :
extraire la bande des badges (`crop=560:52:4:158` pour une source 568×1280) à une dizaine
d'instants, **agrandie** — sur une vignette basse résolution un « 4 » a déjà été lu « 11 ».
Les deux comptes doivent concorder exactement. Sinon, le cadrage ou le seuil est en cause :
ne pas poursuivre.

## 4. Déterminer l'issue

`arrivee.py` donne l'instant où une bille atteint la zone d'arrivée, donc le vainqueur.
Attention : les murs de la couleur cherchée traversent aussi cette zone — le script
distingue par la forme (mur ~22 px d'épaisseur après mise à l'échelle, bille ~48).
**Vérifier le résultat à l'image** en extrayant quelques vignettes de la fin : certaines
captures s'arrêtent avant l'arrivée, et le montage ne doit alors annoncer aucun vainqueur.

## 5. Mèmes et gels

Les mèmes sont **systématiques**, environ un toutes les dix à quinze secondes, placés
**après** le fait qui les motive. Ils s'incrustent dans la bande blanche sous le plateau,
donc ils ne masquent jamais le jeu.

Le **gel** du gameplay (`pause: 1`) est au cas par cas, deux par montage environ, réservé aux
bascules de la partie. Un gel ne doit jamais tomber sur une pose de mur : vérifier l'écart au
mur le plus proche, viser au moins 0,7 s.

Caler le dernier mème sur l'arrivée, et ajuster sa durée pour ne pas dépasser la fin.

## 6. Son des murs

**Le joueur qui pose le plus de murs prend le son 1**, l'autre le son 2. En cas d'égalité —
fréquent — **le premier à poser un mur prend le son 1**. Appliquer la règle même quand elle
attribue le son 1 à l'adversaire, et le signaler, car cela s'entend d'une vidéo à l'autre.

## 7. Rendre et vérifier

```bash
python3 "$P/gen.py" "$PWD" cfg_<tag>.json <tag>
bash "$P/rend.sh" <tag> <nb_images> <duree>
bash "$P/muxnu.sh" <tag> "montage_V<NN>_<Joueur1>-vs-<Joueur2>.mp4"
```

Trois contrôles, à rapporter tels quels :

1. le nombre d'images rendues doit égaler le nombre attendu ;
2. `check.py` doit donner **tous** les impacts nets ;
3. les comptes de murs doivent concorder avec les compteurs du jeu.

Un contrôle qui échoue se corrige, il ne se contourne pas.

## 8. Ce qu'on ne fait plus

- **Aucun commentaire généré** (demandé le 28/10/2026). L'outillage de synthèse vocale reste
  dans le dépôt mais n'est pas utilisé, et il ne faut pas le reproposer.
- **Aucun effet sonore sur les punchlines** (abandonné le 26/09/2026).

## 9. Nommage et livraison

Les montages vont dans `SORTIE/` sous la forme
`montage_V<NN>_<Joueur1>-vs-<Joueur2>.mp4`, un seul fichier par vidéo. Les essais portent un
préfixe `_`. La personne travaille en français ; les rapports de livraison indiquent la durée,
le compte de murs par couleur, les contrôles passés, et signalent franchement ce qui a échoué.
