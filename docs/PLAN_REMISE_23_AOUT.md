# Plan de remise au 23 août 2026
Binôme A : Robot Aérien Autonome
Date de rédaction : 6 août 2026. Cible : soutenance et remise le 23 août 2026.

## Hypothèses de départ

- Les 24 plants seront achetés adultes en pot (pas de semis) : le protocole démarre par l'acclimatation, pas par J14.
- Le centre de gravité est corrigé et testé ; la navigation IMU + ArUco attend la validation des encadrants.
- Scénario A : acquisition par vol autonome. Scénario B : acquisition statique manuelle à 0,70 m (filet de sécurité, déclenché si la validation navigation tarde).

## Calendrier

| Date | Action | Responsable | Livrable |
|------|--------|-------------|----------|
| 6-7 août | Dépôt figé (audit, pipeline, notes) ; présentation de la note navigation aux encadrants | Fyh + Liwingston | dépôt à jour, note envoyée |
| 8-9 août | Achat de 24 plants adultes homogènes (même variété, même stade), 12 témoins + 12 test ; installation en grille 3 x 4 sur 1,0 x 2,0 m | Les deux | parcelle prête, photo datée |
| 10-11 août | Acclimatation (ombre, arrosage égal) ; mesure poussée moteur et courbe batterie (balance + stationnaire chronométré) | Liwingston | deux mesures chiffrées |
| 11 août | Acquisition de référence AVANT stress : 15 tuiles x 24 pots, scénario B si besoin ; métadonnées (heure, température, humidité sol) | Fyh | data/dataset baseline |
| 12-18 août | Arrosage différentiel : témoin 100 % du volume, test 50 % ; relevés quotidiens | Fyh | journal d'arrosage |
| 15-16 août | 2e acquisition ; si encadrants OK et tests ArUco concluants, 1er vol autonome filmé | Les deux | dataset J+4, vidéo |
| 19-20 août | 3e acquisition ; extraction features ; validation_reelle.py avec plants_mapping.csv ; ré-entraînement pkl ; carte de stress | Fyh | F1/Kappa/MCC réels, heatmap |
| 20-21 août | Rapport final : statuts corrigés (audit P1), chiffres unifiés (grep : 50/25, 3,65 V, GRVI) | Les deux | rapport relu |
| 22 août | Slides + répétition de l'oral ; préparation des réponses aux questions pièges | Les deux | présentation prête |
| 23 août | Soutenance et remise | Les deux | |

## Points de bascule

1. Si les encadrants rejettent ou retardent la validation ArUco : passage immédiat au scénario B pour toutes les acquisitions, sans attendre.
2. Si les plants test ne montrent pas de signe visible de stress au 17 août (arrosage réduit de moitié) : réduire à 0 % d'arrosage sur 48 h et documenter la décision ; le stress foliaire (flétrissement puis chlorose) apparaît typiquement en 4 à 8 jours sous serre chaude.
3. Si le modèle réel donne F1 poolé inférieur à 0,70 : le présenter tel quel avec les IC bootstrap, la baseline par seuils recalibrée et la discussion des causes ; un résultat honnête vaut mieux qu'un 1,000 suspect.

## Risques résiduels et parades

| Risque | Parade |
|--------|--------|
| Plants hétérogènes à l'achat (âge, variété) | sélection stricte en jardinerie, photo de chaque pot à J0 |
| Mortalité d'un plant | prévoir 2 plants de réserve par groupe, numérotés hors grille |
| Perte du code MicroPython | récupération immédiate depuis la carte ESP32 ou le poste de développement, commit dans mission/ |
| Données manquantes le jour J | plants_mapping.csv renseigné à chaque acquisition, metadata régénéré par script |
