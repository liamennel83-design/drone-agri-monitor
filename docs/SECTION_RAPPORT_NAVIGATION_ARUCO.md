# Section à adapter pour le rapport : navigation IMU + ArUco

## Évolution envisagée de la navigation

La navigation GPS seule n'est pas adaptée à une parcelle de petite dimension, car sa précision est insuffisante pour un suivi fin des points de passage. Après correction du centre de gravité et tests de stabilité, une approche hybride est proposée pour validation par les encadrants.

Le principe est de conserver l'IMU pour les mesures rapides d'attitude et d'utiliser des marqueurs ArUco pour fournir des corrections de position visuelle. Les marqueurs ne remplacent pas les mesures de sécurité et ne constituent pas encore une validation de vol autonome.

## Architecture proposée

1. L'IMU fournit l'attitude et les variations rapides.
2. La caméra détecte périodiquement les marqueurs ArUco.
3. Un filtre de Kalman fusionne les estimations avec des paramètres qui devront être identifiés par mesure.
4. La trajectoire lawnmower reste planifiée à l'avance.
5. En cas de perte de détection, le prototype repasse en stationnaire ou atterrit selon la règle de sécurité retenue.

La fréquence réelle des corrections visuelles doit être mesurée. Elle ne doit pas être annoncée à 30 Hz sans essai démontré sur la chaîne ESP32, caméra et transmission.

## Positionnement des marqueurs

Les marqueurs sont placés sur un cadre périphérique, à l'extérieur de la zone occupée par les pots. Cette disposition évite de réduire la surface utile de culture. Une taille de 20 à 30 cm est étudiée. À 0,70 m d'altitude, un marqueur de 30 cm représente environ 680 pixels avec le GSD calculé de 0,44 mm par pixel, ce qui est suffisant pour une détection visuelle dans des conditions favorables.

## Protocole de validation proposé

| Étape | Mesure attendue | Critère indicatif |
| --- | --- | --- |
| Détection statique | Taux de détection des marqueurs | Mesuré pour plusieurs hauteurs et lumières |
| Position statique | Écart avec mesure au ruban | Objectif inférieur à 5 cm |
| Stationnaire | Dérive sur 30 secondes | Documenter la valeur observée |
| Trajectoire courte | Écart au couloir prévu | Objectif inférieur à 10 cm |
| Sécurité | Réaction à la perte de marqueur | Stationnaire ou atterrissage documenté |

## Limites et décision demandée

Cette approche est une proposition technique. Elle doit être validée par les encadrants avant d'être présentée comme une solution retenue. Si le délai ne permet pas la validation complète, le résultat expérimental conservé est un prototype de vol basique sécurisé, et la navigation IMU + ArUco est explicitement indiquée comme perspective de Master.
