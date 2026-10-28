"""Détecteur de marches : repère les sauts de luminance d'un canal couleur,
   c'est-à-dire l'apparition d'un mur. Entrée : y_<tag><R|B>.tsv (image, YAVG).
   Sortie : image, seconde, amplitude — une ligne par mur détecté.
   La 1re ligne correspond à l'apparition du plateau, à ignorer en aval."""
import sys
f=sys.argv[1]; W=8
y=[float(l.split('\t')[1]) for l in open(f) if l.strip()]
n=len(y)
def m(a,b):
    a=max(0,a); b=min(n,b)
    return sum(y[a:b])/max(1,b-a)
d=[m(i+2,i+2+W)-m(i-1-W,i-1) for i in range(n)]
cand=[]
for i in range(n):
    if d[i]<=0.06: continue
    if d[i]==max(d[max(0,i-9):i+10]): cand.append((i,d[i]))
# fusionne les voisins a moins de 8 images, en gardant le maximum
out=[]
for i,v in cand:
    if out and i-out[-1][0]<=8:
        if v>out[-1][1]: out[-1]=(i,v)
    else: out.append((i,v))
for i,v in out: print(f"{i}\t{i/30:.2f}\t{v:.3f}")
