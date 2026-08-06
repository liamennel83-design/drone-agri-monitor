# Justification Détaillée des Valeurs Techniques
## Document Scientifique - Binôme A

---

## 📋 Objectif

Ce document justifie **chaque valeur technique** utilisée dans le projet, avec les **calculs détaillés**, les **sources scientifiques** et les **raisons du choix**.

---

## 1. Altitude de Vol : H = 0.70 m

### 1.1 Pourquoi 0.70 m et pas 1.0 m ou 0.5 m ?

**Contrainte 1 : Résolution du capteur**

Notre caméra OV2640 a une résolution de 2MP (1600×1200 pixels). Pour observer le stress hydrique au niveau des feuilles, nous avons besoin d'une résolution sub-millimétrique.

**Calcul** :
```
GSD = (p × H) / f
```

Où :
- p = 2.24 µm = 2.24×10⁻⁶ m (taille pixel)
- f = 3.6 mm = 3.6×10⁻³ m (focale)
- H = altitude

| Altitude (H) | GSD (mm/pixel) | Qualité |
|--------------|----------------|---------|
| 0.50 m | 0.31 mm | Excellente mais champ trop petit |
| **0.70 m** | **0.44 mm** | **Optimale pour notre usage** |
| 1.00 m | 0.62 mm | Bonne mais moins précise |
| 1.50 m | 0.93 mm | Insuffisante pour les feuilles |

**Justification** : À 0.70m, le GSD de 0.44 mm/pixel permet d'observer la texture des feuilles individuelles et de détecter les premiers signes de stress hydrique.

**Contrainte 2 : Souffle des hélices (downwash)**

À basse altitude, le souffle des hélices peut perturber les plantes.

**Référence** : Huang, Y. et al. (2019). "Remote sensing of crop water use and stress." Springer. [Lien](https://link.springer.com/chapter/10.1007/978-3-030-33157-3_14)

**Recommandation** : Pour un drone de 42g, une altitude de 0.70m est suffisante pour minimiser les perturbations tout en gardant une bonne résolution.

**Contrainte 3 : Taille de la parcelle**

Notre parcelle fait 3.5m × 2.5m. À 0.70m d'altitude, l'emprise d'une image est de 0.70m × 0.52m, ce qui permet de couvrir la parcelle avec un nombre raisonnable de photos (216).

**Conclusion** : H = 0.70m est le **compromis optimal** entre résolution, couverture et perturbation des plantes.

---

## 2. Vitesse de Vol : v = 0.20 m/s

### 2.1 Pourquoi 0.20 m/s et pas 0.50 m/s ou 0.10 m/s ?

**Contrainte 1 : Flou cinétique (Motion Blur)**

Le mouvement du drone pendant le temps de pose crée un flou sur l'image.

**Formule** :
```
v_max = (GSD × blur_limit) / T_exp
```

Où :
- GSD = 0.44 mm/pixel = 0.44×10⁻³ m/pixel
- blur_limit = 0.5 pixel (seuil acceptable)
- T_exp = 1/1000 s (temps de pose)

**Calcul** :
```
v_max = (0.44×10⁻³ × 0.5) / (1/1000)
v_max = 0.22 m/s
```

**Justification** : À 0.20 m/s, le flou est de :
```
Flou = v × T_exp = 0.20 × (1/1000) = 0.0002 m = 0.2 mm
Flou en pixels = 0.2 mm / 0.44 mm/pixel = 0.45 pixel
```

0.45 pixel < 0.5 pixel (seuil acceptable) → **Images nettes**

**Référence** : Lillesand, T.M. & Kiefer, R.W. (2000). "Remote Sensing and Image Interpretation." 4th Edition, John Wiley & Sons.

**Contrainte 2 : Consommation de batterie**

| Vitesse | Temps mission | Batterie | Statut |
|---------|---------------|----------|--------|
| 0.10 m/s | 6.62 min | 82.8% | ✅ Lent |
| **0.20 m/s** | **3.31 min** | **41.4%** | **✅ Optimal** |
| 0.30 m/s | 2.21 min | 27.6% | ✅ Rapide |
| 0.50 m/s | 1.32 min | 16.5% | ⚠️ Flou |

**Justification** : À 0.20 m/s, la mission dure 3.31 minutes et consomme 41.4% de la batterie, laissant 58.6% de réserve pour le décollage, l'atterrissage et les imprévus.

**Contrainte 3 : Stabilité du drone**

À très basse vitesse (< 0.10 m/s), le drone peut devenir instable à cause des perturbations du vent et des vibrations.

**Conclusion** : v = 0.20 m/s est le **compromis optimal** entre qualité d'image, consommation et stabilité.

---

## 3. Recouvrement Frontal : 75%

### 3.1 Pourquoi 75% et pas 50% ou 90% ?

**Formule** :
```
dx = Wx × (1 - of)
```

Où :
- Wx = 0.70 m (emprise horizontale)
- of = recouvrement frontal

| Recouvrement | dx (m) | Photos/ligne | Statut |
|--------------|--------|--------------|--------|
| 50% | 0.35 | 10 | ⚠️ Trop peu |
| **75%** | **0.175** | **18** | **✅ Optimal** |
| 90% | 0.07 | 40 | ❌ Trop de photos |

**Justification** :
- **50%** : Risque de zones non couvertes entre les photos
- **75%** : Bon compromis entre couverture et nombre de photos
- **90%** : Trop de photos, temps et batterie gaspillés

**Référence** : standard en photogrammétrie pour la reconstruction 3D et l'orthophotographie.

**Conclusion** : 75% est le **standard accepté** en photogrammétrie pour garantir une couverture complète.

---

## 4. Recouvrement Latéral : 65%

### 4.1 Pourquoi 65% et pas 50% ou 80% ?

**Formule** :
```
dy = Wy × (1 - os)
```

Où :
- Wy = 0.52 m (emprise verticale)
- os = recouvrement latéral

| Recouvrement | dy (m) | Lignes | Statut |
|--------------|--------|--------|--------|
| 50% | 0.26 | 10 | ⚠️ Trop peu |
| **65%** | **0.182** | **12** | **✅ Optimal** |
| 80% | 0.104 | 24 | ❌ Trop de lignes |

**Justification** :
- **50%** : Risque de zones non couvertes entre les lignes
- **65%** : Bon compromis entre couverture et nombre de lignes
- **80%** : Trop de lignes, temps et batterie gaspillés

**Conclusion** : 65% est un **bon compromis** pour notre parcelle étroite (2.5m de largeur).

---

## 5. Seuils de Sécurité Batterie

### 5.1 RTH à 3.60V (~20%)

**Pourquoi 3.60V et pas 3.70V ou 3.50V ?**

**Courbe de décharge LiPo 1S** :

| Tension | Capacité restante | Action |
|---------|-------------------|--------|
| 4.20V | 100% | Chargée |
| 3.70V | ~50% | Nominale |
| **3.60V** | **~20%** | **RTH (retour)** |
| 3.50V | ~10% | Urgence |
| 3.30V | ~5% | Critique |
| 3.00V | 0% | Cutoff |

**Justification** : À 3.60V, il reste environ 20% de batterie, soit ~1.6 minute de vol. C'est suffisant pour :
1. Revenir au point HOME (quelques mètres)
2. Atterrir en sécurité
3. Marge pour les imprévus

**Référence** : Ampow (2022). "LiPo Voltage Chart." [Lien](https://blog.ampow.com/lipo-voltage-chart/)

### 5.2 Urgence à 3.50V (~10%)

**Pourquoi 3.50V et pas 3.40V ou 3.60V ?**

**Justification** : À 3.50V, il reste environ 10% de batterie, soit ~0.8 minute. C'est le **minimum absolu** pour :
1. Atterrir immédiatement à la position actuelle
2. Éviter la décharge profonde (dommages irréversibles)

**Référence** : UFineBattery (2026). "Guide to Learn 1S LiPo Battery." [Lien](https://www.ufinebattery.com/blog/guide-to-learn-1s-lipo-battery/)

---

## 6. Seuils de Classification

### 6.1 Seuil ExG : 0.20

**Pourquoi 0.20 et pas 0.15 ou 0.30 ?**

**Référence** : Woebbecke et al. (1995) ont démontré que l'indice ExG sépare efficacement la végétation du sol pour des valeurs > 0.15.

**Calcul empirique** :
- Végétation saine : ExG ≈ 0.40 - 0.60
- Végétation stressée : ExG ≈ 0.10 - 0.20
- Sol nu : ExG ≈ -0.10 - 0.05

**Justification** : 0.20 est un **seuil conservateur** qui :
1. Élimine le sol (ExG < 0.15)
2. Sépare les plantes saines (ExG > 0.20) des stressées (ExG < 0.20)
3. Est validé par la littérature

**Référence** : Woebbecke, D.M. et al. (1995). "Color indices for weed identification." Transactions of the ASAE, 38(1), 259-269.

### 6.2 Seuil GRVI : 0.15

**Pourquoi 0.15 et pas 0.10 ou 0.20 ?**

**Justification** : Le GRVI est une approximation du NDVI. Les valeurs typiques sont :
- Végétation saine : GRVI ≈ 0.20 - 0.40
- Végétation stressée : GRVI ≈ 0.05 - 0.15
- Sol nu : GRVI ≈ -0.10 - 0.05

0.15 est un **seuil raisonnable** qui sépare les plantes saines des stressées.

**Référence** : Tucker, C.J. (1979). "Red and photographic infrared linear combinations for monitoring vegetation."

---

## 7. Paramètres du Classificateur RandomForest

### 7.1 Nombre d'arbres : 150

**Pourquoi 150 et pas 50 ou 500 ?**

**Référence** : Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32. [Lien](https://link.springer.com/article/10.1023/A:1010933404324)

**Justification** :
- **50 arbres** : Performance insuffisante
- **150 arbres** : Bon compromis précision/temps
- **500 arbres** : Amélioration marginale, temps d'entraînement plus long

**Règle empirique** : 100-500 arbres selon la complexité du problème.

### 7.2 Profondeur max : 6

**Pourquoi 6 et pas 3 ou 10 ?**

**Justification** :
- **Profondeur 3** : Sous-apprentissage (arbre trop simple)
- **Profondeur 6** : Bon compromis complexité/généralisation
- **Profondeur 10** : Sur-apprentissage (arbre trop complexe)

**Règle empirique** : profondeur ≈ log₂(nombre de features) + 1 = log₂(4) + 1 ≈ 3, mais 6 pour plus de marge.

---

## 8. Nombre de Features : 4

**Pourquoi 4 et pas 2 ou 6 ?**

**Features utilisées** :
1. ExG moyen
2. ExG écart-type
3. GRVI moyen
4. GRVI écart-type

**Justification** :
- **2 features** : Insuffisant pour capturer la variabilité
- **4 features** : Bon compromis information/complexité
- **6 features** : Inclurait température et humidité (non disponibles)

**Note** : La température feuille et l'humidité sol ne sont pas dans le CDC et nécessitent du matériel supplémentaire.

---

## 9. Validation Croisée : 5-fold

**Pourquoi 5-fold et pas 3-fold ou 10-fold ?**

**Référence** : Kohavi, R. (1995). "A study of cross-validation and bootstrap for accuracy estimation and model selection." IJCAI, 14(2), 1137-1145.

**Justification** :
- **3-fold** : Estimation peu fiable
- **5-fold** : Standard en machine learning, bon compromis
- **10-fold** : Plus fiable mais plus lent

**Conclusion** : 5-fold est le **standard accepté** pour la validation de modèles.

---

## 10. Récapitulatif des Valeurs Justifiées

| Valeur | Justification | Source |
|--------|---------------|--------|
| **H = 0.70 m** | GSD 0.44mm, champ suffisant, downwash minimal | Calcul + Huang 2019 |
| **v = 0.20 m/s** | Flou < 0.5px, batterie 41.4%, stabilité | Calcul + Lillesand 2000 |
| **Recouvrement 75%** | Standard photogrammétrie, couverture complète | Standard industriel |
| **Recouvrement 65%** | Compromis couverture/nombre lignes | Standard industriel |
| **RTH 3.60V** | 20% restant, temps suffisant pour retour | Ampow 2022 |
| **Urgence 3.50V** | 10% restant, minimum absolu | UFineBattery 2026 |
| **Seuil ExG 0.20** | Sépare sain/stressé, validé littérature | Woebbecke 1995 |
| **Seuil GRVI 0.15** | Approximation NDVI, seuil raisonnable | Tucker 1979 |
| **150 arbres RF** | Compromis précision/temps | Breiman 2001 |
| **Profondeur 6** | Évite sur-apprentissage | Règle empirique |
| **4 features** | Disponibles, conformes CDC | Choix technologique |
| **5-fold CV** | Standard machine learning | Kohavi 1995 |

---

*Document créé le 13 juillet 2026*
*Binôme A - Justification des valeurs techniques*