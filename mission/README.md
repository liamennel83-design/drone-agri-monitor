# Mission — Code Vol MicroPython

Ce dossier contient le code MicroPython pour le drone Pydrone.

## Structure

```
mission/
├── firmware.py       # Firmware principal
├── config.py         # Configuration du drone
├── navigation.py     # Algorithmes de navigation
└── communication.py  # Communication WebSocket
```

## Firmware Principal

### firmware.py
- Initialisation des capteurs (MPU6050, SPL06, GPS)
- Boucle principale de vol
- Gestion des commandes (takeoff, land, hover)
- Communication WebSocket avec le serveur

## Configuration

### config.py
- Paramètres du drone (masse, dimensions)
- Paramètres de vol (altitude, vitesse)
- Seuils de sécurité (batterie, Wi-Fi)

## Navigation

### navigation.py
- Algorithme Lawnmower
- Suivi de waypoints
- Correction de dérive (pitch, roll)

## Communication

### communication.py
- Serveur WebSocket
- Protocole JSON
- Gestion des commandes et télémétrie

---

*Mission créée le 10 juillet 2026*
*Binôme A — Projet Robot Aérien Autonome*