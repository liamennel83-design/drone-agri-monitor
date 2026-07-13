# Simulation — MATLAB et Python

Ce dossier contient les scripts de simulation pour le projet.

## Structure

```
simulation/
├── matlab/           # Scripts MATLAB UAV Toolbox
│   └── simulate_pydrone_uavtoolbox.m
└── python/           # Scripts Python de simulation
    └── run_simulation.py
```

## MATLAB UAV Toolbox

### simulate_pydrone_uavtoolbox.m
- Charge les waypoints depuis le CSV
- Simule la trajectoire en repère NED
- Visualise la trajectoire 3D
- Compatible avec waypointTrajectory

## Python Simulation

### run_simulation.py
- Simulation de la trajectoire Lawnmower
- Calcul des métriques de performance
- Génération de graphiques

---

*Simulation créée le 10 juillet 2026*
*Binôme A — Projet Robot Aérien Autonome*