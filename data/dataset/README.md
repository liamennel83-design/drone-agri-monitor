# Dataset — Images de Tomates

Ce dossier contient les images annotées pour l'entraînement du classificateur.

## Structure

```
dataset/
├── healthy/          # Images de tomates saines
│   ├── sain_001.jpg
│   ├── sain_002.jpg
│   └── ...
├── stressed/         # Images de tomates stressées
│   ├── stresse_001.jpg
│   ├── stresse_002.jpg
│   └── ...
└── metadata.json     # Métadonnées du dataset
```

## Annotations

| Catégorie | Description | Critères |
|-----------|-------------|----------|
| **healthy** | Tomate saine | Feuilles vertes, pas de flétrissement |
| **stressed** | Tomate stressée | Jaunissement, flétrissement, chlorose |

## Métadonnées

Le fichier `metadata.json` contient :
- Date de création
- Nombre d'images par catégorie
- Sources des images
- Méthode d'annotation

---

*Dataset créé le 10 juillet 2026*
*Binôme A — Projet Robot Aérien Autonome*