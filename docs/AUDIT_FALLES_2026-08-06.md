# AUDIT DES FAILLES — Binôme A · Robot Aérien Autonome
**Date : 6 août 2026 (fin Gantt : 10 août 2026 — J-4)**
Sources : archive Drive `workspace-projet_drone_mega_prompt` (60 fichiers racine + 11 dossiers), dépôt GitHub, rapports S9→S14, retours encadrants, JSON modèles/dataset.

---

## 🚨 P0 — BLOQUANTS PROJET (risque d'échec au jury)

### P0-1. Aucune image réelle : le modèle est validé sur du 100% synthétique
- `data/dataset/metadata.json` : `"type": "synthétique_enrichi"` — 60 images générées par simulation.
- `metadata_parcelle.json` affirme 50 images (25+25) en 500×1000 px, `metadata.json` affirme 60 (30+30), le README dataset documente des noms `sain_XXX/stresse_XXX` alors que les fichiers réels sont `temoin_XXX/test_XXX`, et `models/stress_rf_v1_meta.json` dit `n_samples = 25`.
- **4 chiffres/nommages différents → le jury verra l'incohérence.**
- MEGA_PROMPT tâche 4 (66 photos min. des 24 pots) : non faite. Le rapport S13-S14 contient encore `[ESPACE RÉSERVÉ POUR LES PHOTOS DU BINÔME]`.

**Remédiation** : 1 protocole de collecte accéléré (voir § Plan d'urgence). 1 seul `metadata.json` consolidé, régénéré par script (pas à la main).

### P0-2. La « validation robuste » ne valide rien
- `GUIDE_TEST_VALIDATION_ROBUSTE.md` le dit explicitement : `validation_robuste.py` **régénère un dataset synthétique en mémoire** (`generer_dataset_avec_plantes(n_plantes=12, images_par_plante=5)` → 12 folds). Les features ExG/GRVI ne sont **jamais extraites des images** — ni réelles, ni synthétiques stockées.
- Résultats : LOPO **F1 = 0,366 ± 0,439** (cible exigée : 0,70) ; Bootstrap F1 0,790 [0,571 ; 0,933].
- ❌ Or le rapport S13-S14 et le MEGA_PROMPT classent « Validation robuste du classificateur : **Terminé 100%** ». Un critère raté présenté comme accompli = faute de méthode sanctionnable au jury.
- La confusion finale (TP=25, VN=28, FP=2, FN=5 → F1=0,877) coexiste avec le LOPO à 0,366 sans explication → affaiblit encore la crédibilité si non discutée.

**Remédiation** : pipeline `imagerie/validation_reelle.py` (livré dans ce dépôt) — extraction des features **depuis les images**, `LeaveOneGroupOut` par plante, métriques F1/Kappa/MCC, baseline par seuils (threshold_exg=0.2 / grvi=0.15 déjà présents dans le meta) pour comparer le RandomForest à une règle simple. **Requalifier le statut en « en cours » dans le rapport** et présenter les résultats avec honnêteté (les encadrants ont déjà montré qu'ils valorisent la transparence, c'est une ligne de défense gagnante).

> **Nuance technique (à glisser dans la discussion du rapport)** : le « LOPO F1 = 0,366 » est *lui aussi* un artefact — quand le fold de test contient une seule plante (mono-classe), le F1 binaire est indéfini et vaut 0 par convention ; la moyenne des 12 folds devient bipolaire (0 ou 1, d'où σ = 0,44). La lecture correcte du LOPO est la **matrice de confusion poolée** + l'accuracy équilibrée par fold (implémentées dans `validation_reelle.py`). Le vrai problème n'est donc pas tant le 0,366 que le fait qu'**aucune des deux validations ne s'appuie sur des pixels réels**.

### P0-3. Dérive non résolue → collecte bloquée → tout le ML reste synthétique
- S11-S12 : dérive avant-gauche. S13-S14 : hélices innocentées ; retrait du GPS (5,3 g) → « décollage plus acceptable mais instable » ; cause retenue : déséquilibre du centre de gravité. **Aucune correction mécanique finalisée n'est documentée** (repositionnement, contrepoids, nouveau test 30 s ±10 cm).
- Le critère de validation (stationnaire 30 s à ±10 cm) n'est rapporté nulle part comme atteint.
- Contradiction : GPS physiquement retiré alors que la décision validée par les encadrants est « GPS pour HOME » ; vol indoor sans GPS → le repère HOME GPS disparaît.

**Remédiation** : documenter le centrage (méthode balance + positions, déjà brouillée dans `docs/METHODE_CENTRE_GRAVITE_DRONE.md`) puis un seul test formel avec mesure chiffrée de dérive. Décision binaire : soit GPS remis et équilibré (home), soit GPS abandonné et la phrase « GPS pour HOME » est **retirée du rapport**.

### P0-4. Planning impossible : fin 10 août, travaux planifiés jusqu'à S18
- Rapport S13-S14, « Prochaines étapes » : collecte réelle en S15-S16, entraînement + cartographie + rapport + oral en S17-S18 — soit **4 semaines après la fin officielle du Gantt** (5 mai → 10 août).
- Rapport final annoncé à 70 %. Soutenance imminente.

**Remédiation** : redécoupage en mode dégradé assumé (voir plan d'urgence ci-dessous) : priorité absolue à 1 vol de collecte réelle + carte de stress, quitte à réduire l'ambition MK (1 vol, 24 pots, 1 journée).

### P0-5. Code non livré / non versionné
- Dépôt GitHub (livrable #1 du MEGA_PROMPT) : README + `requirements.txt`, **c'est tout**. `mission/`, `web/`, `resultats/` = README vides dans la backup Drive ; aucun code MicroPython embarqué n'apparaît dans l'archive.
- L'archive Drive contient **15 variantes** de `generer_rapport_*.py`, 4 versions de courbe LiPo, 5 rapports S9-S10… Risque élevé de confusion de version la veille de la remise.
- Cause racine documentée : push GitHub jamais résolu (« Python introuvable dans Git Bash » → 3 scripts .bat `setup_sans_python`, `push_github_v2`…).

**Remédiation** : figer `main` avec code + docs avant tout (ce dépôt). 1 seule version de chaque script, archivage du reste dans `archive/`. NE PAS committer les images dataset (>100 Mo) — les garder sur Drive, dépôt = code + métadonnées + résultats JSON.

---

## ⚠️ P1 — INCOHÉRENCES TECHNIQUES (à corriger avant remise)

| # | Failles | Preuves | Correction |
|---|---------|---------|------------|
| P1-1 | **Signe du GRVI contradictoire** | MEGA_PROMPT + rapport : `(G−R)/(G+R)` ; RESUME_COMPLET tableau features : `(R−G)/(R+G)` | Vérifier `stress_detector.py` (non lisible via Drive — antivirus), unifier partout. Le signe change l'ordre des seuils → faux négatifs si mélangé. |
| P1-2 | **Seuil batterie RTH : 3,65 V vs 3,60 V** | MEGA_PROMPT/rapport : 3,65 V ; RESUME_COMPLET : 3,60 V « validé encadrants » | Une seule valeur (3,65 V ≈ 20%) + **mesure expérimentale en 30 min** (vol stationnaire chronométré, log tension) exigée depuis S11-S12 (« vérifier expérimentalement la courbe »). |
| P1-3 | **Nombre d'images de couverture incohérent** | Rapport : 15 images/parcelle (20% overlap) ; MEGA_PROMPT tâche 4 : 66 min ; Livrable : 96 min | Choisir 1 chiffre justifié : 15 tuiles × 4 vols = 60 images, avec le calcul. |
| P1-4 | **Marqueurs ArUco 30×30 cm *dans* la parcelle 1×2 m** | Rapport §3.4.7 : 4 marqueurs aux coins de la parcelle ; grille pots 3×4 + couloirs 23 cm | Un marqueur de 30 cm représente 2× l'entraxe 32,5 cm → il remplace 1-2 pots. Placer les marqueurs **hors zone de culture** sur cadre périphérique (ou passer à 15 cm au sol en bordure). Ajouter au rapport le calcul de taille angulaire : 30 cm à 0,7 m ≈ 430 px → OK ; à 2,5 m (coin opposé) ≈ 120 px → limite. |
| P1-5 | **Chaîne ArUco irréaliste en fréquence** | Rapport : caméra 30 Hz + Kalman 100 Hz | L'ESP32-S3 ne streame pas du 2 MP à 30 Hz en WiFi (1-2 fps JPEG réaliste, et le WiFi est déjà validé « bande passante suffisante mais résolution/fréquence limitées »). La détection tourne côté station sol → boucle fermée à ~1-2 Hz. Q=0,01/R=0,1 « basé sur IMU/caméra » sans mesure. Recalibrer l'architecture : vision = correction lente, IMU = prophétie rapide ; le dire dans le rapport avant que le jury le dise. |
| P1-6 | **Tableau courbe d'apprentissage ≠ JSON** | Rapport §4.4.4 : tailles 10/20/30/60 ; `validation_robuste_results.json` : [9, 19, 28, 38, 48] | Corriger le tableau (les F1 correspondent aux tailles JSON). |
| P1-7 | **Poussée moteur jamais mesurée** | « T_max = 0,72 N estimé » ; question en suspens depuis 2 rapports | Mesure balance de cuisine + drone à l'envers (30 min). Question piège quasi certaine du jury. |

---

## 🔧 P2 — RENFORT SCIENTIFIQUE (différenciant au jury)

1. **Kappa de Cohen + MCC** : les encadrants ont explicitement salué ces métriques chez Binôme B — les ajouter (déjà dans `validation_reelle.py`).
2. **Baseline par seuils** : montrer RandomForest vs règle ExG>0.2 ∧ GRVI>0.15 — si le RF ne bat pas la règle, le dire (honnêteté) ou le corriger.
3. **Protocole ETc indéfini** : « 50% ETc » sans station météo → définir une opérationnalisation simple (fraction de l'arrosage témoin + humidité sol mesurée 1×/jour) et l'écrire, sinon le protocole agronomique n'est pas reproductible.
4. **Plantes à J14 ?** Le stress démarre à J14 après plantation — vérifier que les 24 pots en seront au bon stade AVANT le 10 août, sinon la collecte réelle est physiquement impossible → scénario B (collecte réduite 1 vol) à arbitrer immédiatement.
5. **Analyse des erreurs « plante 10 »** : 5/5 FN sur une plante synthétique = artefact du générateur, pas un phénomène réel — le formuler ainsi, ou le jury croira à un résultat biologique.
6. Sources ResearchGate non traçables (Romero 2017, Embedded ArUco 2021, « ArUco Recognition 2026 ») : donner DOI/liens directs — 1 lien mort = perte de confiance sur toute la bibliographie.

---

## 📋 PLAN D'URGENCE J-4 → J0

| Jour | Objectif unique | Livrable |
|------|-----------------|----------|
| **Jeu 6/08** | Figer le dépôt (code + audit) ; arbitrage scénario A (vol possible) / B (pas de vol) ; mesure poussée + courbe batterie (1 h) | `main` à jour, 2 mesures chiffrées |
| **Ven 7/08** | Si scénario A : 1 vol stationnaire validé (30 s ±10 cm) + collecte 1 vol complet (15 tuiles × 24 pots) + métadonnées terrain. Si B : protocole « carte alidade/sample manuel » au-dessus des pots à 0,70 m à la main — **images réelles sans résoudre la dérive**, assumé dans le rapport comme « acquisition statique pré-vol » | ≥15-30 images réelles + metadata consolidé |
| **Sam 8/08** | Extraction features réelles → `validation_reelle.py` (LOGO par pot) → retrain `.pkl` honnête + carte de stress de la parcelle + mise à jour rapport (statuts corrigés, incohérences P1 corrigées) | F1/Kappa/MCC réels + heatmap PNG/JSON |
| **Dim 9/08** | Finalisation rapport 20-30 p + slides + script oral ; chiffres cohérents partout (grep des valeurs : 60/50/25, 3,60/3,65, GRVI) | Rapport figé + présentation |
| **Lun 10/08** | Soutenance | — |

> Le scénario B (acquisition statique manuelle) est le filet de sécurité : il débloque le ML réel SANS dépendre de la dérive, et il se présente très bien au jury (« séparation des blocs expérimentaux : imagerie validée au sol, navigation validée séparément, intégration en perspective »).

---

## ✅ Ce qui est déjà solide (à ne pas toucher)
- Justification optique (GSD 0,44 mm/px à 0,70 m, Wx 0,70 m × Wy 0,52 m) — vérifiée, correcte.
- Justification vitesse (flou 0,45 px < 0,5 px à 0,20 m/s) et downwash (v_induit 3,85 m/s).
- Démarche hypothèse→test→réfutation sur la dérive (qualifiée « exemplaire » par l'encadrant).
- Distinction assumée GRVI ≠ NDVI.
- Le passage au LOPO prouve que l'équipe sait reconnaître un F1=1,000 suspect — le narratif « nous avons détecté notre propre fuite de données » est un **argument de jury**, pas une honte, à condition de finir la boucle avec des données réelles.
