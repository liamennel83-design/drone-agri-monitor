# Module Simulation - Sous-Projet 1 : Trajectoires

Ce dossier contient les modules de planification et simulation de trajectoires pour le drone Pydrone.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `lawnmower_planner.py` | Algorithme de couverture Lawnmower (boustrophédon) |
| `trajectory_optimizer.py` | Optimisation multi-critères des paramètres de mission |
| `flight_simulator.py` | Simulation de vol avec modèle cinématique |

## Algorithmes implémentés

### 1. Lawnmower (Boustrophédon)

Algorithme de couverture systématique générant des trajectoires parallèles avec chevauchement.

**Référence** : Choset, H. (2001). "Coverage for robotics." Annals of Mathematics and AI.

**Formules clés** :
```
Espacement photos : dx = Wx × (1 - of)
Espacement lignes : dy = Wy × (1 - os)
```

### 2. Optimisation multi-critères

Optimise les paramètres de mission selon :
- Temps de vol (30%)
- Consommation batterie (30%)
- Qualité d'image / GSD (20%)
- Couverture (20%)

### 3. Simulation de vol

Compare deux modes :
- **Vol continu** : 0.20 m/s, 41.4% batterie ✅
- **Stop-and-Capture** : 116% batterie ❌

## Utilisation

```python
from simulation.lawnmower_planner import LawnmowerPlanner
from simulation.trajectory_optimizer import TrajectoryOptimizer
from simulation.flight_simulator import FlightSimulator

# Planification
planner = LawnmowerPlanner()
plan = planner.plan_rectangular_field(3.5, 2.5, 0.70)

# Optimisation
optimizer = TrajectoryOptimizer()
best = optimizer.optimize_mission(3.5, 2.5)

# Simulation
simulator = FlightSimulator()
result = simulator.simulate_continuous_flight(plan['waypoints'], plan['num_photos'])
```

## Paramètres de mission (parcelle 3.5×2.5m)

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Altitude | 0.70 m | GSD 0.44mm |
| Vitesse | 0.20 m/s | Flou < 0.5px |
| Recouvrement frontal | 75% | Standard |
| Recouvrement latéral | 65% | Standard |
| Nombre de photos | 216 | 12 lignes × 18 photos |
| Distance totale | 39.72 m | - |
| Temps de mission | 3.31 min | - |
| Consommation batterie | 41.4% | Sécurisé |

---

*Module créé le 14 juillet 2026*
*Binôme A - Sous-Projet 1 : Trajectoires*