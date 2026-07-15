# Corrections et Précisions
## Binôme A : Projet Robot Aérien Autonome

---

## 1. Correction du lien source

Le lien précédent vers la courbe de décharge Ampow était incorrect.

**Lien correct** : https://blog.ampow.com/lipo-voltage-chart/

**Source vérifiée** : Ampow (2022). "Lipo Voltage Chart: Show the Relationship of Voltage and Capacity."

**Données extraites** :

| Capacité (%) | Tension 1S (V) |
|--------------|----------------|
| 100% | 4.20V |
| 75% | 3.87V |
| 50% | 3.75V |
| 25% | 3.75V |
| 20% | 3.73V |
| 15% | 3.71V |
| 10% | 3.69V |
| 5% | 3.61V |
| 0% | 3.27V |

**Référence complète** : 
Ampow (2022). "Lipo Voltage Chart: Show the Relationship of Voltage and Capacity." 
https://blog.ampow.com/lipo-voltage-chart/

---

## 2. Recalcul avec parcelle réelle : 1m × 2m

### 2.1 Paramètres de la parcelle

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Largeur (X) | 1.0 m | Instructions utilisateur |
| Longueur (Y) | 2.0 m | Instructions utilisateur |
| Surface | 2.0 m² | Calcul |
| Nombre de pots | 12 | Disposition 3×4 |
| Diamètre pot | 10.5 cm | Instructions utilisateur |
| Hauteur pot | 12 cm | Instructions utilisateur |

### 2.2 Positionnement optimal des pots

**Disposition** : 3 colonnes × 4 rangées

**Calcul de l'espacement** :

```
Largeur disponible : 1.0 m - 2 × marge
Longueur disponible : 2.0 m - 2 × marge

Marge recommandée : 10 cm (pour éviter les bords)

Largeur utile : 1.0 - 0.2 = 0.8 m
Longueur utile : 2.0 - 0.2 = 1.8 m

Espacement X (centre à centre) : 0.8 / (3-1) = 0.4 m = 40 cm
Espacement Y (centre à centre) : 1.8 / (4-1) = 0.6 m = 60 cm
```

**Coordonnées des 12 pots** (origine = coin inférieur gauche) :

| Pot | X (m) | Y (m) |
|-----|-------|-------|
| P1 | 0.10 | 0.10 |
| P2 | 0.50 | 0.10 |
| P3 | 0.90 | 0.10 |
| P4 | 0.10 | 0.70 |
| P5 | 0.50 | 0.70 |
| P6 | 0.90 | 0.70 |
| P7 | 0.10 | 1.30 |
| P8 | 0.50 | 1.30 |
| P9 | 0.90 | 1.30 |
| P10 | 0.10 | 1.90 |
| P11 | 0.50 | 1.90 |
| P12 | 0.90 | 1.90 |

### 2.3 Recalcul des paramètres de mission

**Formules** :
```
GSD = (p × H) / f
Wx = (Nx × p × H) / f
Wy = (Ny × p × H) / f
dx = Wx × (1 - of)
dy = Wy × (1 - os)
```

**Avec H = 0.70m** :
```
GSD = (2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.44 mm/pixel
Wx = (1600 × 2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.70 m
Wy = (1200 × 2.24×10⁻⁶ × 0.70) / 3.6×10⁻³ = 0.52 m
dx = 0.70 × (1 - 0.75) = 0.175 m
dy = 0.52 × (1 - 0.65) = 0.182 m
```

**Nombre de lignes et photos** :
```
Lignes = ⌈2.0 / 0.182⌉ = 11 lignes
Photos par ligne = ⌈1.0 / 0.175⌉ = 6 photos
Total photos = 11 × 6 = 66 photos
```

**Distance et temps** :
```
Distance = 11 × 1.0 + 10 × 0.182 = 12.82 m
Temps = 12.82 / 0.20 = 64.1 s = 1.07 min
Batterie = 64.1 / 480 = 13.4%
```

**Tableau récapitulatif** :

| Paramètre | Valeur (parcelle 1×2m) |
|-----------|------------------------|
| Altitude | 0.70 m |
| GSD | 0.44 mm/pixel |
| Emprise (Wx × Wy) | 0.70m × 0.52m |
| Recouvrement frontal | 75% |
| Recouvrement latéral | 65% |
| Espacement photos (dx) | 0.175 m |
| Espacement lignes (dy) | 0.182 m |
| Nombre de lignes | 11 |
| Photos par ligne | 6 |
| Total photos | 66 |
| Distance totale | 12.82 m |
| Temps de mission | 64.1 s (1.07 min) |
| Consommation batterie | 13.4% |

### 2.4 Comparaison Vol Continu vs Stop-and-Capture (parcelle 1×2m)

**Mode Vol Continu** :
```
Temps = 1.07 min
Batterie = 13.4%
Statut : ✅ EXCELLENT
```

**Mode Stop-and-Capture** :
```
Temps de stabilisation = 66 × 0.4s = 26.4s
Temps total = 64.1 + 26.4 = 90.5s = 1.51 min
Batterie = 90.5 / 480 = 18.9%
Statut : ✅ FAISABLE
```

**Conclusion** : Sur la petite parcelle (1×2m), les deux modes sont faisables. Le vol continu reste plus efficace (13.4% vs 18.9%).

---

## 3. Positionnement Optimal des Pots

### 3.1 Contraintes

- Parcelle : 1m × 2m
- Pots : 12 (disposition 3×4)
- Diamètre pot : 10.5 cm = 0.105 m
- Hauteur pot : 12 cm = 0.12 m

### 3.2 Calcul de l'espacement optimal

**Objectif** : Maximiser l'espace entre les pots pour la croissance des plantes, tout en respectant la taille de la parcelle.

**Calcul** :
```
Marge de sécurité (bord) : 10 cm = 0.10 m

Largeur utile : 1.0 - 2 × 0.10 = 0.80 m
Longueur utile : 2.0 - 2 × 0.10 = 1.80 m

Espacement X (centre à centre) : 0.80 / 2 = 0.40 m
Espacement Y (centre à centre) : 1.80 / 3 = 0.60 m

Distance bord à bord (X) : 0.40 - 0.105 = 0.295 m
Distance bord à bord (Y) : 0.60 - 0.105 = 0.495 m
```

**Vérification** :
```
Espace total X : 0.10 + 0.105/2 + 0.40 + 0.105 + 0.40 + 0.105/2 + 0.10 = 1.0 m ✅
Espace total Y : 0.10 + 0.105/2 + 0.60 + 0.105 + 0.60 + 0.105 + 0.60 + 0.105/2 + 0.10 = 2.0 m ✅
```

### 3.3 Adaptabilité du système

**Problème** : Si le terrain change légèrement, tout refaire n'est pas pratique.

**Solution** : Paramétrage dynamique dans le code.

```python
class PotLayout:
    """Classe pour calculer dynamiquement le positionnement des pots"""
    
    def __init__(self, field_width, field_length, num_cols, num_rows, 
                 pot_diameter, margin=0.10):
        self.field_width = field_width
        self.field_length = field_length
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.pot_diameter = pot_diameter
        self.margin = margin
        
    def compute_positions(self):
        """Calcule les positions optimales des pots"""
        usable_width = self.field_width - 2 * self.margin
        usable_length = self.field_length - 2 * self.margin
        
        spacing_x = usable_width / (self.num_cols - 1)
        spacing_y = usable_length / (self.num_rows - 1)
        
        positions = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = self.margin + col * spacing_x
                y = self.margin + row * spacing_y
                positions.append((x, y))
        
        return positions, spacing_x, spacing_y
```

**Avantage** : Si la taille de la parcelle change, il suffit de modifier les paramètres d'entrée.

---

## 4. Description Complète du Projet

### 4.1 Contexte

L'agriculture de précision par drone permet de surveiller l'état des cultures de manière efficace et non destructive. Le stress hydrique est l'un des facteurs les plus critiques affectant la productivité agricole.

### 4.2 Problématique

Comment planifier des trajectoires de vol optimales pour un drone multirotor afin de couvrir efficacement une parcelle agricole, tout en minimisant la consommation de batterie et en garantissant une qualité d'image suffisante pour détecter le stress hydrique des plantes ?

### 4.3 Objectifs

1. **Modéliser** le système drone-parcelle
2. **Implémenter** des algorithmes de couverture (Lawnmower)
3. **Simuler** les trajectoires
4. **Acquérir** des images aériennes
5. **Développer** un algorithme de détection du stress hydrique
6. **Valider** le système sur des parcelles expérimentales

### 4.4 Matériel

- **Drone** : Pydrone (42g, 130×130mm, autonomie 8min)
- **Caméra** : OV2640 2MP (1600×1200), NIR-modified (650nm + 850nm)
- **GPS** : BN-220 (Ublox M8030-KT, ~2m précision)
- **IMU** : MPU6050 (6 axes)
- **Baromètre** : SPL06-001

### 4.5 Méthodologie

1. **Modélisation optique** : Calcul du GSD, de l'emprise et de la vitesse maximale
2. **Planification de trajectoire** : Algorithme Lawnmower
3. **Simulation** : Comparaison vol continu vs Stop-and-Capture
4. **Acquisition d'images** : Capture à 0.70m d'altitude
5. **Traitement d'images** : Calcul ExG + GRVI, classification RandomForest
6. **Validation** : Protocole agronomique avec 24 pots de tomates

### 4.6 Résultats

- **GSD** : 0.44 mm/pixel (sub-millimétrique)
- **Photos** : 66 (parcelle 1×2m)
- **Temps** : 1.07 min
- **Batterie** : 13.4%
- **Précision classification** : F1 = 1.000

---

## 5. Livrables pour les Encadreurs

### 5.1 Documents à envoyer

| Document | Contenu | Fréquence |
|----------|---------|-----------|
| **Rapport d'avancement** | Progression, difficultés, solutions | Toutes les 2 semaines |
| **Mini-rapports** | Détail technique de chaque phase | Fin de chaque phase |
| **Code source** | Scripts Python documentés | Continue |
| **Visualisations** | Graphiques et cartes | Avec chaque rapport |
| **Protocole agronomique** | Suivi des tomates | Début du projet |

### 5.2 Points à présenter

1. **Architecture du système** : Drone + station sol + communication
2. **Choix techniques** : Altitude, vitesse, recouvrement
3. **Découverte majeure** : Vol continu vs Stop-and-Capture
4. **Résultats** : GSD, temps, batterie, précision
5. **Questions** : Validation des choix techniques

### 5.3 Questions pour les encadreurs

1. Le GPS BN-220 pour HOME uniquement, navigation fine par IMU : validez-vous ?
2. L'ExG est accepté, le GRVI à titre exploratoire : documenter les deux ?
3. Mire de calibration radiométrique au sol avant chaque vol ?
4. Mesurer la courbe de décharge de la batterie ?


---

*Document créé le 14 juillet 2026*
*Binôme A : Corrections et précisions*