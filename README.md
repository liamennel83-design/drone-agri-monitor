# Drone autonome pour le suivi du stress hydrique

Projet de Binôme A : prototype de drone Pydrone ESP32-S3 destiné à acquérir des images de plants de tomate et à étudier des indicateurs simples de stress hydrique.

## Objectif du projet

Le projet vise quatre résultats attendus :

1. Un modèle de trajectoire simulé et documenté.
2. Un prototype de vol basique et sûr.
3. Une base d'images annotées en deux classes : sain et stressé.
4. Un rapport présentant les résultats, les limites et les recommandations pour la poursuite en Master.

L'autonomie complète de navigation et la cartographie de stress sont des extensions étudiées dans le rapport. Elles ne doivent pas être confondues avec les résultats déjà validés.

## État des modules

| Module | Contenu disponible | État |
| --- | --- | --- |
| `simulation/` | Planification lawnmower, optimisation et simulateur de vol | Disponible |
| `imagerie/` | ExG, GRVI, extraction de quatre variables et entraînement exploratoire | Disponible, à valider sur images réelles |
| `data/dataset/` | 50 images synthétiques annotées et métadonnées | Démonstration uniquement |
| `mission/` | Documentation de l'interface embarquée attendue | Code de vol à intégrer |
| `web/` | Documentation de l'interface de supervision attendue | Interface à intégrer |
| `docs/` | Notes techniques, protocole expérimental et préparation du rapport | Disponible |

## Installation

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Linux ou macOS
source venv/bin/activate
pip install -r requirements.txt
```

## Vérifier les scripts

```bash
python simulation/lawnmower_planner.py
python imagerie/stress_detector.py
python scripts/consolidate_dataset_metadata.py --check
```

Lorsque les images réelles et le fichier `plants_mapping.csv` sont disponibles :

```bash
python imagerie/validation_reelle.py \
  --dataset data/dataset \
  --mapping data/dataset/plants_mapping.csv \
  --output models/validation_reelle_results.json
```

## Organisation des données

Les images futures doivent être rangées ainsi :

```text
data/dataset/
├── healthy/                 images étiquetées saines
├── stressed/                images étiquetées stressées
├── plants_mapping.csv       lien image, plant, classe et conditions d'acquisition
├── metadata.json            inventaire généré depuis les dossiers
└── README.md                convention de nommage et d'annotation
```

La structure et le protocole sont détaillés dans `data/dataset/README.md`.

## Documents utiles

- `docs/COUVERTURE_CDC.md` : correspondance entre le cahier des charges et les livrables.
- `docs/PLAN_REMISE_23_AOUT.md` : plan de travail jusqu'à la remise visée du 23 août.
- `docs/SECTION_RAPPORT_NAVIGATION_ARUCO.md` : section prête à adapter dans le prochain rapport.
- `docs/PROTOCOLE_HUMIDITE_SOL.md` : protocole de suivi avec capteurs d'humidité du sol.
- `docs/AUDIT_TECHNIQUE.md` : écarts identifiés et corrections prioritaires.

## Règles de dépôt

- Ne pas publier de mot de passe Wi-Fi, clé API ou identifiant de compte.
- Conserver les images réelles avec leur fichier d'annotation.
- Distinguer explicitement les résultats synthétiques des résultats expérimentaux.
- Documenter toute modification de seuil, altitude, vitesse ou protocole d'arrosage.
