# edit-video-solrush

Chaîne de montage automatisée pour les parties de **SolRush** / WallRush (Quoridor en ligne).
À partir d'une capture d'écran de partie — ou directement d'un lien de rejeu — elle produit
une vidéo verticale 1080×1920 avec un effet sonore sur chaque mur posé et des mèmes incrustés.

25 montages produits à ce jour.

---

## Ce que fait la chaîne

1. **Normaliser** — recadrer la capture pour ne garder que les badges des joueurs (avec leurs
   compteurs de murs) et le plateau, puis mettre à l'échelle sur fond blanc en 1080×1920.
   Le blanc du bas sert de bande à mèmes.
2. **Détecter les murs** — isoler le rouge et le bleu par `colorchannelmixer`, mesurer la
   luminance moyenne du plateau image par image, et repérer les marches (`steps.py`).
3. **Recouper** — comparer le nombre de murs trouvés aux compteurs affichés en jeu, relevés
   par zoom sur les badges à une dizaine d'instants. Les deux doivent concorder exactement.
4. **Poser les mèmes** — incrustations dans la bande blanche, certaines avec gel du gameplay.
5. **Rendre** — `gen.py` écrit les chaînes de filtres, `rend.sh` produit image et son.
6. **Vérifier** — `check.py` contrôle que chaque mur a bien un impact sonore net.
7. **Muxer** — `muxnu.sh`.

## Utilisation

Les scripts s'appellent **par leur chemin**, depuis un dossier de travail vide — ils ne se
copient pas, c'est ainsi qu'ils retrouvent les mèmes et les sons d'impact.

```bash
P=$PWD/pipeline
python3 "$P/env.py"                     # verifie que tout se resout
mkdir -p travail && cd travail

# 1. detection + normalisation, en un seul decodage
bash "$P/job2.sh" <source.mp4> "<crop-plateau>" "<crop-cadrage>" <tag> norm_<tag>

# 2. marches -> murs
for c in R B; do python3 "$P/steps.py" y_<tag>$c.tsv > st_<tag>$c.tsv; done

# 3. config (memes + murs) : ecrire un petit script sur le modele de mk25.py

# 4. filtres, rendu, verification, mux
python3 "$P/gen.py" "$PWD" cfg_<tag>.json <tag>
bash "$P/rend.sh" <tag> <nb_images> <duree>
bash "$P/muxnu.sh" <tag> "montage_V<NN>_<Joueur1>-vs-<Joueur2>.mp4"
```

Les chemins se règlent par variables d'environnement — `FFMPEG_BIN` si ffmpeg n'est pas dans
le `PATH`, `SOLRUSH_MEMES`, `SOLRUSH_SORTIE`, `SOLRUSH_SOURCES`, `SOLRUSH_RACINE` — avec un
repli sur la structure du dépôt. Aucun chemin n'est codé en dur.

## Partir d'un lien de rejeu (plus fiable)

`solrush.site` expose ses rejeux : `GET /api/replay?t=<token>` renvoie le `move_log` complet,
les pseudos et le vainqueur, **sans authentification** — le lien fait office d'autorisation,
c'est écrit dans le code du site. Plus aucune détection n'est alors nécessaire.

`cdp.py` est un client Chrome DevTools minimal (WebSocket écrit à la main, sans dépendance).
`capture.py` l'utilise pour piloter le lecteur de rejeu en Chrome invisible et capturer les
positions une par une ; `monter22.py` assemble ensuite avec un rythme choisi — mur tenu
33 images, coup de pion 14 — ce qui donne un montage bien plus dense qu'un rejeu lu en direct.

## Règles de montage

- **Son 1 au joueur qui pose le plus de murs.** En cas d'égalité, à celui qui pose le premier.
- **Les mèmes sont systématiques.** Le gel du gameplay, lui, est au cas par cas.
- **Une incrustation ne recouvre jamais l'action qui l'a déclenchée** — d'où la bande blanche
  dédiée sous le plateau, à `x=225 y=1510`, 630×358.
- **Pas de commentaire généré** (règle du 28/10/2026). Le dossier contient encore l'outillage
  de synthèse vocale (`voix.py`, `el2.py`, `accents.py`, `punch.py`, `mkfx.py`), inutilisé.

## Cadrages par disposition

| Disposition | Cadrage image | Cadrage plateau (détection) |
|---|---|---|
| WallRush arrivée 568×1280 | `552:860:8:200` | `484:684:44:340` |
| WallRush arrivée 568×1280 défilée | `552:860:8:150` | `484:690:44:285` |
| WallRush arrivée 852×1920 | `828:1290:12:225` | `726:1035:66:427` |
| WallRush duel 568×1280 | `552:760:8:100` | `528:490:20:395` |
| SolRush duel 568×1280 | `560:820:4:135` | `544:548:12:350` |
| SolRush duel 852×1920 | `840:1230:6:202` | `816:822:18:525` |
| SolRush arrivée 568×1280 | `560:865:4:140` | `484:670:44:290` |
| SolRush arrivée 568×1280, rejeu navigateur | `560:870:4:130` | `496:680:40:280` |
| Rejeu capturé par CDP (860×1864) | `840:1340:10:120` | — |

Toutes se normalisent ensuite par `scale=900:-2,pad=1080:1920:90:100:white`.

## Pièges rencontrés, et leur cause

- **`apad` seul fige le rendu.** Il génère du silence à l'infini et ne signale jamais la fin ;
  `atrim` en aval ne suffit pas. Toujours `apad=whole_dur=<durée>`.
- **`metadata=print:file=C:/...` ne se parse pas** : le deux-points de la lettre de lecteur
  casse l'analyseur de filtres. Se placer dans le dossier et n'utiliser que des noms relatifs.
- **`signalstats` exige du YUV.** Sur une image RGB, `SATAVG` n'est jamais écrit.
- **Le démultiplexeur `concat` rejoue la dernière durée** à cause de l'entrée finale répétée
  qu'il impose. Couper au nombre exact avec `-frames:v N`.
- **Détection d'arrivée** : les murs de la couleur recherchée traversent aussi la zone
  d'arrivée. Distinguer par la forme — un mur fait ~22 px d'épaisseur après mise à l'échelle,
  une bille ~48 (`arrivee.py`).
- **Synthèse vocale** : n'envoyer que du français **accentué**. « ca » est épelé « KA » et
  « capte » est lu au présent. `accents.py` bloque avant de facturer des caractères.
  Par ailleurs `style=0.35` combiné à `stability=0.45` produisait des hallucinations en début
  de phrase ; `style=0.0, stability=0.75` les a supprimées.

## Dépendances

ffmpeg 9.0.1, Python 3.12 avec Pillow, et Chrome pour la capture de rejeu.
Les rushes et les rendus ne sont pas versionnés ; `pipeline/sfx/` contient les deux sons
d'impact, qui sont les seuls binaires nécessaires.
