#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Collecte et Annotation d'Images de Tomates

Projet : Suivi du stress hydrique par imagerie aérienne
Binôme A - Fyh & Liwingston

Ce script permet de :
- Télécharger des images de tomates depuis le web
- Annoter manuellement les images (sain/stressé)
- Vérifier la qualité du dataset
- Générer des métadonnées

Usage :
1. Collecter des images : python scripts/collecte_images.py
2. Annoter manuellement : python scripts/collecte_images.py <dossier> <categorie>
"""

import os
import sys
import json
import hashlib
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Optional


class TomatoImageCollector:
    """
    Collecteur d'images de tomates pour l'entraînement du classificateur.
    
    Structure attendue :
    data/dataset/
    ├── healthy/          # Images de tomates saines
    │   ├── sain_001.jpg
    │   └── ...
    ├── stressed/         # Images de tomates stressées
    │   ├── stresse_001.jpg
    │   └── ...
    └── metadata.json     # Métadonnées du dataset
    """
    
    def __init__(self, output_dir: str = "data/dataset"):
        """
        Initialise le collecteur d'images.
        
        Args:
            output_dir: Dossier de sortie pour le dataset
        """
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
            "sources": [],
            "annotations": []
        }
    
    def telecharger_image(self, url: str, categorie: str, 
                         nom_fichier: Optional[str] = None) -> Optional[str]:
        """
        Télécharge et sauvegarde une image.
        
        Args:
            url: URL de l'image
            categorie: 'healthy' ou 'stressed'
            nom_fichier: Nom personnalisé (optionnel)
            
        Returns:
            Chemin du fichier sauvegardé ou None
        """
        try:
            # Télécharger l'image
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                print(f"❌ Erreur HTTP {response.status_code}")
                return None
            
            # Ouvrir l'image
            img = Image.open(BytesIO(response.content))
            
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Générer un nom de fichier unique
            if nom_fichier is None:
                hash_url = hashlib.md5(url.encode()).hexdigest()[:8]
                nom_fichier = f"tomate_{categorie}_{hash_url}.jpg"
            
            # Sauvegarder
            dossier = self.dossier_sain if categorie == "healthy" else self.dossier_stresse
            chemin = os.path.join(dossier, nom_fichier)
            img.save(chemin, "JPEG", quality=95)
            
            # Mettre à jour les métadonnées
            if categorie == "healthy":
                self.metadata["images_saines"] += 1
            else:
                self.metadata["images_stressees"] += 1
            
            self.metadata["total_images"] = (
                self.metadata["images_saines"] + self.metadata["images_stressees"]
            )
            
            self.metadata["sources"].append({
                "url": url,
                "categorie": categorie,
                "fichier": nom_fichier,
                "date": datetime.now().isoformat()
            })
            
            print(f"✅ Sauvegardé : {nom_fichier} ({categorie})")
            return chemin
            
        except Exception as e:
            print(f"❌ Erreur téléchargement : {e}")
            return None
    
    def annoter_image(self, chemin_image: str, categorie: str) -> bool:
        """
        Annote manuellement une image existante.
        
        Args:
            chemin_image: Chemin vers l'image source
            categorie: 'healthy' ou 'stressed'
            
        Returns:
            True si succès, False sinon
        """
        import shutil
        
        if not os.path.exists(chemin_image):
            print(f"❌ Fichier non trouvé : {chemin_image}")
            return False
        
        nom_fichier = os.path.basename(chemin_image)
        dossier = self.dossier_sain if categorie == "healthy" else self.dossier_stresse
        destination = os.path.join(dossier, nom_fichier)
        
        shutil.copy2(chemin_image, destination)
        
        # Mettre à jour les métadonnées
        if categorie == "healthy":
            self.metadata["images_saines"] += 1
        else:
            self.metadata["images_stressees"] += 1
        
        self.metadata["total_images"] = (
            self.metadata["images_saines"] + self.metadata["images_stressees"]
        )
        
        self.metadata["annotations"].append({
            "fichier": nom_fichier,
            "categorie": categorie,
            "date": datetime.now().isoformat()
        })
        
        print(f"✅ Annoté : {nom_fichier} → {categorie}")
        return True
    
    def sauvegarder_metadata(self) -> str:
        """
        Sauvegarde les métadonnées du dataset.
        
        Returns:
            Chemin du fichier de métadonnées
        """
        chemin_metadata = os.path.join(self.output_dir, "metadata.json")
        with open(chemin_metadata, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"✅ Métadonnées sauvegardées : {chemin_metadata}")
        return chemin_metadata
    
    def afficher_statistiques(self) -> None:
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
    
    def verifier_qualite(self) -> Dict:
        """
        Vérifie la qualité du dataset.
        
        Returns:
            Dictionnaire avec les résultats de vérification
        """
        resultats = {
            "total_images": 0,
            "images_saines": 0,
            "images_stressees": 0,
            "images_corrompues": 0,
            "formats_valides": True,
            "equilibre": False
        }
        
        # Vérifier les images saines
        for fichier in os.listdir(self.dossier_sain):
            if fichier.endswith(('.jpg', '.jpeg', '.png')):
                chemin = os.path.join(self.dossier_sain, fichier)
                try:
                    img = Image.open(chemin)
                    img.verify()
                    resultats["images_saines"] += 1
                except:
                    resultats["images_corrompues"] += 1
        
        # Vérifier les images stressées
        for fichier in os.listdir(self.dossier_stresse):
            if fichier.endswith(('.jpg', '.jpeg', '.png')):
                chemin = os.path.join(self.dossier_stresse, fichier)
                try:
                    img = Image.open(chemin)
                    img.verify()
                    resultats["images_stressees"] += 1
                except:
                    resultats["images_corrompues"] += 1
        
        resultats["total_images"] = resultats["images_saines"] + resultats["images_stressees"]
        
        # Vérifier l'équilibre
        if resultats["total_images"] > 0:
            ratio = resultats["images_saines"] / resultats["total_images"]
            resultats["equilibre"] = 0.4 <= ratio <= 0.6
        
        return resultats


def collecter_images_test() -> None:
    """Fonction principale de collecte d'images de test"""
    
    print("=" * 60)
    print("COLLECTE D'IMAGES DE TOMATES - VALIDATION MÉTHODOLOGIQUE")
    print("=" * 60)
    print()
    
    # Initialiser le collecteur
    collecteur = TomatoImageCollector()
    
    # URLs d'exemple (à remplacer par de vraies URLs)
    # Note : Ces URLs sont des exemples - à remplacer par des images réelles
    urls_saines = [
        # Ajouter ici les URLs d'images de tomates saines
        # "https://example.com/tomato_healthy_1.jpg",
        # "https://example.com/tomato_healthy_2.jpg",
    ]
    
    urls_stressees = [
        # Ajouter ici les URLs d'images de tomates stressées
        # "https://example.com/tomato_stressed_1.jpg",
        # "https://example.com/tomato_stressed_2.jpg",
    ]
    
    # Télécharger les images saines
    print("📥 Téléchargement des images saines...")
    for i, url in enumerate(urls_saines[:25], 1):  # Max 25 images
        print(f"  [{i}/{min(25, len(urls_saines))}] ", end="")
        collecteur.telecharger_image(url, "healthy", f"sain_{i:03d}.jpg")
    
    # Télécharger les images stressées
    print("\n📥 Téléchargement des images stressées...")
    for i, url in enumerate(urls_stressees[:25], 1):  # Max 25 images
        print(f"  [{i}/{min(25, len(urls_stressees))}] ", end="")
        collecteur.telecharger_image(url, "stressed", f"stresse_{i:03d}.jpg")
    
    # Sauvegarder les métadonnées
    collecteur.sauvegarder_metadata()
    
    # Afficher les statistiques
    collecteur.afficher_statistiques()
    
    print("\n" + "=" * 60)
    print("INSTRUCTIONS POUR L'ANNOTATION MANUELLE :")
    print("=" * 60)
    print("1. Copiez vos images dans le dossier 'data/dataset/'")
    print("2. Déplacez les images saines dans 'healthy/'")
    print("3. Déplacez les images stressées dans 'stressed/'")
    print("4. Exécutez 'python scripts/collecte_images.py' pour vérifier")
    print("5. Entraînez le classificateur avec 'python imagerie/train_classifier.py'")
    print()


def annoter_images_manuellement(dossier_source: str, categorie: str) -> None:
    """
    Annote manuellement toutes les images d'un dossier.
    
    Args:
        dossier_source: Dossier contenant les images à annoter
        categorie: 'healthy' ou 'stressed'
    """
    collecteur = TomatoImageCollector()
    
    if not os.path.exists(dossier_source):
        print(f"❌ Dossier source non trouvé : {dossier_source}")
        return
    
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    fichiers = [f for f in os.listdir(dossier_source) 
                if os.path.splitext(f)[1].lower() in extensions]
    
    print(f"📁 Annotation de {len(fichiers)} images dans '{dossier_source}'...")
    
    for i, fichier in enumerate(fichiers, 1):
        chemin = os.path.join(dossier_source, fichier)
        print(f"  [{i}/{len(fichiers)}] ", end="")
        collecteur.annoter_image(chemin, categorie)
    
    collecteur.sauvegarder_metadata()
    collecteur.afficher_statistiques()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mode annotation manuelle
        if len(sys.argv) == 3:
            dossier_source = sys.argv[1]
            categorie = sys.argv[2]
            if categorie not in ["healthy", "stressed"]:
                print("❌ Catégorie invalide. Utilisez 'healthy' ou 'stressed'")
                sys.exit(1)
            annoter_images_manuellement(dossier_source, categorie)
        else:
            print("Usage : python collecte_images.py <dossier_source> <categorie>")
            print("  categorie : 'healthy' ou 'stressed'")
    else:
        # Mode collecte automatique
        collecter_images_test()