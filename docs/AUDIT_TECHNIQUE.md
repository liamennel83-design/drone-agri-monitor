# Audit technique et corrections prioritaires

Date de mise à jour : 12 août 2026

Ce document distingue les éléments observables dans le dépôt des travaux restant à réaliser. Il doit servir de base de discussion avec les encadrants.

## Priorité 1 : rendre les données cohérentes

### Écart constaté

- `data/dataset/metadata.json` annonce 60 images, 30 saines et 30 stressées.
- Les dossiers contiennent 50 fichiers : 25 `healthy` et 25 `stressed`.
- Les noms documentés étaient `sain_` et `stresse_`, mais les fichiers présents sont `temoin_` et `test_`.

### Correction appliquée

- La convention de nommage et le format d'annotation sont documentés dans `data/dataset/README.md`.
- Le script `scripts/consolidate_dataset_metadata.py` recalcule les compteurs depuis les dossiers.
- Le fichier `plants_mapping.csv` est ajouté pour associer chaque future image à un pot et à une condition expérimentale.

### Action attendue

Avant d'entraîner un modèle sur des images réelles, exécuter le script de consolidation et vérifier que les valeurs de `metadata.json` correspondent à l'inventaire.

## Priorité 2 : ne pas présenter le dataset synthétique comme un résultat terrain

### Écart constaté

`imagerie/train_classifier.py` crée des données avec `generate_synthetic_dataset()` puis applique une validation croisée stratifiée aléatoire. Les images d'un même plant ne sont pas séparées par groupe dans ce protocole.

Un score F1 élevé sur ces données synthétiques démontre seulement que la chaîne logicielle fonctionne sur des classes créées par simulation. Il ne mesure pas la généralisation sur des plants réels, des luminosités différentes ou des prises de vue répétées.

### Correction appliquée

Le script `imagerie/validation_reelle.py` est ajouté. Il extrait les quatre variables depuis les images, utilise `LeaveOneGroupOut` avec `plant_id` comme groupe et produit les métriques F1, accuracy, kappa et MCC. Les métriques globales sont calculées sur les prédictions regroupées de tous les plis.

### Action attendue

Utiliser le fichier `plants_mapping.csv`. Sans plusieurs vues par plant, la validation par plant est impossible et le résultat doit être présenté comme exploratoire.

## Priorité 3 : unifier la formule GRVI dans le rapport et le code

### Écart constaté

Le code `imagerie/stress_detector.py` emploie :

```text
GRVI = (R - G) / (R + G)
```

Certains documents antérieurs utilisent la formule opposée. Inverser le signe sans réentraîner ou recalibrer le modèle rend les seuils et les variables incohérents.

### Décision recommandée

Conserver la formule actuellement implémentée, soit `(R - G) / (R + G)`, dans le rapport et dans les scripts. Indiquer que la convention est spécifique au pipeline choisi et que les seuils devront être étalonnés sur les données réelles.

## Priorité 4 : cadrer la navigation IMU + ArUco

### État actuel

La correction mécanique du centre de gravité a été testée. La proposition IMU + ArUco reste à faire valider par les encadrants avant toute annonce de navigation autonome validée.

### Action attendue

Insérer la note `docs/SECTION_RAPPORT_NAVIGATION_ARUCO.md` dans le rapport, avec les résultats réellement mesurés seulement. En cas de délai, conserver comme résultat expérimental minimal un décollage, un stationnaire et un atterrissage documentés.

## Priorité 5 : aligner le dépôt et les livrables

Les anciens README de `mission/` et `web/` annonçaient des fichiers absents. Ils ont été remplacés par une description de l'état réel et des éléments à intégrer.

La correspondance entre les quatre résultats du cahier des charges et les actions restantes est donnée dans `docs/COUVERTURE_CDC.md`.
