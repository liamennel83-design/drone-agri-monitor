# Sources Fiables - Courbe de Décharge LiPo
## Binôme A - Projet Robot Aérien Autonome

---

## ⚠️ Problème des liens précédents

Les liens précédents (Ampow, letusrc) ne fonctionnent plus ou sont instables. Voici les **sources vérifiées et fiables** :

---

## 📚 Sources Vérifiées

### Source 1 : WhaleBattery (2026) - RECOMMANDÉE
**Lien** : https://www.whalebattery.com/blog-detail/lipo-battery-voltage

**Données extraites** :

| Tension (V) | Niveau batterie (%) |
|-------------|---------------------|
| 4.20V | 100% |
| 4.15V | 95% |
| 4.10V | 90% |
| 4.05V | 85% |
| 4.00V | 80% |
| 3.95V | 75% |
| 3.90V | 70% |
| 3.85V | 60% |
| 3.80V | 50% |
| 3.75V | 40% |
| 3.70V | 30% |
| 3.65V | 20% |
| 3.60V | 15% |
| 3.50V | 10% |
| 3.40V | 5% |
| ≤3.30V | 0-2% |

**Note** : "Voltage can be used to estimate battery percentage, but it is not linear and is affected by load, temperature, and battery condition."

---

### Source 2 : HobbyKing (2026)
**Lien** : https://hobbyking.com/blog/lipo-battery-voltage-chart-per-cell

**Points clés** :
- 4.20V/cell = full (standard LiPo)
- 3.7V/cell = nominal label (not a reliable "battery %")
- 3.5V/cell = late-pack warning
- 3.2-3.3V/cell (rebound/resting) = practical stop line

---

### Source 3 : Grepow (2025)
**Lien** : https://www.grepow.com/blog/what-is-the-voltage-of-a-lipo-battery.html

**Points clés** :
- Storage voltage: 3.7V to 3.85V per cell (40-60% capacity)
- Operating range: 3.5V to 4.2V per cell
- "Knee" of discharge curve: rapid voltage drop after 3.5V

---

### Source 4 : usedbytes (2019) - Données mesurées
**Lien** : https://blog.usedbytes.com/2019/03/battery-discharge-profile/

**Points clés** :
- Données réelles mesurées sur batterie LiPo
- "The voltage 'falls of a cliff' at around 3.6V"
- "If you stop at 3.6V, you're at somewhere around 5% charge"

---

### Source 5 : Electronics StackExchange - Formule mathématique
**Lien** : https://electronics.stackexchange.com/questions/435837/calculate-battery-percentage-on-lipo-battery

**Formule empirique** :
```
Battery % = 123 - 123 / (1 + (V/3.7)^80)^0.165
```

---

## 📊 Données Corrigées pour Notre Projet

### Courbe de décharge LiPo 1S 400mAh (Pydrone)

| Capacité (%) | Tension (V) | Action |
|--------------|-------------|--------|
| 100% | 4.20V | Chargée complète |
| 90% | 4.10V | Prête à l'emploi |
| 80% | 4.00V | Zone sûre |
| 70% | 3.90V | Zone sûre |
| 60% | 3.85V | Zone sûre |
| 50% | 3.80V | Nominale |
| 40% | 3.75V | Zone attention |
| 30% | 3.70V | Zone attention |
| **20%** | **3.65V** | **RTH recommandé** |
| **15%** | **3.60V** | **RTH critique** |
| **10%** | **3.50V** | **Urgence** |
| 5% | 3.40V | Danger |
| 0% | 3.30V | Cutoff |

### Seuils de sécurité pour notre projet

| Seuil | Tension | Capacité | Action |
|-------|---------|----------|--------|
| **RTH** | **3.65V** | **~20%** | Return-To-Home automatique |
| **Urgence** | **3.50V** | **~10%** | Atterrissage d'urgence |
| **Critique** | **3.40V** | **~5%** | Arrêt immédiat |

---

## 🔬 Justification des seuils

### RTH à 3.65V (20%)

**Source** : WhaleBattery (2026)
> "3.65V corresponds to approximately 20% battery level"

**Justification** :
- Temps restant : 20% × 480s = 96s ≈ 1.6 min
- Suffisant pour revenir au point HOME (quelques mètres)
- Marge de sécurité pour imprévus

### Urgence à 3.50V (10%)

**Source** : WhaleBattery (2026)
> "3.50V corresponds to approximately 10% battery level"

**Justification** :
- Temps restant : 10% × 480s = 48s ≈ 0.8 min
- Minimum absolu pour atterrir immédiatement
- Évite la décharge profonde (dommages irréversibles)

### Critique à 3.40V (5%)

**Source** : WhaleBattery (2026)
> "3.40V corresponds to approximately 5% battery level"

**Justification** :
- Zone de danger immédiat
- Arrêt obligatoire pour protéger la batterie

---

## 📈 Courbe de décharge typique

```
Tension (V)
    │
4.2 │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
    │
4.0 │────────────────────────────────────────────── 80%
    │
3.8 │────────────────────────────────────────────── 50%
    │
3.65│─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ 20% (RTH)
    │
3.5 │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ 10% (Urgence)
    │                    ╲
3.3 │━━━━━━━━━━━━━━━━━━━━━╲━━━━━━━━━━━━━━━━━━━━━━ 0% (Cutoff)
    │                      ╲
    └────────────────────────────────────────────── Temps
         Début      Plateau      "Knee"        Fin
```

---

## ✅ Sources à utiliser dans le rapport

| Source | Lien | Usage |
|--------|------|-------|
| **WhaleBattery** | https://www.whalebattery.com/blog-detail/lipo-battery-voltage | Courbe de décharge principale |
| **HobbyKing** | https://hobbyking.com/blog/lipo-battery-voltage-chart-per-cell | Guide pratique |
| **Grepow** | https://www.grepow.com/blog/what-is-the-voltage-of-a-lipo-battery.html | Stockage et plages de fonctionnement |
| **usedbytes** | https://blog.usedbytes.com/2019/03/battery-discharge-profile/ | Données mesurées réelles |

---

*Document créé le 14 juillet 2026*
*Binôme A - Sources fiables LiPo*