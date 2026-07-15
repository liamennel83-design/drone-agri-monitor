# Plan de Corrections Finales
## Binome A - Projet Robot Aerien Autonome

---

## 1. Sources LiPo Corrigees

### Sources verifiees et fonctionnelles

| Source | Lien | Usage |
|--------|------|-------|
| WhaleBattery | https://www.whalebattery.com/blog-detail/lipo-battery-voltage | Courbe de décharge principale |
| HobbyKing | https://hobbyking.com/blog/lipo-battery-voltage-chart-per-cell | Guide pratique |
| Grepow | https://www.grepow.com/blog/what-is-the-voltage-of-a-lipo-battery.html | Stockage et plages |
| usedbytes | https://blog.usedbytes.com/2019/03/battery-discharge-profile/ | Données mesurées |

### Données corrigées (WhaleBattery 2026)

| Tension (V) | Capacité (%) | Action |
|-------------|--------------|--------|
| 4.20V | 100% | Chargée complète |
| 4.10V | 90% | Prête à l'emploi |
| 4.00V | 80% | Zone sûre |
| 3.90V | 70% | Zone sûre |
| 3.80V | 50% | Nominale |
| 3.70V | 30% | Zone attention |
| 3.65V | 20% | RTH recommandé |
| 3.50V | 10% | Urgence |
| 3.40V | 5% | Danger |
| ≤3.30V | 0% | Cutoff |

### Seuils de sécurité corrigés

| Seuil | Ancien | Corrigé | Source |
|-------|--------|---------|--------|
| RTH | 3.60V | 3.65V (20%) | WhaleBattery |
| Urgence | 3.50V | 3.50V (10%) | WhaleBattery |
| Critique | 3.30V | 3.40V (5%) | WhaleBattery |

---

## 2. Corrections de Style

### Suppressions
- Tous les tirets cadratins (—) remplacés par des tirets normaux (-)
- Tous les signes génériques supprimés
- Noms propres retirés (seulement "Binôme A")

### Améliorations
- Justifications détaillées pour chaque valeur
- Sources vérifiées avec liens fonctionnels
- Calculs complets et reproductibles

---

## 3. Fichiers à mettre à jour sur GitHub

| Fichier | Action | Priorité |
|---------|--------|----------|
| README.md | Remplacer par version professionnelle | Haute |
| simulation/lawnmower_planner.py | Déjà créé | - |
| simulation/trajectory_optimizer.py | Déjà créé | - |
| simulation/flight_simulator.py | Déjà créé | - |
| simulation/README.md | Déjà créé | - |
| docs/justification_valeurs.md | Mettre à jour sources LiPo | Haute |
| reports/Rapport_Final_Licence_BinomeA_Corrige.docx | Nouveau | Haute |

---

## 4. Prochaines Étapes

1. ✅ Sources LiPo corrigées
2. ✅ Rapport Word corrigé généré
3. 🔄 Mettre à jour les fichiers sur GitHub
4. 🔄 Préparer les livrables pour encadreurs

---

*Document créé le 14 juillet 2026*
*Binôme A - Plan de corrections finales*