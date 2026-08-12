# Module de vol embarqué

Ce dossier est réservé au code MicroPython réellement déployé sur le Pydrone ESP32-S3.

Aucun firmware de vol n'est actuellement versionné dans ce dépôt. Les fichiers décrits dans une ancienne version de cette documentation ne sont donc pas annoncés comme disponibles.

## À intégrer avant la remise

- Point d'entrée MicroPython utilisé lors du dernier essai.
- Configuration matérielle réellement embarquée : caméra, IMU, GPS si présent, batterie.
- Paramètres de sécurité : altitude, durée de stationnaire, seuil de batterie, comportement en cas de perte de communication.
- Protocole de commandes entre la station sol et le drone.

## Règle de traçabilité

Toute version testée doit être copiée dans ce dossier avec une date, puis associée à une fiche d'essai décrivant le résultat observé.
