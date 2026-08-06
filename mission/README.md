# Mission : code embarqué MicroPython (ESP32-S3)
Binôme A : Robot Aérien Autonome

## Contenu

- `main.py` : code de vol récupéré le 6 août 2026 depuis le dépôt de travail
  de Liwingston (Robot_aerien1). Fonctions principales : connexion WiFi,
  liaison WebSocket avec la station sol, calibration MPU6050/SPL06,
  télémétrie périodique (batterie, attitude), traitement des commandes,
  vérifications RTH et urgence batterie. Le GPS y est commenté, cohérent
  avec le retrait du module pour l'équilibrage du centre de gravité.

## Configuration avant flash

1. Renseigner `WIFI_SSID` et `WIFI_PASSWORD` (placeholders, ne jamais committer
   de vrais identifiants).
2. Renseigner `SERVEUR_IP` (IP du PC station sol sur le même réseau).
3. La bibliothèque `drone` provient du kit pyDrone 01Studio : elle doit être
   présente sur la carte (non redistribuée ici, voir le dépôt officiel 01Studio).

## Points d'attention relevés à la relecture

- `ALTITUDE_CIBLE_CM = 80` alors que le plan optique impose 0,70 m : aligner
  la valeur avant les acquisitions (voir audit, point P1.8).
- Les seuils batterie du code sont exprimés en pourcentage, le rapport en
  tension (3,65 V) : harmoniser les deux référentiels et documenter la
  correspondance mesurée.
- `SEUIL_CORRECTION_CM = 15` et la parcimonie des corrections relèvent d'un
  choix de pilotage à justifier dans le rapport final.
