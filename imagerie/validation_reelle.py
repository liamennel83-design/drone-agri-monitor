#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation RÉELLE du classificateur de stress hydrique - Binôme A
=================================================================

Pourquoi ce script existe
-------------------------
Les validations précédentes (F1 = 1.000 puis LOPO = 0.366) ont été obtenues
sur des features SYNTHÉTIQUES générées en mémoire
(voir GUIDE_TEST_VALIDATION_ROBUSTE.md : `generer_dataset_avec_plantes`).
Ce script corrige la faille :

  features ExG/GRVI extraites DES IMAGES  ->  validation croisée GROUPÉE
  par plante (Leave-One-Group-Out)       ->  métriques honnêtes (F1, Kappa,
  MCC, IC bootstrap)                     ->  comparaison à une baseline
  par seuils (la règle que le RandomForest doit au moins battre).

Conventions (une seule source de vérité) :
  ExG  = 2*G - R - B                  (Woebbecke et al., 1995)
  GRVI = (R - G) / (R + G)            (convention du code embarqué
           stress_detector.py, lignes 95 et 118 ; végétation saine -> GRVI
           négatif, végétation stressée -> GRVI qui remonte vers 0 et au-delà)
  NOTE : le rapport S13-S14 (paragraphe 4.3) écrit (G - R)/(G + R), signe
  inverse. Le code et le modèle stress_rf_v1.pkl font foi : c'est le
  rapport qui doit être corrigé, pas le code.

Attendu en entrée
-----------------
  data/dataset/healthy/*.jpg        (témoins, arrosage 100 % ETc)
  data/dataset/stressed/*.jpg       (test, 50 % ETc)
  data/dataset/plants_mapping.csv   (optionnel, colonnes: image,plante)
      -> regroupe les images par POT. Sans ce fichier, chaque image est
         son propre groupe (LOGO par image) et une alerte est émise :
         le split par image surestime les performances (fuite intra-plante).

Sortie : models/validation_reelle_results.json  (+ figures si matplotlib OK)

Usage :  python imagerie/validation_reelle.py [--dataset data/dataset]

Binôme A - ESP Antsiranana - août 2026
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

SEED = 42
EXG_THRESHOLD = 0.2     # seuil déjà présent dans stress_rf_v1_meta.json
GRVI_THRESHOLD = 0.15   # idem
MIN_PER_CLASS_WARN = 30


# ---------------------------------------------------------------------------
# 1. Extraction des features DEPUIS LES IMAGES
# ---------------------------------------------------------------------------

def compute_indices(img_bgr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """ExG (float, centré ~0 en [-1, 1] après normalisation) et GRVI ∈ [-1, 1].

    Convention unique, alignée sur stress_detector.py : GRVI = (R - G)/(R + G).
    Les canaux sont normalisés en [0, 1] pour que les seuils 0.2 / 0.15
    (cf. models/stress_rf_v1_meta.json) restent valables.
    """
    img = img_bgr.astype(np.float32) / 255.0
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    exg = (2.0 * g - r - b) / 2.0
    grvi = (r - g) / np.clip(r + g, 1e-6, None)
    return exg, grvi


def extract_features(image_path: Path) -> list[float] | None:
    """4 features : [ExG_moyen, ExG_std, GRVI_moyen, GRVI_std]."""
    import cv2
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    exg, grvi = compute_indices(img)
    return [float(exg.mean()), float(exg.std()),
            float(grvi.mean()), float(grvi.std())]


def load_dataset(dataset_dir: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Charge X (features), y (0=sain, 1=stressé), groups (id plante), noms."""
    mapping = {}
    map_file = dataset_dir / "plants_mapping.csv"
    if map_file.exists():
        with open(map_file, newline="", encoding="utf-8") as fh:
            mapping = {row["image"]: row["plante"] for row in csv.DictReader(fh)}
        print(f"[info] Mapping images->plantes chargé : {len(mapping)} entrées")
    else:
        print("[ALERTE] Pas de plants_mapping.csv -> validation par IMAGE, pas par plante.")
        print("         Résultats surestimés (même plante en train ET test possible).")

    X, y, groups, names = [], [], [], []
    per_class_found = {}
    for label, sub in [(0, "healthy"), (1, "stressed")]:
        files = sorted((dataset_dir / sub).glob("*.jpg")) + sorted((dataset_dir / sub).glob("*.png"))
        per_class_found[sub] = len(files)
        for f in files:
            feats = extract_features(f)
            if feats is None:
                print(f"[warn] Image illisible, ignorée : {f.name}")
                continue
            X.append(feats)
            y.append(label)
            # Priorité au CSV ; sinon on tente d'extraire un id de pot du nom
            # (ex. 'temoin_p03_v2.jpg' -> 'temoin_p03') ; à défaut : le nom du fichier.
            stem = f.stem
            plant_id = mapping.get(f.name, stem.rsplit("_v", 1)[0] if "_v" in stem else stem)
            groups.append(plant_id)
            names.append(f.name)

    print(f"[info] Images trouvées : {per_class_found}")
    for sub, n in per_class_found.items():
        if n < MIN_PER_CLASS_WARN:
            print(f"[ALERTE] Seulement {n} images '{sub}' (<{MIN_PER_CLASS_WARN}) : "
                  "intervalles de confiance larges attendus.")

    return np.asarray(X), np.asarray(y), np.asarray(groups), names


# ---------------------------------------------------------------------------
# 2. Modèles : RandomForest (pipeline) + baseline par seuils
# ---------------------------------------------------------------------------

def make_rf():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    return Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=150, max_depth=6,
                                      min_samples_leaf=3, random_state=SEED)),
    ])


class ThresholdBaseline:
    """Règle experte alignée sur stress_detector.py : stressé si
    ExG_moyen < 0.2 ET GRVI_moyen > 0.15 (GRVI en convention R-G).
    Le RandomForest DOIT battre cette baseline, sinon il n'apporte rien."""
    def fit(self, X, y):
        return self

    def predict(self, X):
        return ((X[:, 0] < EXG_THRESHOLD) & (X[:, 2] > GRVI_THRESHOLD)).astype(int)


# ---------------------------------------------------------------------------
# 3. Métriques
# ---------------------------------------------------------------------------

def metrics(y_true, y_pred) -> dict:
    from sklearn.metrics import (accuracy_score, cohen_kappa_score,
                                 confusion_matrix, f1_score,
                                 matthews_corrcoef, precision_score, recall_score)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "kappa": float(cohen_kappa_score(y_true, y_pred)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "confusion_matrix_tn_fp_fn_tp": cm.ravel().tolist(),
    }


def ci95(values: list[float]) -> list[float]:
    if len(values) < 2:
        return [float(values[0]), float(values[0])] if values else [0.0, 0.0]
    lo, hi = np.percentile(values, [2.5, 97.5])
    return [float(lo), float(hi)]


def logo_validation(X, y, groups, factory) -> dict:
    """Leave-One-Group-Out : chaque plante (ou image à défaut) testée à part entière.
    => aucune fuite intra-plante entre train et test.

    POINT MÉTHODOLOGIQUE IMPORTANT (explique aussi l'ancien "LOPO F1 = 0.366") :
    quand le fold de test = UNE plante, y_test est mono-classe et le F1 binaire
    est indéfini (0 par convention) -> la moyenne des F1 par fold est dégénérée
    et bipolaire (0 ou 1). La lecture principale doit être les métriques
    POOLÉES (prédictions agrégées sur tous les folds). Par fold on rapporte
    l'accuracy équilibrée (définie même mono-classe) et le F1 seulement si le
    fold contient les deux classes."""
    from sklearn.metrics import balanced_accuracy_score, f1_score
    from sklearn.model_selection import LeaveOneGroupOut
    logo = LeaveOneGroupOut()
    y_pred_all = np.zeros_like(y)
    fold_bacc, fold_f1 = [], []
    for train_idx, test_idx in logo.split(X, y, groups):
        model = factory()
        model.fit(X[train_idx], y[train_idx])
        pred = model.predict(X[test_idx])
        y_pred_all[test_idx] = pred
        fold_bacc.append(float(balanced_accuracy_score(y[test_idx], pred)))
        if len(np.unique(y[test_idx])) == 2:   # F1 défini seulement si 2 classes
            fold_f1.append(float(f1_score(y[test_idx], pred, zero_division=0)))
    pooled = metrics(y, y_pred_all)
    return {
        "n_folds": len(fold_bacc),
        "accuracy_equilibree_folds_mean": float(np.mean(fold_bacc)),
        "accuracy_equilibree_folds_std": float(np.std(fold_bacc)),
        "f1_folds_mean(si_defini)": float(np.mean(fold_f1)) if fold_f1 else None,
        "metriques_global(poolées)__LECTURE_PRINCIPALE": pooled,
    }


def bootstrap_grouped(X, y, groups, factory, n_iter=500) -> dict:
    """Bootstrap par GROUPES (on rééchantillonne les plantes, pas les images).
    Test = plantes hors échantillon (out-of-bag) : pas de double emploi."""
    rng = np.random.default_rng(SEED)
    uniq = np.unique(groups)
    f1s, kappas, mccs, accs = [], [], [], []
    for _ in range(n_iter):
        sampled = rng.choice(uniq, size=len(uniq), replace=True)
        oob = ~np.isin(groups, sampled)
        if oob.sum() == 0 or len(np.unique(y[oob])) < 2:
            continue
        tr = np.isin(groups, sampled)
        model = factory()
        model.fit(X[tr], y[tr])
        m = metrics(y[oob], model.predict(X[oob]))
        f1s.append(m["f1"]); kappas.append(m["kappa"])
        mccs.append(m["mcc"]); accs.append(m["accuracy"])
    return {
        "n_iterations": len(f1s),
        "f1": {"mean": float(np.mean(f1s)), "ci95": ci95(f1s)},
        "accuracy": {"mean": float(np.mean(accs)), "ci95": ci95(accs)},
        "kappa": {"mean": float(np.mean(kappas)), "ci95": ci95(kappas)},
        "mcc": {"mean": float(np.mean(mccs)), "ci95": ci95(mccs)},
    }


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="data/dataset", help="dossier dataset")
    ap.add_argument("--out", default="models/validation_reelle_results.json")
    ap.add_argument("--bootstrap", type=int, default=500)
    args = ap.parse_args()

    dataset_dir = Path(args.dataset)
    if not (dataset_dir / "healthy").exists() or not (dataset_dir / "stressed").exists():
        print(f"[FATAL] Structure absente : {dataset_dir}/healthy et stressed/ requis.",
              file=sys.stderr)
        return 2

    X, y, groups, _ = load_dataset(dataset_dir)
    if len(X) < 10:
        print(f"[FATAL] {len(X)} images exploitables : collecte réelle insuffisante.",
              file=sys.stderr)
        return 2

    results = {
        "date": datetime.now().isoformat(),
        "conventions": {
            "ExG": "2*G - R - B (canaux normalisés [0,1], sortie divisée par 2)",
            "GRVI": "(R - G) / (R + G)   <- convention du code stress_detector.py (signe unifié)",
        },
        "dataset": {
            "n_images": int(len(X)),
            "n_saines": int((y == 0).sum()),
            "n_stressees": int((y == 1).sum()),
            "n_groupes(plantes)": int(len(np.unique(groups))),
            "split": "Leave-One-Group-Out (par plante si plants_mapping.csv fourni)",
        },
        "seuils_baseline": {"exg": EXG_THRESHOLD, "grvi": GRVI_THRESHOLD},
    }

    print("\n=== 1/3 Baseline par seuils (référence minimale) ===")
    results["baseline_seuils"] = {
        "logo": logo_validation(X, y, groups, ThresholdBaseline),
    }
    print("  F1 (poolé) :", results["baseline_seuils"]["logo"]
          ["metriques_global(poolées)__LECTURE_PRINCIPALE"]["f1"])

    print("\n=== 2/3 RandomForest - validation L.O.Group.Out ===")
    results["random_forest"] = {
        "hyperparametres": {"n_estimators": 150, "max_depth": 6,
                            "min_samples_leaf": 3, "seed": SEED},
        "logo": logo_validation(X, y, groups, make_rf),
    }
    logo_rf = results["random_forest"]["logo"]
    pooled = logo_rf["metriques_global(poolées)__LECTURE_PRINCIPALE"]
    print(f"  F1 poolé = {pooled['f1']:.3f} | acc. équilibrée/fold = "
          f"{logo_rf['accuracy_equilibree_folds_mean']:.3f} ± "
          f"{logo_rf['accuracy_equilibree_folds_std']:.3f} (folds={logo_rf['n_folds']})")
    print(f"  Kappa = {pooled['kappa']:.3f} | MCC = {pooled['mcc']:.3f} | "
          f"matrice TN/FP/FN/TP = {pooled['confusion_matrix_tn_fp_fn_tp']}")

    print(f"\n=== 3/3 Bootstrap groupé ({args.bootstrap} itérations) ===")
    results["random_forest"]["bootstrap_groupe"] = bootstrap_grouped(
        X, y, groups, make_rf, n_iter=args.bootstrap)
    bg = results["random_forest"]["bootstrap_groupe"]
    print(f"  F1 = {bg['f1']['mean']:.3f} IC95 {bg['f1']['ci95']}")

    verdict_f1 = pooled["f1"]
    results["verdict"] = {
        "critere_projet": "F1 > 0.70 (LOPO/par plante)",
        "f1_obtenu": round(verdict_f1, 3),
        "critere_atteint": bool(verdict_f1 > 0.70),
        "honnêteté": "Résultat calculé sur IMAGES RÉELLES avec split par GROUPE. "
                     "Toute valeur antérieure (1.000 ; 0.366) venait de features synthétiques.",
    }
    print(f"\n>>> Verdict : F1={verdict_f1:.3f} "
          f"({'OK' if verdict_f1 > 0.70 else 'SOUS LE CRITÈRE 0.70 - à traiter dans le rapport'})")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print(f"\n[ok] Résultats écrits : {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
