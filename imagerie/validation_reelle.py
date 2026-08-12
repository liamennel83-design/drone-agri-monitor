#!/usr/bin/env python3
"""Validation par plant des images annotées du projet.

Le script ne crée pas de données synthétiques. Il extrait quatre variables depuis les
images présentes, sépare les données avec LeaveOneGroupOut et écrit des métriques
sur les prédictions regroupées. Le groupe est l'identifiant stable du pot.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, matthews_corrcoef
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from stress_detector import StressDetector

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
LABELS = {"healthy": 0, "stressed": 1}


def read_mapping(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        return {row["image"]: row for row in csv.DictReader(handle) if row.get("image")}


def load_samples(dataset: Path, mapping: dict[str, dict[str, str]]):
    detector = StressDetector()
    features, labels, groups, records = [], [], [], []

    for folder_name, label in LABELS.items():
        folder = dataset / folder_name
        for image_path in sorted(folder.iterdir()) if folder.exists() else []:
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            image_bgr = cv2.imread(str(image_path))
            if image_bgr is None:
                print(f"Image ignorée, lecture impossible : {image_path}")
                continue
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            annotation = mapping.get(image_path.name, {})
            annotated_label = annotation.get("label", folder_name).strip().lower()
            if annotated_label and annotated_label != folder_name:
                raise ValueError(
                    f"Annotation incohérente pour {image_path.name} : "
                    f"dossier={folder_name}, label={annotated_label}"
                )
            plant_id = annotation.get("plant_id", "").strip()
            if not plant_id:
                plant_id = image_path.stem
            values = detector.extract_features(image_rgb)
            features.append(values)
            labels.append(label)
            groups.append(plant_id)
            records.append({"image": image_path.name, "plant_id": plant_id, "label": folder_name})

    if not features:
        raise ValueError("Aucune image valide trouvée dans healthy/ et stressed/.")
    return np.asarray(features), np.asarray(labels), np.asarray(groups), records


def evaluate_logo(X: np.ndarray, y: np.ndarray, groups: np.ndarray) -> dict:
    if len(np.unique(groups)) < 2:
        raise ValueError("Au moins deux plant_id distincts sont nécessaires.")
    if len(np.unique(y)) < 2:
        raise ValueError("Les deux classes healthy et stressed sont nécessaires.")

    logo = LeaveOneGroupOut()
    prediction = np.full(shape=len(y), fill_value=-1, dtype=int)
    valid_folds = 0
    for train_idx, test_idx in logo.split(X, y, groups):
        if len(np.unique(y[train_idx])) < 2:
            continue
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestClassifier(
                n_estimators=200,
                max_depth=6,
                min_samples_leaf=2,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            )),
        ])
        model.fit(X[train_idx], y[train_idx])
        prediction[test_idx] = model.predict(X[test_idx])
        valid_folds += 1

    usable = prediction >= 0
    if not np.all(usable):
        raise ValueError("Certains plis ne contiennent pas les deux classes à l'entraînement.")

    return {
        "method": "LeaveOneGroupOut par plant_id",
        "n_folds": valid_folds,
        "f1_pooled": round(float(f1_score(y, prediction, zero_division=0)), 4),
        "accuracy_pooled": round(float(accuracy_score(y, prediction)), 4),
        "kappa_pooled": round(float(cohen_kappa_score(y, prediction)), 4),
        "mcc_pooled": round(float(matthews_corrcoef(y, prediction)), 4),
        "predictions": prediction.tolist(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validation d'images par séparation des plants.")
    parser.add_argument("--dataset", type=Path, default=Path("data/dataset"))
    parser.add_argument("--mapping", type=Path, default=Path("data/dataset/plants_mapping.csv"))
    parser.add_argument("--output", type=Path, default=Path("models/validation_reelle_results.json"))
    args = parser.parse_args()

    mapping = read_mapping(args.mapping)
    X, y, groups, records = load_samples(args.dataset, mapping)
    result = evaluate_logo(X, y, groups)
    result.update({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_images": int(len(y)),
        "n_healthy": int(np.sum(y == 0)),
        "n_stressed": int(np.sum(y == 1)),
        "n_plants": int(len(np.unique(groups))),
        "mapping_entries": len(mapping),
        "records": records,
        "features": ["exg_mean", "exg_std", "grvi_mean", "grvi_std"],
        "grvi_formula": "(R - G) / (R + G)",
        "limitation": (
            "Un plant_id absent est remplacé par le nom du fichier. Dans ce cas, "
            "la séparation par plant n'est pas démontrée si plusieurs vues du même plant existent."
        ),
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in result if key not in {"records", "predictions"}}, indent=2, ensure_ascii=False))
    print(f"Résultats écrits : {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
