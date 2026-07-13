# Module Imagerie — Traitement d'Images

Ce dossier contient les modules de traitement d'images pour la détection du stress hydrique.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `camera_model.py` | Modélisation optique de la caméra OV2640 |
| `stress_detector.py` | Calcul des indices de végétation et classification |
| `train_classifier.py` | Entraînement du classificateur RandomForest |

## Indices de végétation

### ExG (Excess Green)
```
ExG = 2×G - R - B
```
- Référence : Woebbecke et al. (1995)
- Usage : Indice principal pour la détection de végétation

### GRVI (Green-Red Vegetation Index)
```
GRVI = (R - G) / (R + G)
```
- Référence : Tucker et al. (1979)
- Usage : Approximation NDVI sur caméra NIR-modified

## Classification

- **Algorithme** : RandomForest (150 arbres, profondeur max 6)
- **Features** : 4 (ExG moyen, ExG écart-type, GRVI moyen, GRVI écart-type)
- **Validation** : 5-fold cross-validation
- **Export** : Modèle .pkl + métadonnées JSON

---

*Module créé le 10 juillet 2026*
*Binôme A — Projet Robot Aérien Autonome*