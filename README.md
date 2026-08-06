# Drone Autonome — Détection du Stress Hydrique

**Binôme A** (FANOGNY Hernandez Liwingston & RAKOTONIRINA Ny Antso Fyh Arihvony)
Licence L3 EIT — ESP Antsiranana — mai → août 2026

> Objectif : drone autonome capable d'acquérir des images aériennes géolocalisées
> et de cartographier le stress hydrique des cultures (parcelle 1,0 m × 2,0 m, 24 pots de tomates).

## ⚠️ État du projet & audit

Un audit complet des failles a été réalisé le 6 août 2026 :
**→ [docs/AUDIT_FALLES_2026-08-06.md](docs/AUDIT_FALLES_2026-08-06.md)** (failles P0/P1/P2 + plan d'urgence J-4 → J0).

Points clés : dataset 100 % synthétique à remplacer par de la collecte réelle,
validation ML reprise sur pixels réels (`imagerie/validation_reelle.py`),
métadonnées consolidées par script (`scripts/consolidate_dataset_metadata.py`).

## Matériel

- PyDrone 01Studio ESP32-S3 (42 g, 130×130 mm, ~8 min d'autonomie)
- Caméra OV2640 66° sans filtre IR (sensible 650 + 850 nm)
- GPS BN-220 Ublox M8030 (HOME uniquement ; navigation fine = IMU + ArUco)
- Batterie LiPo 1S 400 mAh (RTH 3,65 V, urgence 3,50 V)

## Paramètres optiques validés

- Altitude 0,70 m → GSD = 0,44 mm/pixel ; emprise 0,70 m × 0,52 m
- Vitesse 0,20 m/s → flou 0,45 px < 0,5 px
- Indices : ExG = 2G − R − B ; GRVI = (G − R)/(G + R) *(convention unique)*

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Structure

```
imagerie/
  validation_reelle.py        # Extraction ExG/GRVI depuis images + LOGO par plante
                              # + Kappa/MCC + baseline seuils (pipeline corrigé)
scripts/
  consolidate_dataset_metadata.py   # metadata.json régénéré depuis le disque (source unique)
data/dataset/
  healthy/  stressed/  plants_mapping.csv
                              # images RÉELLES (non versionnées) + mapping image→pot
models/                       # modèles + résultats JSON de validation
simulation/                   # Lawnmower, trajectoires, simulateur (à réintégrer)
mission/                      # code MicroPython embarqué (à réintégrer)
web/                          # station sol Flask + carte Leaflet (à réintégrer)
docs/                         # audit + notes techniques
reports/                      # rapports hebdomadaires (docx)
```

## Validation ML (pipeline corrigé)

```bash
# 1. Après chaque collecte : régénérer les métadonnées (compteurs vérité)
python scripts/consolidate_dataset_metadata.py

# 2. Validation honnête sur images réelles, split par plante
python imagerie/validation_reelle.py
# -> models/validation_reelle_results.json : F1 poolé, Kappa, MCC,
#    IC bootstrap 95 %, comparaison baseline seuils, verdict vs critère F1 > 0,70
```

Convention GRVI unique : `(G − R)/(G + R)`. Split par plante obligatoire
(`data/dataset/plants_mapping.csv` : colonnes `image,plante`).
