#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consolidateur de métadonnées du dataset — Binôme A
==================================================
Corrige la faille P0-1 de l'audit : plusieurs sources contradictoires
(metadata.json: 60 images 30/30 ; metadata_parcelle.json: 50 images 25/25 ;
README: noms sain_XXX/stresse_XXX ; fichiers réels: temoin_XXX/test_XXX ;
meta modèle: n_samples=25).

Ce script REGÉNÈRE data/dataset/metadata.json depuis le contenu réel du
disque : il devient la SEULE source de vérité, à ré-exécuter après chaque
ajout d'images (collecte drone, ajout manuel...).

Usage :  python scripts/consolidate_dataset_metadata.py [--dataset data/dataset]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

EXTS = {".jpg", ".jpeg", ".png"}


def scan(folder: Path) -> dict:
    files = sorted(p for p in folder.glob("*") if p.suffix.lower() in EXTS) if folder.is_dir() else []
    prefixes = {}
    for f in files:
        prefix = f.stem.split("_")[0] if "_" in f.stem else f.stem
        prefixes[prefix] = prefixes.get(prefix, 0) + 1
    return {
        "n_images": len(files),
        "noms_de_fichiers": {"premier": files[0].name if files else None,
                              "dernier": files[-1].name if files else None},
        "prefixes_detectes": prefixes,
        "doublons_noms": len(files) - len({f.name for f in files}),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="data/dataset")
    args = ap.parse_args()
    root = Path(args.dataset)

    healthy = scan(root / "healthy")
    stressed = scan(root / "stressed")
    total = healthy["n_images"] + stressed["n_images"]

    warnings = []
    if healthy["n_images"] != stressed["n_images"]:
        warnings.append(
            f"Classes déséquilibrées: {healthy['n_images']} saines vs "
            f"{stressed['n_images']} stressées -> documenter le rééquilibrage.")
    if total < 60:
        warnings.append(f"{total} images (< 60) : en dessous de la cible collecte (≥60).")
    for label, info in (("healthy", healthy), ("stressed", stressed)):
        if info["doublons_noms"]:
            warnings.append(f"{label}: {info['doublons_noms']} nom(s) en double dans le dossier.")

    metadata = {
        "date_generation": datetime.now().isoformat(),
        "projet": "Robot Aérien Autonome - Stress Hydrique",
        "binome": "A",
        "regenerer_avec": "python scripts/consolidate_dataset_metadata.py",
        "source_unique_de_verite": True,
        "images_saines": healthy["n_images"],
        "images_stressees": stressed["n_images"],
        "total_images": total,
        "detail": {"healthy": healthy, "stressed": stressed},
        "mapping_images_plantes": "plants_mapping.csv (requis pour la validation par plante)",
        "avertissements": warnings,
    }

    out = root / "metadata.json"
    root.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2, ensure_ascii=False)
    print(f"[ok] {out} écrit : {total} images "
          f"({healthy['n_images']} saines / {stressed['n_images']} stressées)")
    for w in warnings:
        print(f"[ALERTE] {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
