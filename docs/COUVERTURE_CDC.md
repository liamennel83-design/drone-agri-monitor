# Couverture des résultats attendus

## Résultat 1 : modèle de trajectoire simulé et validé

**Éléments présents** : `simulation/lawnmower_planner.py`, `simulation/trajectory_optimizer.py`, `simulation/flight_simulator.py` et figures dans `reports/figures/`.

**À finaliser** : exécuter les scripts avec les paramètres de la parcelle retenue, conserver la figure de trajectoire, indiquer le temps de mission et la marge batterie. Le rapport doit préciser que la validation est une validation par simulation.

## Résultat 2 : prototype de vol fonctionnel, niveau basique

**Résultat minimal défendable** : décollage, stationnaire stable, atterrissage et télémétrie de base, avec une courte vidéo et une fiche d'essai.

**À finaliser** : noter la masse finale, la configuration réellement embarquée, l'altitude testée, la durée de stationnaire et le comportement de la batterie. La navigation IMU + ArUco est une évolution soumise à la validation des encadrants.

## Résultat 3 : base d'images annotées

**Éléments présents** : arborescence `healthy/` et `stressed/`, images synthétiques et scripts de traitement.

**À finaliser** : acheter ou réunir des plants en pots homogènes, acquérir des images réelles, renseigner `plants_mapping.csv`, mesurer l'humidité du sol et générer les métadonnées. Une acquisition statique à hauteur constante est recevable pour constituer la base d'images si le vol autonome n'est pas prêt.

## Résultat 4 : rapport avec recommandations pour le Master

**À inclure** :

- Limites du dataset synthétique et plan de collecte réel.
- Protocole d'annotation et validation par plant.
- Validation progressive de l'IMU + ArUco.
- Fusion future avec capteurs d'humidité du sol.
- Augmentation du nombre de plants, de jours de suivi et de conditions lumineuses.
- Carte de stress et automatisation de la mission comme prolongements de Master.

## Priorités jusqu'au 23 août

1. Envoyer le rapport intermédiaire avec une description honnête de l'état de validation.
2. Préparer et filmer le vol basique après les vérifications de sécurité.
3. Mettre en place les pots, le capteur et le journal d'acquisition.
4. Collecter, annoter et sauvegarder les premières images réelles.
5. Mettre à jour le rapport final avec les résultats réellement obtenus et les limites restantes.
