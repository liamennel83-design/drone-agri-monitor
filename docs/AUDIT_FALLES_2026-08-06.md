# Audit des failles du projet
Binôme A : Robot Aérien Autonome, suivi du stress hydrique par imagerie
Date : 6 août 2026. Remise et soutenance visées : 23 août 2026 (marge incluse).
Sources : archive complète du workspace, dépôt GitHub, rapports S9 à S14, retours encadrants, fichiers JSON des modèles, relecture du code source Python.

## Résumé en dix lignes

Le projet est bien documenté et les justifications physiques (optique, vitesse, souffle) sont correctes et vérifiables. En revanche la chaîne machine learning repose entièrement sur des données synthétiques, la validation statistique a été faite sur des features générées en mémoire et non sur des pixels, le classifieur livré a été entraîné sur 25 échantillons avec une validation croisée par image de type StratifiedKFold (fuite intra-plante, F1 = 1,000), et aucune image réelle n'a encore été acquise puisque la plantation n'a pas démarré. La dérive du drone était liée au centre de gravité ; la correction mécanique a été testée après retrait du GPS. La nouvelle navigation IMU + ArUco reste à faire valider par les encadrants. Le planning initial finissait le 10 août ; la nouvelle cible au 23 août rend le plan ci-dessous tenable à condition d'acheter des plants adultes en pot cette semaine et de lancer le protocole de stress dès l'acclimatation.

## P0. Failles bloquantes

### P0.1 Classifieur entraîné et validé sans aucune donnée réelle
Preuves vérifiées dans le code :
- `imagerie/train_classifier.py` lignes 151 à 156 : `cross_val_score(..., cv=StratifiedKFold(n_splits=5, shuffle=True), scoring='f1')`. Split par image sans groupage par plante : c'est exactement la fuite de données soupçonnée par les encadrants ("split stratifié par plante et non par image").
- `models/stress_rf_v1_meta.json` : `n_samples = 25`, `cv_f1_mean = 1.0`. Le modèle publié provient de 25 vecteurs de features synthétiques.
- `data/dataset/metadata.json` annonce 60 images (30/30), `metadata_parcelle.json` en annonce 50 (25/25), les dossiers contiennent réellement 25 + 25 fichiers `temoin_XXX / test_XXX`, le README dataset documente une nomenclature différente (`sain_XXX / stresse_XXX`). Quatre sources, quatre versions.

Correction livrée : `scripts/consolidate_dataset_metadata.py` régénère `metadata.json` depuis le disque (source unique de vérité). `imagerie/validation_reelle.py` applique un Leave-One-Group-Out par plante avec métriques poolées.

### P0.2 La "validation robuste" précédente ne portait pas sur des pixels
Le guide de test de l'ancienne procédure indique que le script régénérait un dataset synthétique en mémoire (12 plantes x 5 images). Résultats rapportés : LOPO F1 = 0,366 +/- 0,439, Bootstrap 0,790 [0,571 ; 0,933], malgré un statut "Terminé 100 %" dans le rapport S13-S14.
Deux défauts cumulés : features non extraites des images, et F1 par fold mathématiquement dégénéré (test mono-classe, F1 indéfini mis à 0 par convention ; la moyenne des folds devient bipolaire, d'où l'écart-type de 0,44). La lecture correcte du LOPO passe par la matrice de confusion poolée et, par fold, l'accuracy équilibrée.

### P0.3 Le dataset synthétique est séparable par construction (nouveau résultat)
Exécution de `validation_reelle.py` sur les 50 images stockées (`models/validation_synthetique_results.json`) :
- RandomForest, LOGO par image : F1 poolé = 1,000, Kappa = 1,000, MCC = 1,000, Bootstrap IC95 [1,0 ; 1,0].
- Baseline par seuils documentés (ExG < 0,2 et GRVI > 0,15) : F1 = 0,0.
Enseignements : le générateur produit des classes artificiellement séparées ; un score parfait sur ce dataset ne prouve rien sur le terrain ; et les seuils fixes documentés ne sont pas calibrés sur des statistiques d'image moyennes (à recalibrer après collecte réelle). Toute valeur F1 = 1,000 issue de ces images doit être présentée comme un test de santé du pipeline, jamais comme une performance.

### P0.4 Aucune acquisition réelle possible à ce jour
La plantation n'a pas eu lieu. La cible retenue est l'achat de 24 plants de tomates adultes en pot (12 témoins + 12 test). Conséquences : protocole de stress compressé (arrosage différentiel dès la fin d'acclimatation), première acquisition de référence avant le début du stress, 2 à 3 acquisitions espacées ensuite. La cartographie et le ré-entraînement du modèle dépendent intégralement de ce calendrier.

### P0.5 Navigation IMU + ArUco non encore validée par les encadrants
La correction du centre de gravité a été testée après retrait du module GPS (5,3 g). Décision en attente de présentation : navigation intérieure par IMU (MPU6050) + marqueurs ArUco avec filtre de Kalman. Tant que cette approche n'est pas validée, la trajectoire Lawmower autonome reste en suspens ; le filet de sécurité est l'acquisition statique manuelle à 0,70 m (voir Plan, scénario B).

### P0.6 Code de vol introuvable dans le dépôt
`mission/` et `web/` ne contiennent que des README. Le code MicroPython embarqué (connexion WiFi, WebSocket, calibration, boucle de mission) n'apparaît ni dans le dépôt ni dans l'archive analysée. Le livrable "code source complet" n'est pas reconstituable en l'état.

## P1. Incohérences techniques à corriger dans les documents

| Réf. | Constat | Preuve | Correction |
|------|---------|--------|------------|
| P1.1 | Signe du GRVI opposé entre code et rapport | stress_detector.py lignes 36, 95, 118 : (R-G)/(R+G) ; rapport S13-S14 paragraphe 4.3 : (G-R)/(G+R) | Aligner le rapport sur le code : GRVI = (R-G)/(R+G) ; feuillage sain -> GRVI négatif ; corriger aussi RESUME_COMPLET et MEGA_PROMPT |
| P1.2 | Seuil batterie RTH : 3,65 V ou 3,60 V selon les documents | MEGA_PROMPT et rapport : 3,65 V ; RESUME_COMPLET : 3,60 V "validé" | Une seule valeur : 3,65 V ; plus une mesure expérimentale (stationnaire chronométré avec relevé de tension) exigée depuis S11-S12 |
| P1.3 | Nombre d'images cible : 15, 66 ou 96 selon les documents | Rapport §4.1 ; MEGA_PROMPT tâche 4 ; livrables | Unifier : 15 tuiles par vol x nombre de vols, calcul joint |
| P1.4 | Marqueurs ArUco 30 x 30 cm placés aux coins de la parcelle | Rapport §3.4.7 | Conflit avec la grille de pots ; placer les marqueurs hors zone de culture sur cadre périphérique ; joindre le calcul de taille apparente (~690 px au zénith à 0,70 m, ~190 px à 2,5 m ; voir NOTE_NAVIGATION_IMU_ARUCO.md) |
| P1.5 | Chaîne vision annoncée à 30 Hz | Rapport §3.4.5 | L'ESP32-S3 ne streame pas du 2 MP à 30 Hz ; annoncer honnêtement une correction vision à 1-2 Hz, IMU pour la prophétie haute fréquence ; les paramètres Q et R du filtre de Kalman doivent être mesurés, pas choisis |
| P1.6 | Tableau des courbes d'apprentissage incohérent avec le JSON | Rapport §4.4.4 tailles 10/20/30/60 ; JSON : [9, 19, 28, 38, 48] | Reporter les tailles réelles du JSON |
| P1.7 | Poussée moteur jamais mesurée | "T_max = 0,72 N estimé" ; question en suspens depuis deux rapports | Mesure à la balance (drone à l'envers, 15 minutes) ; question probable du jury |

## P2. Renforts scientifiques recommandés

1. Ajouter Kappa de Cohen et MCC dans le rapport (déjà calculés par validation_reelle.py) ; ces métriques ont été explicitement appréciées chez le Binôme B.
2. Présenter la baseline par seuils à côté du RandomForest ; si les seuils recalibrés suffisent, le dire franchement.
3. Préciser l'opérationnalisation de "50 % ETc" sans station météo : moitié du volume d'arrosage témoin, plus un relevé d'humidité du sol par pesée ou capteur, à écrire noir sur blanc pour la reproductibilité.
4. Expliquer que "la plante 10" en faute 5 fois sur 5 était un artefact du générateur synthétique, pas un résultat biologique.
5. Donner des liens directs ou DOI pour les trois références ArUco (Romero 2017, Embedded ArUco 2021, ArUco Recognition) aujourd'hui citées "ResearchGate" sans traçabilité.
6. Retirer du rapport toute phrase présentant "Validation robuste : Terminé 100 %" ; la remplacer par le statut réel et les métriques à jour.

## Ce qui est solide et ne doit pas bouger

- GSD = 0,44 mm/pixel à 0,70 m, emprise 0,70 m x 0,52 m (formules vérifiées).
- Vitesse 0,20 m/s pour un flou de 0,45 pixel ; calcul de vitesse induite 3,85 m/s cohérent.
- Démarche hypothèse, test, réfutation sur la dérive, qualifiée d'exemplaire par l'encadrant.
- Distinction assumée entre GRVI et un vrai NDVI.
- Le projet a su détecter lui-même son F1 = 1,000 suspect : c'est un argument de soutenance, à condition de boucler avec des données réelles.
