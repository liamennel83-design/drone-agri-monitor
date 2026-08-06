# Dataset d'imagerie foliaire
Binôme A : Robot Aérien Autonome

## Contenu actuel

- healthy/ : 25 images synthétiques (témoin) générées le 13 juillet 2026
- stressed/ : 25 images synthétiques (test) générées le 13 juillet 2026

Ces images servent uniquement au test fonctionnel de la chaîne de traitement.
Elles ne permettent aucune conclusion sur les performances réelles du
classifieur (voir docs/AUDIT_FALLES_2026-08-06.md, points P0.1 à P0.3).
Le remplacement par les acquisitions réelles est prévu à partir du 11 août 2026
selon docs/PLAN_REMISE_23_AOUT.md.

## Règles d'alimentation

1. Nomenclature cible pour les acquisitions réelles : `<groupe>_p<pot>_v<vue>.jpg`,
   exemple : `temoin_p03_v2.jpg` (groupe temoin ou test, pot 01 à 12, vue 01 à NN).
   Ce format permet le groupage par plante dans la validation.
2. Renseigner `plants_mapping.csv` (colonnes `image,plante`) à chaque acquisition.
3. Après tout ajout, régénérer les métadonnées :
   `python scripts/consolidate_dataset_metadata.py`
4. Ne jamais mélanger images synthétiques et réelles dans un même entraînement ;
   archiver les synthétiques dans un sous-dossier daté si nécessaire.

## Annotation

| Catégorie | Définition opérationnelle |
|-----------|---------------------------|
| healthy | parcelle témoin, arrosage 100 % du volume de référence |
| stressed | parcelle test, arrosage 50 % du volume de référence, signes de stress visibles ou mesurés |
