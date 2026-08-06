# Paramètres Optimaux - Parcelle Réelle 1m × 2m
## Binôme A - Projet Robot Aérien Autonome

---

## 📋 Résumé Exécutif

Ce document présente les **paramètres optimaux calculés** pour la parcelle réelle de **1m × 2m**, avec les **calculs détaillés** et les **justifications** pour chaque valeur.

---

## 1. Caractéristiques de la Parcelle

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Largeur (X) | **1.0 m** | Instructions encadrants |
| Longueur (Y) | **2.0 m** | Instructions encadrants |
| Surface | **2.0 m²** | Calcul : 1.0 × 2.0 |
| Nombre de pots | **12** | Configuration 3×4 |
| Diamètre pot | **10.5 cm** | Instructions encadrants |
| Hauteur pot | **12 cm** | Instructions encadrants |

---

## 2. Positionnement Optimal des Pots

### 2.1 Calcul de l'espacement

```
Marge de sécurité (bord) : 10 cm = 0.10 m

Largeur utile : 1.0 - 2 × 0.10 = 0.80 m
Longueur utile : 2.0 - 2 × 0.10 = 1.80 m

Espacement X (centre à centre) : 0.80 / (3-1) = 0.40 m
Espacement Y (centre à centre) : 1.80 / (4-1) = 0.60 m

Distance bord à bord (X) : 0.40 - 0.105 = 0.295 m
Distance bord à bord (Y) : 0.60 - 0.105 = 0.495 m
```

### 2.2 Coordonnées des 12 pots

| Pot | X (m) | Y (m) | Position |
|-----|-------|-------|----------|
| P1 | 0.10 | 0.10 | Coin inférieur gauche |
| P2 | 0.50 | 0.10 | Centre inférieur |
| P3 | 0.90 | 0.10 | Coin inférieur droit |
| P4 | 0.10 | 0.70 | 2ème rangée gauche |
| P5 | 0.50 | 0.70 | 2ème rangée centre |
| P6 | 0.90 | 0.70 | 2ème rangée droite |
| P7 | 0.10 | 1.30 | 3ème rangée gauche |
| P8 | 0.50 | 1.30 | 3ème rangée centre |
| P9 | 0.90 | 1.30 | 3ème rangée droite |
| P10 | 0.10 | 1.90 | Coin supérieur gauche |
| P11 | 0.50 | 1.90 | Centre supérieur |
| P12 | 0.90 | 1.90 | Coin supérieur droit |

---

## 3. Paramètres de Mission Optimaux

### 3.1 Altitude de vol : H = 0.70 m

**Formule** : `GSD = (p × H) / f`

**Calcul** :
```
GSD = (2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.44 mm/pixel
```

**Justification** :
- Résolution sub-millimétrique (0.44 mm/pixel)
- Permet d'observer les feuilles individuelles
- Suffisant pour détecter le stress hydrique

### 3.2 Emprise au sol

**Formule** : `Wx = (Nx × p × H) / f`

**Calcul** :
```
Wx = (1600 × 2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.70 m
Wy = (1200 × 2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.52 m
```

**Résultat** : Emprise = **0.70m × 0.52m**

### 3.3 Vitesse de vol : v = 0.20 m/s

**Formule** : `v_max = (GSD × blur_limit) / T_exp`

**Calcul** :
```
v_max = (0.44×10⁻³ × 0.5) / (1/1000) = 0.22 m/s
```

**Justification** :
- Flou = 0.20 × (1/1000) = 0.0002 m = 0.2 mm
- Flou en pixels = 0.2 / 0.44 = 0.45 pixel < 0.5 pixel (acceptable)
- **Images nettes garanties**

### 3.4 Recouvrement

| Paramètre | Valeur | Formule | Justification |
|-----------|--------|---------|---------------|
| Frontal | 75% | `dx = Wx × (1 - 0.75)` | Standard photogrammétrie |
| Latéral | 65% | `dy = Wy × (1 - 0.65)` | Compromis couverture |

**Calcul** :
```
dx = 0.70 × (1 - 0.75) = 0.175 m
dy = 0.52 × (1 - 0.65) = 0.182 m
```

### 3.5 Nombre de photos

**Calcul** :
```
Lignes = ⌈2.0 / 0.182⌉ = 11 lignes
Photos/ligne = ⌈1.0 / 0.175⌉ = 6 photos
Total photos = 11 × 6 = 66 photos
```

### 3.6 Distance et temps de mission

**Calcul** :
```
Distance = 11 × 1.0 + 10 × 0.182 = 12.82 m
Temps = 12.82 / 0.20 = 64.1 s = 1.07 min
Batterie = 64.1 / 480 = 13.4%
```

---

## 4. Tableau Récapitulatif

| Paramètre | Valeur | Formule | Justification |
|-----------|--------|---------|---------------|
| **Altitude** | 0.70 m | Choix technologique | GSD 0.44mm, champ suffisant |
| **Vitesse** | 0.20 m/s | Calcul anti-flou | Flou < 0.5px |
| **GSD** | 0.44 mm/pixel | (p × H) / f | Résolution sub-millimétrique |
| **Emprise** | 0.70m × 0.52m | (N × p × H) / f | Couverture optimale |
| **Recouvrement frontal** | 75% | Standard | Couverture complète |
| **Recouvrement latéral** | 65% | Standard | Compromis |
| **Espacement photos** | 0.175 m | Wx × (1 - 0.75) | - |
| **Espacement lignes** | 0.182 m | Wy × (1 - 0.65) | - |
| **Nombre de lignes** | 11 | ⌈2.0 / 0.182⌉ | - |
| **Photos par ligne** | 6 | ⌈1.0 / 0.175⌉ | - |
| **Total photos** | 66 | 11 × 6 | - |
| **Distance totale** | 12.82 m | Calcul géométrique | - |
| **Temps de mission** | 1.07 min | Distance / vitesse | - |
| **Consommation batterie** | 13.4% | Temps / autonomie | **Sécurisé** ✅ |

---

## 5. Comparaison des Modes de Vol

### 5.1 Vol Continu

```
Temps = 64.1 s = 1.07 min
Batterie = 13.4%
Statut : ✅ EXCELLENT
```

### 5.2 Stop-and-Capture

```
Stabilisation = 66 × 0.4s = 26.4s
Temps total = 64.1 + 26.4 = 90.5s = 1.51 min
Batterie = 90.5 / 480 = 18.9%
Statut : ✅ FAISABLE (mais moins efficace)
```

### 5.3 Conclusion

| Mode | Temps | Batterie | Statut |
|------|-------|----------|--------|
| **Vol Continu** | 1.07 min | 13.4% | ✅ **Recommandé** |
| Stop-and-Capture | 1.51 min | 18.9% | ✅ Faisable |

**Le vol continu est 1.4× plus efficace en énergie.**

---

## 6. Sources et Références

| Source | Lien | Sujet |
|--------|------|-------|
| **LiPo Voltage** | https://letusrc.com/lipo-vs-lihv/ | Courbe de décharge |
| **OV2640 Datasheet** | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/OV2640-datasheet.pdf | Spécifications caméra |
| **Woebbecke 1995** | https://elibrary.asabe.org/abstract.asp?AID=33478 | Indice ExG |
| **Tucker 1979** | https://www.sciencedirect.com/science/article/abs/pii/0034425779900130 | Indice GRVI |
| **Breiman 2001** | https://link.springer.com/article/10.1023/A:1010933404324 | RandomForest |

---

*Document créé le 14 juillet 2026*
*Binôme A - Paramètres optimaux parcelle 1m × 2m*