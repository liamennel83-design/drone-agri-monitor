# Web — Interface Flask et Leaflet

Ce dossier contient l'interface web pour la supervision du drone.

## Structure

```
web/
├── page.py           # Serveur Flask principal
├── templates/        # Templates HTML
└── static/           # Fichiers statiques (CSS, JS)
```

## Interface Web

### page.py
- Serveur Flask avec WebSocket
- Carte Leaflet.js pour la visualisation
- Gestion des waypoints (sauvegarde, chargement)
- Interface de contrôle du drone

## Fonctionnalités

- Visualisation en temps réel de la position du drone
- Affichage des waypoints et de la trajectoire
- Tableau de bord de télémétrie
- Terminal de commandes manuelles

---

*Web créé le 10 juillet 2026*
*Binôme A — Projet Robot Aérien Autonome*