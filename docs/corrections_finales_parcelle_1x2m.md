# Corrections Finales : Parcelle Réelle 1m × 2m
## Binôme A : Projet Robot Aérien Autonome

---

## 1. Source Corrigée : Courbe de Décharge LiPo

**Lien vérifié et fonctionnel** : https://letusrc.com/lipo-vs-lihv/

**Données extraites (LiPo 1S)** :

| Capacité (%) | Tension (V) | Action recommandée |
|--------------|-------------|-------------------|
| 100% | 4.200V | Chargée complète |
| 90% | 4.070V | Prête à l'emploi |
| 80% | 3.963V | Zone sûre |
| 70% | 3.898V | Zone sûre |
| 60% | 3.835V | Zone sûre |
| 50% | 3.789V | Nominale |
| 40% | 3.756V | Zone attention |
| 30% | 3.733V | Zone attention |
| 20% | 3.707V | RTH recommandé |
| 15% | 3.685V | Zone critique |
| 10% | 3.664V | Urgence |
| 5% | 3.618V | Danger |
| 0% | 3.200V | Cutoff (dommages irréversibles) |

**Référence** : letusrc.com (2024). "LiPo vs. LiHV: Discharge Curve Chart, Voltage Chart, Capacity Chart."

---

## 2. Recalcul Complet : Parcelle 1m × 2m

### 2.1 Paramètres de la parcelle

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Largeur | 1.0 m | Instructions encadrants |
| Longueur | 2.0 m | Instructions encadrants |
| Surface | 2.0 m² | Calcul |
| Nombre de pots | 12 | Configuration 3×4 |
| Diamètre pot | 10.5 cm | Instructions encadrants |
| Hauteur pot | 12 cm | Instructions encadrants |

### 2.2 Positionnement Optimal des Pots

**Disposition** : 3 colonnes × 4 rangées

**Calcul de l'espacement** :
```
Marge de sécurité (bord) : 10 cm = 0.10 m
Largeur utile : 1.0 - 2 × 0.10 = 0.80 m
Longueur utile : 2.0 - 2 × 0.10 = 1.80 m

Espacement X (centre à centre) : 0.80 / (3-1) = 0.40 m
Espacement Y (centre à centre) : 1.80 / (4-1) = 0.60 m

Distance bord à bord (X) : 0.40 - 0.105 = 0.295 m
Distance bord à bord (Y) : 0.60 - 0.105 = 0.495 m
```

**Coordonnées des 12 pots** (origine = coin inférieur gauche) :

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

### 2.3 Paramètres de Mission Recalculés

**Formules appliquées** :
```
GSD = (p × H) / f = (2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.44 mm/pixel

Wx = (Nx × p × H) / f = (1600 × 2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.70 m
Wy = (Ny × p × H) / f = (1200 × 2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.52 m

dx = Wx × (1 - 0.75) = 0.70 × 0.25 = 0.175 m
dy = Wy × (1 - 0.65) = 0.52 × 0.35 = 0.182 m

Lignes = ⌈2.0 / 0.182⌉ = 11 lignes
Photos/ligne = ⌈1.0 / 0.175⌉ = 6 photos
Total photos = 11 × 6 = 66

Distance = 11 × 1.0 + 10 × 0.182 = 12.82 m
Temps = 12.82 / 0.20 = 64.1 s = 1.07 min
Batterie = 64.1 / 480 = 13.4%
```

**Tableau récapitulatif** :

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Altitude | 0.70 m | GSD 0.44mm, champ suffisant |
| Vitesse | 0.20 m/s | Flou < 0.5px |
| GSD | 0.44 mm/pixel | Résolution sub-millimétrique |
| Emprise | 0.70m × 0.52m | Calcul optique |
| Recouvrement frontal | 75% | Standard photogrammétrie |
| Recouvrement latéral | 65% | Compromis couverture |
| Photos | 66 | 11 lignes × 6 photos |
| Distance | 12.82 m | Calcul géométrique |
| Temps | 1.07 min | 64.1 secondes |
| **Batterie** | **13.4%** | **Sécurisé** ✅ |

---

## 3. Comparaison Vol Continu vs Stop-and-Capture (Parcelle 1×2m)

### 3.1 Vol Continu

```
Temps = 64.1 s = 1.07 min
Batterie = 13.4%
Statut : ✅ EXCELLENT
```

### 3.2 Stop-and-Capture

```
Stabilisation = 66 × 0.4s = 26.4s
Temps total = 64.1 + 26.4 = 90.5s = 1.51 min
Batterie = 90.5 / 480 = 18.9%
Statut : ✅ FAISABLE (mais moins efficace)
```

### 3.3 Conclusion

Sur la petite parcelle (1×2m), **les deux modes sont faisables** :
- Vol continu : 13.4% batterie
- Stop-and-Capture : 18.9% batterie

**Le vol continu reste plus efficace** (13.4% vs 18.9%), mais le Stop-and-Capture est réalisable.

---

## 4. Sources Corrigées

| Source | Lien vérifié | Sujet |
|--------|--------------|-------|
| **LiPo Voltage Chart** | https://letusrc.com/lipo-vs-lihv/ | Courbe de décharge |
| **OV2640 Datasheet** | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/OV2640-datasheet.pdf | Spécifications caméra |
| **PyDrone GitHub** | https://github.com/01studio-lab/pyDrone | Documentation drone |
| **Ublox GPS** | https://www.u-blox.com/en/product/neo-m8-series | Spécifications GPS |
| **ExG Reference** | https://elibrary.asabe.org/abstract.asp?AID=33478 | Woebbecke 1995 |
| **GRVI Reference** | https://www.sciencedirect.com/science/article/abs/pii/0034425779900130 | Tucker 1979 |
| **RandomForest** | https://link.springer.com/article/10.1023/A:1010933404324 | Breiman 2001 |

---

## 5. Prochaines Étapes

1. ✅ Source LiPo corrigée
2. ✅ Paramètres recalculés pour 1m × 2m
3. 🔄 Régénérer les images avec pots correctement positionnés
4. 🔄 Mettre à jour le rapport final
5. 🔄 Préparer les livrables pour encadreurs

---

*Document créé le 14 juillet 2026*
*Binôme A : Corrections finales*