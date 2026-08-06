# Couverture du cahier des charges au 6 août 2026
Binôme A : Robot Aérien Autonome
Rappel des résultats attendus (CDC) et état réel de couverture.

## Tableau de couverture

| Résultat attendu du CDC | Statut | Preuves / fichiers | Reste à faire |
|-------------------------|--------|--------------------|----------------|
| 1. Modèle de trajectoire simulé et validé | LARGEMENT COUVERT | simulation/lawnmower_planner.py, trajectory_optimizer.py, flight_simulator.py, modele_matlab.m ; bilan batterie 41,4 % en vol continu | une figure synthétique finale + relecture des hypothèses (1/2 journée) |
| 2. Prototype de vol fonctionnel (basique) | EN BONNE VOIE | mission/main.py (télémétrie, calibration, seuils batterie, commandes WebSocket), web/app_flask.py ; centre de gravité corrigé et testé | démonstration filmée : décollage, stationnaire 30 s, atterrissage ; mesure poussée + courbe batterie (1/2 journée) |
| 3. Base d'images annotées (stress / non-stress) | POINT CRITIQUE | structure prête : data/dataset (healthy/stressed), plants_mapping.csv, metadata régénérée par script ; protocole hydrique : docs/PROTOCOLE_CAPTEURS_HUMIDITE.md | acquisitions réelles à partir du 11 août (plan), minimum 60 images réelles annotées ; les 50 images actuelles sont synthétiques (tests du pipeline uniquement) |
| 4. Rapport avec recommandations pour la suite en Master | À FINALISER | rapports S9-S14, audit, notes techniques | rapport final 20-30 p + section recommandations (trames ci-dessous) |

## Trame de la section "Recommandations pour la suite en Master"

1. Navigation autonome complète : industrialiser la fusion IMU + ArUco
   (corrections vision 1-2 Hz, Kalman caractérisé), avec évaluation
   statistique de l'erreur de position sur trajectoire.
2. Passage à un vrai NDVI : double caméra RGB + NIR ou filtre passe-bande,
   calibration radiométrique par cibles de réflectance.
3. Dataset élargi : plusieurs sessions, plusieurs variétés, conditions
   d'éclairage variées ; objectif 300+ images réelles par classe.
4. Chaîne ML : features enrichies (texture, histogrammes ExG/GRVI),
   comparaison RandomForest / SVM / baseline par seuils, après calibration
   des seuils sur données terrain.
5. Intégration inter-binômes : capteurs d'humidité du sol du Binôme C et
   données du Binôme B (mesures de référence au sol) pour une validation
   croisée capteur/image.
6. Durcissement du prototype : retour automatique (RTH) validé en vol,
   journalisation des vols, procédure de sécurité écrite.

## Décision structurante du 6 août

Le CDC n'exige pas la cartographie autonome complète pour la remise du
23 août. L'effort est donc concentré sur : (a) une base d'images réelles
annotées, (b) un vol basique démontré et filmé, (c) un rapport honnête
intégrant les corrections de l'audit. Le reste est présenté en perspectives.
