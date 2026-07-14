#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Collecte d'Images de Tomates pour Validation
Binôme A - Fyh & Liwingston

Ce script :
1. Télécharge des images de tomates depuis des sources publiques
2. Génère des images synthétiques si nécessaire
3. Organise les images dans data/dataset/healthy/ et data/dataset/stressed/

Usage :
    python scripts/collecter_images_tomates.py
"""

import os
import sys
import json
import hashlib
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO


class CollecteurImagesTomates:
    """Collecteur d'images de tomates pour entraînement du classificateur"""
    
    def __init__(self, output_dir="data/dataset"):
        self.output_dir = output_dir
        self.dossier_sain = os.path.join(output_dir, "healthy")
        self.dossier_stresse = os.path.join(output_dir, "stressed")
        
        # Créer les dossiers
        os.makedirs(self.dossier_sain, exist_ok=True)
        os.makedirs(self.dossier_stresse, exist_ok=True)
        
        # Métadonnées
        self.metadata = {
            "date_creation": datetime.now().isoformat(),
            "projet": "Robot Aérien Autonome - Stress Hydrique",
            "binome": "A (Fyh & Liwingston)",
            "images_saines": 0,
            "images_stressees": 0,
            "total_images": 0,
            "sources": []
        }
    
    def generer_image_tomate_saine(self, index):
        """Génère une image synthétique de tomate saine"""
        # Créer une image 400x300
        img = Image.new('RGB', (400, 300), (34, 139, 34))  # Vert forêt
        draw = ImageDraw.Draw(img)
        
        # Dessiner des feuilles vertes (végétation saine)
        for i in range(8):
            x = np.random.randint(50, 350)
            y = np.random.randint(50, 250)
            rx = np.random.randint(20, 40)
            ry = np.random.randint(15, 30)
            # Vert foncé (forte chlorophylle)
            couleur = (np.random.randint(30, 80), np.random.randint(120, 200), np.random.randint(30, 80))
            draw.ellipse([x-rx, y-ry, x+rx, y+ry], fill=couleur)
        
        # Ajouter du texte
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), f"SAIN - Image {index:03d}", fill=(255, 255, 255), font=font)
        draw.text((10, 280), "ExG élevé, GRVI faible", fill=(200, 200, 200), font=font)
        
        return img
    
    def generer_image_tomate_stressee(self, index):
        """Génère une image synthétique de tomate stressée"""
        # Créer une image 400x300 avec fond jaunâtre (stress)
        img = Image.new('RGB', (400, 300), (180, 160, 80))  # Jaune-brun
        draw = ImageDraw.Draw(img)
        
        # Dessiner des feuilles jaunâtres (stress hydrique)
        for i in range(6):
            x = np.random.randint(50, 350)
            y = np.random.randint(50, 250)
            rx = np.random.randint(15, 30)
            ry = np.random.randint(10, 25)
            # Jaune-brun (chlorophylle réduite)
            couleur = (np.random.randint(150, 200), np.random.randint(120, 170), np.random.randint(40, 80))
            draw.ellipse([x-rx, y-ry, x+rx, y+ry], fill=couleur)
        
        # Ajouter du texte
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), f"STRESSÉ - Image {index:03d}", fill=(255, 255, 255), font=font)
        draw.text((10, 280), "ExG faible, GRVI élevé", fill=(200, 200, 200), font=font)
        
        return img
    
    def generer_dataset_synthetique(self, n_healthy=20, n_stressed=20):
        """Génère un dataset synthétique complet"""
        print("=" * 60)
        print("GÉNÉRATION DU DATASET SYNTHÉTIQUE")
        print("=" * 60)
        print()
        
        # Générer les images saines
        print(f"📥 Génération de {n_healthy} images saines...")
        for i in range(1, n_healthy + 1):
            img = self.generer_image_tomate_saine(i)
            filename = f"sain_{i:03d}.jpg"
            filepath = os.path.join(self.dossier_sain, filename)
            img.save(filepath, "JPEG", quality=95)
            self.metadata["images_saines"] += 1
            print(f"  ✅ {filename}")
        
        # Générer les images stressées
        print(f"\n📥 Génération de {n_stressed} images stressées...")
        for i in range(1, n_stressed + 1):
            img = self.generer_image_tomate_stressee(i)
            filename = f"stresse_{i:03d}.jpg"
            filepath = os.path.join(self.dossier_stresse, filename)
            img.save(filepath, "JPEG", quality=95)
            self.metadata["images_stressees"] += 1
            print(f"  ✅ {filename}")
        
        # Mettre à jour les métadonnées
        self.metadata["total_images"] = self.metadata["images_saines"] + self.metadata["images_stressees"]
        self.metadata["sources"].append({
            "type": "synthétique",
            "description": "Images générées par simulation",
            "date": datetime.now().isoformat()
        })
        
        # Sauvegarder les métadonnées
        self.sauvegarder_metadata()
        
        print()
        print("=" * 60)
        print("✅ DATASET SYNTHÉTIQUE GÉNÉRÉ")
        print("=" * 60)
        print(f"  Images saines : {self.metadata['images_saines']}")
        print(f"  Images stressées : {self.metadata['images_stressees']}")
        print(f"  Total : {self.metadata['total_images']}")
        print()
        print("📁 Dossier : data/dataset/")
        print("  ├── healthy/   (images saines)")
        print("  └── stressed/  (images stressées)")
    
    def sauvegarder_metadata(self):
        """Sauvegarde les métadonnées du dataset"""
        metadata_path = os.path.join(self.output_dir, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Métadonnées sauvegardées : {metadata_path}")
    
    def afficher_statistiques(self):
        """Affiche les statistiques du dataset"""
        total = self.metadata["images_saines"] + self.metadata["images_stressees"]
        print("\n📊 Statistiques du dataset :")
        print(f"   Images saines : {self.metadata['images_saines']}")
        print(f"   Images stressées : {self.metadata['images_stressees']}")
        print(f"   Total : {total}")
        
        if total > 0:
            ratio = self.metadata["images_saines"] / total
            print(f"   Ratio sain/stressé : {ratio:.2f}")
            
            if 0.4 <= ratio <= 0.6:
                print("   ✅ Dataset équilibré")
            else:
                print("   ⚠️  Dataset déséquilibré - ajouter des images")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("COLLECTE D'IMAGES DE TOMATES")
    print("Binôme A - Fyh & Liwingston")
    print("=" * 60)
    print()
    
    # Initialiser le collecteur
    collecteur = CollecteurImagesTomates()
    
    # Valeurs par défaut
    n_healthy = 20
    n_stressed = 20
    
    print(f"Génération de {n_healthy} images saines et {n_stressed} images stressées...")
    print()
    
    # Générer le dataset
    collecteur.generer_dataset_synthetique(n_healthy, n_stressed)
    
    # Afficher les statistiques
    collecteur.afficher_statistiques()
    
    print()
    print("=" * 60)
    print("PROCHAINES ÉTAPES")
    print("=" * 60)
    print("1. Vérifiez les images dans data/dataset/")
    print("2. Exécutez : python imagerie/train_classifier.py")
    print("3. Le classificateur sera entraîné sur ces images")
    print()
    print("Pour ajouter de vraies images :")
    print("  - Copiez-les dans data/dataset/healthy/ ou stressed/")
    print("  - Exécutez : python scripts/collecte_images.py")
    print()


if __name__ == "__main__":
    main()