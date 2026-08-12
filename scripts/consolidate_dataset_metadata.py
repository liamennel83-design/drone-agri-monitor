#!/usr/bin/env python3
"""Reconstruit les métadonnées du dataset à partir des fichiers présents."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

EXTENSIONS = {".jpg", ".jpeg", ".png"}


def images_in(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(path for path in folder.iterdir() if path.suffix.lower() in EXTENSIONS)


def build_metadata(dataset: Path) -> dict:
    healthy = images_in(dataset / "healthy")
    stressed = images_in(dataset / "stressed")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "Drone autonome pour le suivi du stress hydrique",
        "dataset_status": "synthetic_demo" if healthy and stressed else "empty_or_incomplete",
        "images_healthy": len(healthy),
        "images_stressed": len(stressed),
        "total_images": len(healthy) + len(stressed),
        "folders": {"healthy": "healthy", "stressed": "stressed"},
        "note": (
            "Les données actuelles sont des images synthétiques de démonstration. "
            "Les acquisitions réelles doivent être annotées dans plants_mapping.csv."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path("data/dataset"))
    parser.add_argument("--check", action="store_true", help="Affiche les compteurs sans écrire.")
    args = parser.parse_args()

    metadata = build_metadata(args.dataset)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    if args.check:
        return 0

    output = args.dataset / "metadata.json"
    output.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Métadonnées écrites : {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
