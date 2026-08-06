# Note technique : navigation intérieure IMU + vision ArUco
Binôme A : Robot Aérien Autonome
Document préparé pour validation par les encadrants, 6 août 2026.

## 1. Pourquoi abandonner le GPS pour la navigation fine

- Précision du GPS BN-220 : environ 2 m (CEP), soit deux fois la largeur de la parcelle (1,0 m).
- Le module GPS de 5,3 g déséquilibrait le centre de gravité du drone (42 g) : c'était la cause de la dérive systématique avant-gauche observée en S11-S12. Après retrait du module et correction du centrage, le comportement en vol a été vérifié.
- Le GPS conserve un rôle de référence HOME en usage extérieur ; il est démonté pour les campagnes intérieures.

## 2. Solution proposée

Fusion de deux sources complémentaires par filtre de Kalman :

| Source | Fréquence | Rôle | Limite |
|--------|-----------|------|--------|
| IMU MPU6050 | ~100 Hz | prophétie rapide de la position | dérive temporelle |
| Caméra OV2640 + marqueurs ArUco | 1 à 2 Hz effectif | correction absolue sans dérive | latence WiFi |

Etat du filtre : [x, y, z, vx, vy, vz]. Les paramètres de bruit Q (processus) et R (mesure) seront caractérisés expérimentalement (immobile sur table : variance de l'IMU ; marqueur à distance connue : variance de la pose ArUco) au lieu d'être fixés arbitrairement.

Point d'honnêteté technique : le flux 2 MP ne peut pas transiter à 30 Hz en WiFi ESP32 ; la correction vision sera de l'ordre de 1 à 2 Hz, l'IMU portant la haute fréquence. La bibliographie citée (Romero 2017 ; Embedded ArUco 2021 : précision moyenne 2,03 cm) reste compatible avec ce schéma.

## 3. Placement des marqueurs (correction du plan initial)

Le plan initial plaçait quatre marqueurs de 30 x 30 cm aux coins de la parcelle, en conflit avec la grille de 12 pots. Proposition corrigée : quatre marqueurs sur un cadre périphérique, hors zone de culture.

Budget de détection (focale 3,6 mm, pixel 2,24 µm, marqueur 30 cm) :

| Configuration | Taille apparente | Détectabilité |
|---------------|------------------|---------------|
| Au zénith, 0,70 m | ~690 px | très confortable |
| Coin opposé, distance ~2,5 m | ~190 px | détectable (module ~30 px) |

## 4. Protocole de validation proposé

1. Détection statique à 0,3 m, 0,5 m, 0,7 m : taux de détection supérieur à 90 %.
2. Précision de position : comparaison pose estimée / mesure à la règle, erreur inférieure à 5 cm.
3. Vol stationnaire corrigé : dérive résiduelle inférieure à 10 cm sur 30 s.
4. Suivi de trajectoire lawnmower sur 1,0 x 2,0 m : erreur latérale inférieure à 10 cm.

Filet de sécurité (scénario B) : si l'étape 4 n'est pas atteinte à temps, la campagne d'imagerie est menée en acquisition statique manuelle à 0,70 m au-dessus de chaque tuile ; la navigation autonome devient alors un développement présenté séparément, avec ses résultats partiels documentés.

## 5. Questions soumises aux encadrants

1. Validez-vous le schéma IMU + Kalman + corrections ArUco en intérieur ?
2. Le placement des marqueurs sur cadre périphérique vous convient-il ?
3. Le protocole de caractérisation de Q et R (section 2) est-il suffisant ?
4. Acceptez-vous le scénario B comme mode d'acquisition si l'étape 4 est en retard, la partie agronomique étant prioritaire sur la partie navigation ?
