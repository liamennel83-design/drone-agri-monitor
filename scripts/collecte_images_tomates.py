#!/usr/bin/env python3
"""
Script de collecte et annotation d'images de tomates
pour la validation méthodologique du classificateur de stress hydrique.

Usage :
1. Exécuter ce script pour télécharger des images de test
2. Annoter manuellement les images dans les dossiers healthy/ et stressed/
3. Entraîner le classificateur avec train_stress_classifier.py

Auteur : Fyh - Binôme A - Projet Robotique Autonome
Date : 10 juillet 2026
"""

import os
import sys
import hashlib
import requests
from PIL import Image
from io import BytesIO
import json
from datetime import datetime

class CollecteurImagesTomates:
    """Collecteur d'images de tomates pour annotation"""
    
    def __init__(self, dossier_sortie="data/tomato_dataset"):
        self.dossier_sortie = dossier_sortie
        self.dossier_sain = os.path.join(dossier_sortie, "healthy")
        self.dossier_stresse = os.path.join(dossier_sortie, "stressed")
        
        # Créer les dossiers
        os.makedirs(self.dossier_sain, exist_ok=True)
        os.makedirs(self.dossier_stresse, exist_ok=True)
        
        # Métadonnées
        self.metadata = {
            "date_creation": datetime.now().isoformat(),
            "images_saines": 0,
            "images_stressees": 0,
            "sources": []
        }
    
    def telecharger_image(self, url, categorie, nom_fichier=None):
        """
        Télécharge et sauvegarde une image
        
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
    
    def annoter_image(self, chemin_image, categorie):
        """
        Annote manuellement une image existante
        
        Args:
            chemin_image: Chemin vers l'image source
            categorie: 'healthy' ou 'stressed'
        """
        import shutil
        
        nom_fichier = os.path.basename(chemin_image)
        dossier = self.dossier_sain if categorie == "healthy" else self.dossier_stresse
        destination = os.path.join(dossier, nom_fichier)
        
        shutil.copy2(chemin_image, destination)
        print(f"✅ Annoté : {nom_fichier} → {categorie}")
        
        # Mettre à jour les métadonnées
        if categorie == "healthy":
            self.metadata["images_saines"] += 1
        else:
            self.metadata["images_stressees"] += 1
    
    def sauvegarder_metadata(self):
        """Sauvegarde les métadonnées du dataset"""
        chemin_metadata = os.path.join(self.dossier_sortie, "metadata.json")
        with open(chemin_metadata, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"✅ Métadonnées sauvegardées : {chemin_metadata}")
    
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

def collecter_images_test():
    """Fonction principale de collecte d'images de test"""
    
    print("=" * 60)
    print("COLLECTE D'IMAGES DE TOMATES - VALIDATION MÉTHODOLOGIQUE")
    print("=" * 60)
    print()
    
    # Initialiser le collecteur
    collecteur = CollecteurImagesTomates()
    
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
    print("1. Copiez vos images dans le dossier 'data/tomato_dataset/'")
    print("2. Déplacez les images saines dans 'healthy/'")
    print("3. Déplacez les images stressées dans 'stressed/'")
    print("4. Exécutez 'python scripts/collecte_images_tomates.py' pour vérifier")
    print("5. Entraînez le classificateur avec 'python tools/train_stress_classifier.py'")
    print()

def annoter_images_manuellement(dossier_source, categorie):
    """
    Annote manuellement toutes les images d'un dossier
    
    Args:
        dossier_source: Dossier contenant les images à annoter
        categorie: 'healthy' ou 'stressed'
    """
    collecteur = CollecteurImagesTomates()
    
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
            print("Usage : python collecte_images_tomates.py <dossier_source> <categorie>")
            print("  categorie : 'healthy' ou 'stressed'")
    else:
        # Mode collecte automatique
        collecter_images_test()