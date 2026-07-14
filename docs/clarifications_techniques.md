# Clarifications Techniques
## Binôme A — Points à approfondir

---

## 1. RandomForest (150 arbres, profondeur max 6)

### 1.1 Qu'est-ce que le RandomForest ?

Le **RandomForest** (Forêt Aléatoire) est un algorithme de **machine learning** utilisé pour la classification et la régression. Il combine plusieurs **arbres de décision** pour obtenir une prédiction plus robuste.

**Référence** : Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.

### 1.2 Comment ça fonctionne ?

```
Image d'entrée
      ↓
┌─────────────┐
│ Arbre 1     │ → Prédiction 1
├─────────────┤
│ Arbre 2     │ → Prédiction 2
├─────────────┤
│ Arbre 3     │ → Prédiction 3
├─────────────┤
│    ...      │ → ...
├─────────────┤
│ Arbre 150   │ → Prédiction 150
└─────────────┘
      ↓
  Vote majoritaire
      ↓
  Classe finale (Sain/Stressé)
```

### 1.3 Pourquoi 150 arbres ?

| Nombre d'arbres | Performance | Temps d'entraînement | Choix |
|-----------------|-------------|---------------------|-------|
| 10 | Faible | Très rapide | ❌ |
| 50 | Moyenne | Rapide | ❌ |
| **150** | **Bonne** | **Modéré** | ✅ |
| 500 | Excellente | Lent | ❌ |

**Justification** :
- **150 arbres** offre un bon compromis entre **précision** et **temps de calcul**
- Au-delà de 150, l'amélioration est marginale
- **Source** : Breiman (2001) recommande 100-500 arbres selon la complexité

### 1.4 Pourquoi profondeur max 6 ?

La **profondeur** d'un arbre détermine sa complexité :

| Profondeur | Complexité | Risque de surapprentissage | Choix |
|------------|------------|---------------------------|-------|
| 2 | Très faible | Très faible | ❌ (sous-apprentissage) |
| 4 | Faible | Faible | ❌ |
| **6** | **Modérée** | **Modéré** | ✅ |
| 10 | Élevée | Élevé | ❌ (surapprentissage) |
| Illimitée | Maximale | Maximal | ❌ |

**Justification** :
- **Profondeur 6** = arbre suffisamment complexe pour capturer les patterns
- **Profondeur 6** = pas trop complexe pour éviter le surapprentissage
- **Source** : Règle empirique : profondeur = log2(nombre de features) + 1 = log2(4) + 1 ≈ 3, mais on prend 6 pour plus de marge

### 1.5 Visualisation

```
Arbre de décision (profondeur 3) :

                    [ExG > 0.20 ?]
                    /              \
                Oui                Non
                /                    \
        [GRVI > 0.15 ?]        [ExG_std > 0.05 ?]
        /            \          /              \
      Oui           Non       Oui             Non
      /               \        /                \
   SAIN          STRESSÉ   SAIN             STRESSÉ
```

---

## 2. 5-fold Cross-Validation Stratifiée

### 2.1 Qu'est-ce que la cross-validation ?

La **cross-validation** (validation croisée) est une méthode pour **évaluer la performance** d'un modèle de machine learning de manière **robuste**.

**Référence** : Kohavi, R. (1995). "A study of cross-validation and bootstrap for accuracy estimation and model selection." IJCAI, 14(2), 1137-1145.

### 2.2 Comment fonctionne le 5-fold ?

```
Dataset complet (120 images)
      ↓
┌─────────────────────────────────────┐
│ Fold 1 │ Fold 2 │ Fold 3 │ Fold 4 │ Fold 5 │
│  24    │  24    │  24    │  24    │  24    │
└─────────────────────────────────────┘

Itération 1 : [TEST] [Train] [Train] [Train] [Train] → Précision 1
Itération 2 : [Train] [TEST] [Train] [Train] [Train] → Précision 2
Itération 3 : [Train] [Train] [TEST] [Train] [Train] → Précision 3
Itération 4 : [Train] [Train] [Train] [TEST] [Train] → Précision 4
Itération 5 : [Train] [Train] [Train] [Train] [TEST] → Précision 5

Précision finale = Moyenne(Précision 1, 2, 3, 4, 5)
```

### 2.3 Pourquoi 5 folds ?

| Nombre de folds | Avantages | Inconvénients | Choix |
|-----------------|-----------|---------------|-------|
| 2 | Rapide | Estimation peu fiable | ❌ |
| 3 | Rapide | Estimation moyenne | ❌ |
| **5** | **Bon compromis** | **Modéré** | ✅ |
| 10 | Très fiable | Lent | ❌ |
| Leave-one-out | Maximal | Très lent | ❌ |

**Justification** :
- **5 folds** = standard en machine learning
- **5 folds** = bon compromis entre fiabilité et temps de calcul
- **Source** : Kohavi (1995) recommande 5 ou 10 folds

### 2.4 Pourquoi "stratifiée" ?

La **stratification** garantit que chaque fold contient la **même proportion** de chaque classe :

```
Dataset : 60 sains + 60 stressés = 120 images

Fold 1 : 12 sains + 12 stressés = 24 images
Fold 2 : 12 sains + 12 stressés = 24 images
Fold 3 : 12 sains + 12 stressés = 24 images
Fold 4 : 12 sains + 12 stressés = 24 images
Fold 5 : 12 sains + 12 stressés = 24 images
```

**Justification** :
- **Stratification** = évite le biais si les classes sont déséquilibrées
- **Stratification** = garantit que chaque fold est représentatif
- **Source** : Pratique standard en classification binaire

### 2.5 Résultat attendu

```
Fold 1 : Précision = 95%
Fold 2 : Précision = 92%
Fold 3 : Précision = 97%
Fold 4 : Précision = 94%
Fold 5 : Précision = 96%

Précision finale = (95 + 92 + 97 + 94 + 96) / 5 = 94.8%
Écart-type = 1.8%

Rapport : "Précision : 94.8% ± 1.8%"
```

---

## 3. Batterie LiPo 1S : Chargée 4.20V, 100%

### 3.1 Qu'est-ce qu'une batterie LiPo 1S ?

**LiPo** = Lithium Polymer
**1S** = 1 cellule en série

| Paramètre | Valeur | Signification |
|-----------|--------|---------------|
| **Tension nominale** | 3.7V | Tension de fonctionnement |
| **Tension chargée** | 4.20V | Tension maximale |
| **Tension déchargée** | 3.00V | Tension minimale (cutoff) |
| **Capacité** | 400 mAh | Autonomie |

**Source** : UFineBattery (2026), WhaleBattery (2026)

### 3.2 Pourquoi 4.20V = 100% ?

La tension d'une batterie LiPo varie avec sa charge :

| État | Tension | Pourcentage | Action |
|------|---------|-------------|--------|
| **Chargée** | 4.20V | 100% | Prête à l'emploi |
| **Plateau** | 3.70V | ~50% | Zone de fonctionnement |
| **RTH** | 3.60V | ~20% | Return-To-Home |
| **Urgence** | 3.50V | ~10% | Atterrissage d'urgence |
| **Critique** | 3.30V | ~5% | Zone de danger |
| **Cutoff** | 3.00V | 0% | Arrêt immédiat |

**Source** : Ampow LiPo Voltage Chart (2022)

### 3.3 Pourquoi pas 5V ou 3.7V ?

| Tension | État | Risque |
|---------|------|--------|
| **5.0V** | Surchargée | ⚠️ DANGER : surchauffe, gonflement, explosion |
| **4.20V** | Chargée | ✅ Optimal |
| **3.70V** | Nominale | ✅ Fonctionnement normal |
| **3.00V** | Déchargée | ⚠️ Dommage permanent si < 3.0V |

**Source** : UFineBattery (2026)
> "When the battery voltage drops to 3.0V, it's considered fully discharged. Draining the battery below this level can cause irreversible damage."

### 3.4 Courbe de décharge typique

```
Tension (V)
    │
4.2 │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% (Chargée)
    │
3.7 │────────────────────────────────────────────── 50% (Nominale)
    │                    ╲
3.6 │─ ─ ─ ─ ─ ─ ─ ─ ─ ─╲─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ 20% (RTH)
    │                      ╲
3.5 │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─╲─ ─ ─ ─ ─ ─ ─ ─ ─ ─ 10% (Urgence)
    │                        ╲
3.3 │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─╲─ ─ ─ ─ ─ ─ ─ ─ ─ 5% (Critique)
    │                          ╲
3.0 │━━━━━━━━━━━━━━━━━━━━━━━━━━━╲━━━━━━━━━━━━━━━━ 0% (Cutoff)
    │                             ╲
    └────────────────────────────────────────────── Temps
         Début      Plateau      "Knee"        Fin
```

**Observations** :
1. **Chute initiale** : La tension baisse légèrement au début (normal sous charge)
2. **Plateau** : Zone principale de fonctionnement (3.7V - 3.3V)
3. **"Knee"** : Chute rapide après 3.3V = zone de danger
4. **Cutoff** : Arrêt à 3.0V pour éviter les dommages

### 3.5 Nos seuils de sécurité

| Seuil | Tension | % restant | Justification |
|-------|---------|-----------|---------------|
| **RTH** | 3.60V | ~20% | Temps suffisant pour retourner au point HOME |
| **Urgence** | 3.50V | ~10% | Atterrissage immédiat à la position actuelle |

**Validation encadrants** : "Ces valeurs paraissent cohérentes pour une batterie LiPo 1S et peuvent être retenues pour les premiers essais."

---

## 4. Résumé des Clarifications

| Point | Clarification |
|-------|---------------|
| **RandomForest 150 arbres** | Bon compromis précision/temps, 150 arbres votent pour la classe finale |
| **Profondeur max 6** | Évite le surapprentissage tout en capturant les patterns |
| **5-fold stratifiée** | Chaque fold contient la même proportion de sains/stressés |
| **Batterie 4.20V = 100%** | Tension maximale de sécurité pour LiPo 1S |

---

## 5. Sources

1. **Breiman, L.** (2001). "Random Forests." Machine Learning, 45(1), 5-32.
2. **Kohavi, R.** (1995). "A study of cross-validation and bootstrap for accuracy estimation and model selection." IJCAI, 14(2), 1137-1145.
3. **UFineBattery** (2026). "Guide to Learn 1S LiPo Battery."
4. **WhaleBattery** (2026). "LiPo Battery Voltage Explained."
5. **Ampow** (2022). "LiPo Voltage Chart."

---

*Document créé le 10 juillet 2026*
*Binôme A — Clarifications techniques*