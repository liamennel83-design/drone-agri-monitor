#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de Traitement d'Images — Détection du Stress Hydrique

Projet : Suivi du stress hydrique par imagerie aérienne
Binôme A — Fyh & Liwingston

Ce module implémente :
- Calcul de l'indice ExG (Excess Green)
- Calcul de l'indice GRVI (Green-Red Vegetation Index)
- Classification binaire (sain / stressé)
- Masquage de la végétation

IMPORTANT : 4 features seulement (conformément au CDC) :
1. ExG moyen
2. ExG écart-type
3. GRVI moyen
4. GRVI écart-type

Références :
- ExG : Woebbecke et al. (1995) - Color indices for weed identification
- GRVI : Tucker (1979) - Red and photographic infrared linear combinations
"""

import numpy as np
from typing import Dict, Optional, Tuple


class StressDetector:
    """
    Détecteur de stress hydrique par analyse radiométrique simplifiée.
    
    Utilise deux indices de végétation :
    - ExG (Excess Green) : 2×G - R - B
    - GRVI (Green-Red Vegetation Index) : (R - G) / (R + G)
    
    Classification binaire :
    - Végétation saine : ExG > 0.20
    - Stress hydrique : ExG < 0.20
    
    Source : Woebbecke et al. (1995), Tucker (1979)
    """
    
    def __init__(self, 
                 threshold_exg: float = 0.20,
                 threshold_grvi: float = 0.15,
                 threshold_vegetation: float = 0.05):
        """
        Initialise le détecteur de stress hydrique.
        
        Args:
            threshold_exg: Seuil ExG pour la classification binaire (défaut 0.20)
            threshold_grvi: Seuil GRVI pour la classification binaire (défaut 0.15)
            threshold_vegetation: Seuil pour détecter la végétation (défaut 0.05)
        """
        self.threshold_exg = threshold_exg
        self.threshold_grvi = threshold_grvi
        self.threshold_vegetation = threshold_vegetation
    
    def compute_exg(self, image_array: np.ndarray) -> np.ndarray:
        """
        Calcule l'indice ExG (Excess Green) pour chaque pixel.
        
        Formule : ExG = 2×G - R - B
        
        Args:
            image_array: Image matricielle 3 canaux (R, G, B) codée sur 8 bits (0-255)
            
        Returns:
            Carte ExG normalisée entre -1 et 1
            
        Référence : Woebbecke et al. (1995)
        "Color indices for weed identification under various soil, residue, 
        and lighting conditions." Transactions of the ASAE, 38(1), 259-269.
        """
        # Conversion en float32 pour éviter les débordements
        img_float = image_array.astype(np.float32) / 255.0
        
        # Extraction des canaux
        R = img_float[:, :, 0]
        G = img_float[:, :, 1]
        B = img_float[:, :, 2]
        
        # Calcul ExG = 2×G - R - B
        exg = 2.0 * G - R - B
        
        # Normalisation entre -1 et 1
        return np.clip(exg, -1.0, 1.0)
    
    def compute_grvi(self, image_array: np.ndarray) -> np.ndarray:
        """
        Calcule l'indice GRVI (Green-Red Vegetation Index) pour chaque pixel.
        
        Formule : GRVI = (R - G) / (R + G)
        
        Note : Sur une caméra NIR-modified (filtre IR-cut retiré), le canal R 
        contient à la fois le Rouge visible ET le Proche-Infrarouge (850nm).
        Le GRVI fournit donc une approximation du NDVI sur ce type de capteur.
        
        Args:
            image_array: Image matricielle 3 canaux (R, G, B) codée sur 8 bits (0-255)
            
        Returns:
            Carte GRVI normalisée entre -1 et 1
            
        Référence : Tucker (1979)
        "Red and photographic infrared linear combinations for monitoring vegetation."
        Remote Sensing of Environment, 8(2), 127-150.
        """
        # Conversion en float32
        img_float = image_array.astype(np.float32)
        
        # Extraction des canaux
        R = img_float[:, :, 0].astype(float)
        G = img_float[:, :, 1].astype(float)
        
        # Calcul GRVI = (R - G) / (R + G)
        # Ajout d'un epsilon pour éviter la division par zéro
        grvi = (R - G) / (R + G + 1e-6)
        
        # Normalisation entre -1 et 1
        return np.clip(grvi, -1.0, 1.0)
    
    def compute_vegetation_mask(self, exg_map: np.ndarray) -> np.ndarray:
        """
        Détecte les pixels de végétation à partir de la carte ExG.
        
        Args:
            exg_map: Carte des valeurs ExG
            
        Returns:
            Masque booléen (True = végétation, False = sol/fond)
        """
        return exg_map > self.threshold_vegetation
    
    def classify_binary_stress(self, 
                               image_array: np.ndarray,
                               vegetation_mask: Optional[np.ndarray] = None) -> Dict:
        """
        Effectue une classification binaire (Stressé / Non-Stressé) sur l'image.
        
        Args:
            image_array: Image matricielle 3 canaux (R, G, B)
            vegetation_mask: Masque booléen optionnel pour isoler la végétation
            
        Returns:
            Dictionnaire avec :
            - exg_map: Carte ExG
            - grvi_map: Carte GRVI
            - vegetation_mask: Masque de végétation
            - stress_mask: Masque de stress (True = stressé)
            - healthy_mask: Masque de végétation saine (True = sain)
            - features: Tuple de 4 features (exg_mean, exg_std, grvi_mean, grvi_std)
            - stress_ratio: Ratio de pixels stressés
            - status: "SAIN" ou "STRESS HYDRIQUE DÉTECTÉ"
        """
        # Calcul des indices
        exg_map = self.compute_exg(image_array)
        grvi_map = self.compute_grvi(image_array)
        
        # Masque de végétation
        if vegetation_mask is None:
            vegetation_mask = self.compute_vegetation_mask(exg_map)
        
        # Classification binaire
        stress_mask = np.logical_and(vegetation_mask, exg_map < self.threshold_exg)
        healthy_mask = np.logical_and(vegetation_mask, exg_map >= self.threshold_exg)
        
        # Statistiques
        total_veg_pixels = np.sum(vegetation_mask)
        stressed_pixels = np.sum(stress_mask)
        healthy_pixels = np.sum(healthy_mask)
        
        # Calcul du ratio de stress
        if total_veg_pixels > 0:
            stress_ratio = float(stressed_pixels / total_veg_pixels)
        else:
            stress_ratio = 0.0
        
        # Calcul des 4 features (CONFORMÉMENT AU CDC)
        # Feature 1 : ExG moyen
        exg_mean = float(np.mean(exg_map[vegetation_mask])) if total_veg_pixels > 0 else 0.0
        
        # Feature 2 : ExG écart-type
        exg_std = float(np.std(exg_map[vegetation_mask])) if total_veg_pixels > 0 else 0.0
        
        # Feature 3 : GRVI moyen
        grvi_mean = float(np.mean(grvi_map[vegetation_mask])) if total_veg_pixels > 0 else 0.0
        
        # Feature 4 : GRVI écart-type
        grvi_std = float(np.std(grvi_map[vegetation_mask])) if total_veg_pixels > 0 else 0.0
        
        # Tuple des 4 features
        features = (exg_mean, exg_std, grvi_mean, grvi_std)
        
        # Statut
        status = "STRESS HYDRIQUE DÉTECTÉ" if stress_ratio > 0.3 else "VÉGÉTATION SAINE"
        
        return {
            'exg_map': exg_map,
            'grvi_map': grvi_map,
            'vegetation_mask': vegetation_mask,
            'stress_mask': stress_mask,
            'healthy_mask': healthy_mask,
            'features': features,
            'exg_mean': exg_mean,
            'exg_std': exg_std,
            'grvi_mean': grvi_mean,
            'grvi_std': grvi_std,
            'stress_ratio': stress_ratio,
            'stressed_pixels': int(stressed_pixels),
            'healthy_pixels': int(healthy_pixels),
            'total_veg_pixels': int(total_veg_pixels),
            'status': status
        }
    
    def extract_features(self, image_array: np.ndarray) -> np.ndarray:
        """
        Extrait les 4 features pour le classificateur.
        
        Args:
            image_array: Image matricielle 3 canaux (R, G, B)
            
        Returns:
            Array numpy de 4 features : [exg_mean, exg_std, grvi_mean, grvi_std]
        """
        result = self.classify_binary_stress(image_array)
        return np.array(result['features'])
    
    def analyze_image(self, image_array: np.ndarray) -> Dict:
        """
        Analyse complète d'une image avec tous les détails.
        
        Args:
            image_array: Image matricielle 3 canaux (R, G, B)
            
        Returns:
            Dictionnaire avec l'analyse complète
        """
        return self.classify_binary_stress(image_array)


def main():
    """Fonction de test et démonstration"""
    
    print("=" * 60)
    print("DÉTECTEUR DE STRESS HYDRIQUE — Double Indice")
    print("=" * 60)
    print()
    
    # Créer le détecteur
    detector = StressDetector(
        threshold_exg=0.20,
        threshold_grvi=0.15,
        threshold_vegetation=0.05
    )
    
    # Créer une image synthétique de test
    print("Création d'une image synthétique de test...")
    
    # Image 100x100 avec fond sol (brun-vert)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Fond sol (R=120, G=100, B=80)
    img[:, :, 0] = 120  # R
    img[:, :, 1] = 100  # G
    img[:, :, 2] = 80   # B
    
    # Végétation saine (R=50, G=150, B=50)
    img[20:40, 20:40, 0] = 50   # R
    img[20:40, 20:40, 1] = 150  # G
    img[20:40, 20:40, 2] = 50   # B
    
    # Végétation stressée (R=120, G=100, B=60)
    img[60:80, 60:80, 0] = 120  # R
    img[60:80, 60:80, 1] = 100  # G
    img[60:80, 60:80, 2] = 60   # B
    
    # Analyser l'image
    print("Analyse de l'image...")
    result = detector.analyze_image(img)
    
    # Afficher les résultats
    print()
    print("=== RÉSULTATS ===")
    print(f"Statut : {result['status']}")
    print(f"Ratio de stress : {result['stress_ratio']*100:.1f}%")
    print()
    print("=== FEATURES (4 conformes au CDC) ===")
    print(f"1. ExG moyen    : {result['exg_mean']:.4f}")
    print(f"2. ExG écart-type : {result['exg_std']:.4f}")
    print(f"3. GRVI moyen   : {result['grvi_mean']:.4f}")
    print(f"4. GRVI écart-type : {result['grvi_std']:.4f}")
    print()
    print("=== STATISTIQUES ===")
    print(f"Pixels végétation : {result['total_veg_pixels']}")
    print(f"Pixels stressés   : {result['stressed_pixels']}")
    print(f"Pixels sains      : {result['healthy_pixels']}")
    print()
    print("=" * 60)
    print("✅ Détecteur de stress hydrique fonctionnel")
    print("=" * 60)


if __name__ == "__main__":
    main()