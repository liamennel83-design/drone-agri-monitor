# Web : station sol
Binôme A : Robot Aérien Autonome

## Contenu

- `app_flask.py` : interface "Mission Planner" (Flask + Leaflet), récupérée le
  6 août 2026 depuis le dépôt de travail de Liwingston (Robot_aerien1). Page
  unique servie sur `/`, relais vers le serveur WebSocket du drone
  (`ws://127.0.0.1:8765`).

## Lancement

```bash
pip install -r requirements.txt
python web/app_flask.py
# ouvrir http://127.0.0.1:5000 dans le navigateur du PC station sol
```

## Évolutions prévues (après les acquisitions réelles)

1. Import des résultats du classifieur (models/*.json) et affichage de la
   carte de stress de la parcelle en surimpression Leaflet.
2. Journal des vols (télémétrie reçue) exporté en CSV pour le rapport.
3. Bandeau d'alerte aligné sur les seuils batterie mesurés.
