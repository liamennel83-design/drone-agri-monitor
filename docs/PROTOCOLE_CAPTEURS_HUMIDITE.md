# Protocole de stress hydrique piloté par capteur d'humidité du sol
Binôme A : Robot Aérien Autonome
Décision du 6 août 2026 : l'indicateur "50 % ETc" est remplacé par un pilotage
à l'humidité du sol mesurée. Ce document rend le protocole reproductible.

## 1. Principe

Sans station météo, l'ETc n'est pas mesurable directement. On pilote donc la
contraste hydrique sur l'état du sol : le groupe témoin est maintenu à sa zone
de confort hydrique, le groupe test à environ la moitié. L'humidité du sol
devient la variable de contrôle, mesurée et journalisée quotidiennement.

## 2. Matériel

| Item | Recommandation |
|------|----------------|
| Type de capteur | capacitif (v1.2 ou v2.0), pas résistif (corrosion rapide) |
| Nombre | idéalement 2 par parcelle en points fixes ; si un seul capteur : mesures itinérantes sur 6 points fixes numérotés par parcelle |
| Mutualisation | le Binôme C dispose de capteurs sol : emprunt possible (recommandation transversale des encadrants) |
| Lecture | carte ESP32/Arduino ou module analogique affichant la valeur brute 0-4095 |

## 3. Étalonnage (30 minutes, une fois)

1. Mesure à l'air libre (sec) : valeur brute notée `RAW_SEC`.
2. Mesure sonde plongée dans l'eau : valeur brute notée `RAW_EAU`.
3. Conversion : humidité relative (%) = 100 x (RAW - RAW_SEC) / (RAW_EAU - RAW_SEC).
4. Référence parcelle : mesurer le témoin juste après un arrosage complet
   (drainage terminé) : c'est la "capacité au champ" de ce substrat, notée CC.

## 4. Consignes d'arrosage

| Groupe | Consigne |
|--------|----------|
| Témoin | maintenir entre 80 % et 100 % de CC (arrosage quotidien léger) |
| Test | laisser descendre à environ 40-50 % de CC, puis maintenir par petits apports contrôlés |

Le ratio 50 % du CDC est ainsi porté par une mesure, pas par un volume théorique.

## 5. Journal de mesure (un CSV, versionné)

Colonnes : date, heure, parcelle, point_de_mesure, valeur_brute, humidite_%,
volume_arrose_mL, temperature_ambiante, remarque (flétrissement, chlorose).
Fréquence : 1 relevé par jour, heure fixe, avant l'arrosage éventuel.

## 6. Articulation avec les acquisitions d'images

- Chaque session d'imagerie (baseline, J+4, J+8/J+10) est associée aux relevés
  du jour dans le journal ; les deux fichiers se citent mutuellement.
- La classe finale du pot (`healthy` / `stressed`) tient compte du groupe ET
  du relevé d'humidité le jour de l'image : un pot test non stressé
  (humidité encore haute) ne doit pas entrer dans la classe stressed.

## 7. Phrase prête pour le rapport

"Le contraste hydrique entre parcelles a été contrôlé par mesure capacitive
quotidienne de l'humidité du sol (6 points fixes par parcelle), la parcelle
témoin étant maintenue au-dessus de 80 % de la capacité au champ et la
parcelle test autour de 45 +/- 5 %, ce qui opérationnalise le cahier des
charges (50 % ETc) sans station météo."
