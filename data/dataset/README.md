# Base d'images annotées

## Contenu actuel

Le dépôt contient actuellement 50 images de démonstration : 25 dans `healthy/` et 25 dans `stressed/`. Elles sont indiquées comme synthétiques dans les métadonnées. Elles servent à vérifier la chaîne de traitement, mais ne constituent pas une validation agronomique du modèle.

## Convention pour les acquisitions réelles

Nommer chaque image selon le format suivant :

```text
P01_J00_V1.jpg
P01_J00_V2.jpg
P13_J07_V1.jpg
```

- `P01` : identifiant stable du pot, de `P01` à `P24`.
- `J00` : jour depuis le début du protocole de stress.
- `V1` : vue ou répétition de prise de vue.

Ranger l'image selon son annotation au moment de l'acquisition :

```text
healthy/P01_J00_V1.jpg
stressed/P13_J07_V1.jpg
```

## Fichier d'annotation

Le fichier `plants_mapping.csv` est obligatoire pour une validation rigoureuse. Une ligne représente une image.

| Colonne | Description |
| --- | --- |
| `image` | Nom exact du fichier image |
| `plant_id` | Identifiant du pot, par exemple `P01` |
| `label` | `healthy` ou `stressed` |
| `jour` | Jour du protocole, par exemple `J07` |
| `humidite_sol_pct` | Valeur mesurée par le capteur après étalonnage |
| `date_heure` | Date et heure de prise de vue au format ISO |
| `notes` | Lumière, hauteur, incident ou observation visuelle |

Le découpage apprentissage et test doit séparer les plants, pas seulement les images. Toutes les vues d'un même pot doivent donc utiliser le même `plant_id`.

## Métadonnées

Générer les compteurs après chaque ajout d'images :

```bash
python scripts/consolidate_dataset_metadata.py
```

Cette commande met à jour `metadata.json` à partir du contenu réel des dossiers.
