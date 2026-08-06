# Section prête à insérer dans le rapport hebdomadaire
Sujet : navigation intérieure IMU + vision ArUco
A copier-coller tel quel, puis compléter les placeholders avant l'envoi.

## X. Changement d'approche de navigation

### X.1 Rappel du problème

La navigation fine par GPS a été abandonnée pour deux raisons mesurées : la
précision du BN-220 (environ 2 m CEP) excède la largeur de la parcelle (1,0 m),
et la masse du module (5,3 g) déséquilibrait le centre de gravité du drone
(42 g), ce qui a été identifié comme cause principale de la dérive
avant-gauche documentée en S11-S12. Après retrait du module et correction du
centrage, le comportement en vol a été vérifié [insérer mesure : durée du
stationnaire et dérive résiduelle observée].

### X.2 Solution proposée : fusion IMU + marqueurs ArUco

| Source | Fréquence | Rôle | Limite |
|--------|-----------|------|--------|
| IMU MPU6050 | ~100 Hz | prophétie rapide de la position | dérive temporelle |
| Caméra OV2640 + ArUco | 1 à 2 Hz effectif | correction absolue | latence WiFi |

Etat du filtre de Kalman : [x, y, z, vx, vy, vz]. Les paramètres de bruit Q
et R seront caractérisés expérimentalement (variance IMU au repos, variance
de pose ArUco à distance connue) plutôt que fixés arbitrairement.

### X.3 Placement des marqueurs

Correction du plan initial : les quatre marqueurs de 30 x 30 cm initialement
prévus aux coins de la parcelle auraient recouvert une partie de la grille de
pots. Ils seront installés sur un cadre périphérique, hors zone de culture.
Taille apparente d'un marqueur de 30 cm (focale 3,6 mm, pixel 2,24 µm) :
environ 690 px au zénith à 0,70 m, environ 190 px à 2,5 m (coin opposé).

### X.4 Protocole de validation

1. Détection statique à 0,3 m, 0,5 m, 0,7 m : taux supérieur à 90 %.
2. Précision de position : erreur inférieure à 5 cm versus mesure à la règle.
3. Stationnaire : dérive résiduelle inférieure à 10 cm sur 30 s.
4. Suivi de trajectoire lawnmower : erreur latérale inférieure à 10 cm.

Résultats : [à compléter après les tests]

### X.5 Point de vigilance assumé

Le flux vidéo 2 MP ne transite pas à 30 Hz en WiFi ESP32 ; la correction
vision est donc prévue à 1-2 Hz, la haute fréquence étant portée par l'IMU.
Ce compromis est conforme aux précisions de la bibliographie (Romero 2017 ;
Embedded ArUco 2021).

### X.6 Questions soumises aux encadrants

1. Validation du schéma IMU + Kalman + corrections ArUco en intérieur.
2. Validation du placement des marqueurs sur cadre périphérique.
3. Accord sur le mode dégradé d'acquisition statique manuelle si l'étape 4
   du protocole n'est pas atteinte avant la remise (l'imagerie réelle étant
   prioritaire pour la base annotée).

---

## Modifications associées à appliquer dans le reste du rapport avant envoi

- Paragraphe indices de végétation : écrire GRVI = (R - G)/(R + G) partout
  (convention du code embarqué ; feuillage sain donne un GRVI négatif).
- Tableau des courbes d'apprentissage : remplacer les tailles 10/20/30/60 par
  les tailles réelles du fichier JSON : 9, 19, 28, 38, 48.
- Seuil batterie : une seule valeur pour le RTH, 3,65 V.
- Statut "Validation robuste du classificateur : Terminé 100 %" : reformuler
  en "validation méthodologique mise en place ; performance sur données
  réelles en cours de mesure".
- Préciser que le jeu actuel (50 images) est synthétique et que tout score
  parfait sur ce jeu n'est pas une mesure de performance terrain.
