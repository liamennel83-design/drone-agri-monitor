# Résultats — Sorties du Projet

Ce dossier contient les résultats générés par les scripts.

## Structure

```
resultats/
├── images/           # Images traitées
├── cartes/           # Cartes NDVI et d'alerte
├── modeles/          # Modèles entraînés (.pkl)
├── rapports/         # Rapports de classification
└── figures/          # Graphiques et visualisations
```

## Types de résultats

### Images traitées
- Images prétraitées (correction d'exposition, recadrage)
- Cartes d'indices (ExG, GRVI)
- Masques de classification

### Cartes
- Carte NDVI spatiale
- Carte d'alerte sécheresse (vert/rouge)
- Carte de confiance

### Modèles
- Modèle RandomForest entraîné (.pkl)
- Métadonnées du modèle (.json)
- Métriques de performance

### Rapports
- Rapport de classification par image
- Statistiques globales
- Matrice de confusion

---

*Résultats créés le 10 juillet 2026*
*Binôme A — Projet Robot Aérien Autonome*