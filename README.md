# Drone autonome pour la détection du stress hydrique

Projet de licence L3 EIT, ESP Antsiranana, mai à août 2026.
Binôme A : FANOGNY Hernandez Liwingston et RAKOTONIRINA Ny Antso Fyh Arihvony.

Objectif : développer un drone autonome capable d'acquérir des images aériennes
géolocalisées au-dessus d'une parcelle de 24 plants de tomates (1,0 m x 2,0 m)
et de cartographier le stress hydrique à partir des indices de végétation.

## Documents de pilotage

- Audit des failles et corrections : [docs/AUDIT_FALLES_2026-08-06.md](docs/AUDIT_FALLES_2026-08-06.md)
- Note technique de navigation (présentation aux encadrants) : [docs/NOTE_NAVIGATION_IMU_ARUCO.md](docs/NOTE_NAVIGATION_IMU_ARUCO.md)
- Calendrier de remise au 23 août : [docs/PLAN_REMISE_23_AOUT.md](docs/PLAN_REMISE_23_AOUT.md)

## Matériel

| Composant | Spécifications | Rôle |
|-----------|----------------|------|
| PyDrone 01Studio | ESP32-S3-WROOM-1 N8R8, 42 g, 130 x 130 mm | Plateforme de vol |
| Caméra OV2640 | 2 MP (1600 x 1200), FOV 66°, sans filtre IR | Imagerie 650 + 850 nm |
| GPS BN-220 | Ublox M8030-KT, précision ~2 m | Référence HOME uniquement |
| MPU6050 + SPL06 | IMU 6 axes + baromètre | Stabilisation et altitude |
| Batterie LiPo 1S | 400 mAh | Autonomie ~8 min ; RTH à 3,65 V |

## Paramètres optiques et de vol validés

- Altitude 0,70 m : GSD = 0,44 mm/pixel, emprise au sol 0,70 m x 0,52 m.
- Vitesse 0,20 m/s : flou de mouvement 0,45 pixel (inférieur au seuil de 0,5).
- Indices : ExG = 2G - R - B (Woebbecke 1995) ; GRVI = (R - G)/(R + G).
  Convention unique, celle du code embarqué : la végétation saine a un GRVI négatif.
- Trajectoire de couverture : lawnmower (boustrophédon) pré-calculée.

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Structure du dépôt

```
imagerie/
  camera_model.py             modélisation optique OV2640 (GSD, emprise)
  stress_detector.py          indices ExG et GRVI, classification binaire
  train_classifier.py         entraînement RandomForest (ancienne version, voir audit P0.1)
  validation_reelle.py        pipeline corrigé : features extraites des images,
                              Leave-One-Group-Out par plante, F1 poolé, Kappa, MCC,
                              bootstrap groupé, comparaison à la baseline par seuils
simulation/
  lawnmower_planner.py        génération de la trajectoire de couverture
  trajectory_optimizer.py     optimisation multi-critères
  flight_simulator.py         simulation cinématique
mission/                      code MicroPython embarqué (en cours de réintégration)
web/                          station sol : serveur et interface cartographique (en cours)
data/dataset/
  healthy/  stressed/         images (25 + 25 synthétiques actuellement,
                              remplacement par données réelles en cours)
  plants_mapping.csv          mapping image -> pot (obligatoire pour la validation par plante)
  metadata.json               régénéré par scripts/consolidate_dataset_metadata.py
models/                       modèles entraînés et résultats JSON de validation
reports/                      rapports hebdomadaires et figures
docs/                         audit, notes techniques, références
scripts/                      collecte d'images et utilitaires de données
```

## Procédure de validation du classifieur (version corrigée)

```bash
# 1. Après chaque collecte : régénérer les métadonnées depuis le disque
python scripts/consolidate_dataset_metadata.py

# 2. Validation statistique sur les images, split par plante
python imagerie/validation_reelle.py
#    sortie : models/validation_reelle_results.json
#    (F1 poolé, Kappa, MCC, intervalles bootstrap à 95 %, verdict vs critère F1 > 0,70)
```

Règles associées : split obligatoire par plante (jamais par image) ; le fichier
`data/dataset/plants_mapping.csv` (colonnes `image,plante`) fait foi pour le
groupage ; tout résultat obtenu sur les images synthétiques est un test de
fonctionnement du pipeline et ne constitue pas une mesure de performance.
