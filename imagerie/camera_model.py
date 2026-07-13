#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modélisation Optique et Photogrammétrique — Caméra OV2640 (Pydrone)

Projet : Suivi du stress hydrique par imagerie aérienne
Binôme A — Fyh & Liwingston

Ce module calcule :
- Le Ground Sampling Distance (GSD) en fonction de l'altitude
- L'emprise au sol (footprint) de chaque image
- La contrainte de flou cinétique (motion blur)
- L'espacement optimal entre les photos

Références :
- Woebbecke et al. (1995) - Color indices for weed identification
- Tucker (1979) - Red and photographic infrared linear combinations
- Rouse et al. (1974) - Monitoring vegetation systems
"""

import numpy as np
from typing import Tuple, Dict


class CameraOV2640:
    """
    Modélisation physique de la caméra OV2640 2MP NIR-modified.
    
    Paramètres par défaut configurés pour le capteur OV2640 avec :
    - Filtre IR-cut retiré (Night Vision)
    - Résolution 1600×1200 (UXGA)
    - Focale 3.6mm
    - Taille pixel 2.24µm
    
    Source : Datasheet OV2640 (OmniVision)
    """
    
    def __init__(self,
                 resolution_x: int = 1600,
                 resolution_y: int = 1200,
                 pixel_pitch_m: float = 2.24e-6,
                 focal_length_m: float = 3.6e-3,
                 fov_deg: float = 66.0):
        """
        Initialise le modèle de la caméra OV2640.
        
        Args:
            resolution_x: Nombre de pixels en largeur (1600 pour UXGA)
            resolution_y: Nombre de pixels en hauteur (1200 pour UXGA)
            pixel_pitch_m: Taille d'un pixel en mètres (2.24µm pour OV2640)
            focal_length_m: Distance focale de l'objectif en mètres (3.6mm)
            fov_deg: Champ de vision en degrés (66° pour notre objectif)
            
        Source : Datasheet OV2640 - Seeed Studio
        Lien : https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/OV2640-datasheet.pdf
        """
        # Résolution du capteur
        self.nx = resolution_x
        self.ny = resolution_y
        
        # Paramètres physiques
        self.pixel_pitch = pixel_pitch_m  # 2.24µm
        self.focal_length = focal_length_m  # 3.6mm
        
        # Dimensions physiques du capteur
        self.sensor_width = self.nx * self.pixel_pitch   # ~3.584mm
        self.sensor_height = self.ny * self.pixel_pitch  # ~2.688mm
        
        # Angles de champ (FOV)
        self.fov_x_rad = 2.0 * np.arctan(self.sensor_width / (2.0 * self.focal_length))
        self.fov_y_rad = 2.0 * np.arctan(self.sensor_height / (2.0 * self.focal_length))
        self.fov_x_deg = np.degrees(self.fov_x_rad)
        self.fov_y_deg = np.degrees(self.fov_y_rad)
        
        # Vérification avec le FOV annoncé
        self.fov_declared = fov_deg
        
    def get_gsd(self, altitude_m: float) -> float:
        """
        Calcule le Ground Sampling Distance (GSD) pour une altitude donnée.
        
        Le GSD représente la taille au sol d'un pixel de l'image.
        
        Formule : GSD = (pixel_pitch × altitude) / focal_length
        
        Args:
            altitude_m: Hauteur de vol au-dessus du sol (en mètres)
            
        Returns:
            GSD en mètres/pixel
            
        Exemple :
            À H = 0.70m : GSD = (2.24e-6 × 0.70) / 3.6e-3 = 0.435 mm/pixel
            
        Source : Formule photogrammétrique standard
        """
        return (self.pixel_pitch * altitude_m) / self.focal_length
    
    def get_footprint(self, altitude_m: float) -> Tuple[float, float]:
        """
        Calcule l'emprise au sol (largeur Wx, hauteur Wy) de l'image.
        
        Formule : Wx = (sensor_width × altitude) / focal_length
        
        Args:
            altitude_m: Hauteur de vol au-dessus du sol (en mètres)
            
        Returns:
            Tuple (largeur_sol_m, hauteur_sol_m) en mètres
            
        Exemple :
            À H = 0.70m : Wx = (3.584mm × 0.70m) / 3.6mm = 0.70m
                          Wy = (2.688mm × 0.70m) / 3.6mm = 0.52m
        """
        wx = (self.sensor_width * altitude_m) / self.focal_length
        wy = (self.sensor_height * altitude_m) / self.focal_length
        return wx, wy
    
    def compute_spacing(self, altitude_m: float, 
                       forward_overlap: float = 0.75,
                       side_overlap: float = 0.65) -> Tuple[float, float]:
        """
        Calcule la distance entre les photos successives et l'espacement inter-trace.
        
        Args:
            altitude_m: Hauteur de vol en mètres
            forward_overlap: Taux de recouvrement frontal (0 à 1)
            side_overlap: Taux de recouvrement latéral (0 à 1)
            
        Returns:
            Tuple (dx_photo_m, dy_intertrace_m) en mètres
            
        Exemple :
            À H = 0.70m avec 75% frontal et 65% latéral :
            dx = 0.70 × (1 - 0.75) = 0.175m
            dy = 0.52 × (1 - 0.65) = 0.182m
        """
        wx, wy = self.get_footprint(altitude_m)
        dx_photo = wx * (1.0 - forward_overlap)
        dy_intertrace = wy * (1.0 - side_overlap)
        return dx_photo, dy_intertrace
    
    def get_max_flight_speed(self, altitude_m: float,
                            exposure_time_s: float = 1.0/1000.0,
                            blur_limit_px: float = 0.5) -> float:
        """
        Calcule la vitesse de vol maximale autorisée pour éviter le flou cinétique.
        
        Le flou cinétique (motion blur) est causé par le mouvement du drone
        pendant le temps de pose de la caméra.
        
        Formule : v_max = (GSD × blur_limit) / exposure_time
        
        Args:
            altitude_m: Hauteur de vol (m)
            exposure_time_s: Temps de pose de l'obturateur (ex: 1/1000s)
            blur_limit_px: Flou maximal toléré en fraction de pixel (défaut 0.5px)
            
        Returns:
            Vitesse maximale en m/s
            
        Exemple :
            À H = 0.70m avec pose 1/1000s et 0.5px :
            GSD = 0.435mm/pixel
            v_max = (0.435e-3 × 0.5) / (1/1000) = 0.218 m/s
            
        Source : Règle photogrammétrique du 1/2 pixel
        """
        gsd = self.get_gsd(altitude_m)
        v_max = (gsd * blur_limit_px) / exposure_time_s
        return v_max
    
    def compute_mission_params(self, field_length_m: float,
                              field_width_m: float,
                              altitude_m: float,
                              flight_speed_ms: float = 0.20) -> Dict:
        """
        Calcule les paramètres complets de mission pour une parcelle donnée.
        
        Args:
            field_length_m: Longueur de la parcelle (m)
            field_width_m: Largeur de la parcelle (m)
            altitude_m: Altitude de vol (m)
            flight_speed_ms: Vitesse de vol (m/s)
            
        Returns:
            Dictionnaire avec tous les paramètres de mission
        """
        # Paramètres optiques
        gsd = self.get_gsd(altitude_m)
        wx, wy = self.get_footprint(altitude_m)
        dx, dy = self.compute_spacing(altitude_m)
        v_max = self.get_max_flight_speed(altitude_m)
        
        # Paramètres de mission
        nb_photos_x = max(1, int(np.ceil(field_length_m / dx)))
        nb_photos_y = max(1, int(np.ceil(field_width_m / dy)))
        nb_photos_total = nb_photos_x * nb_photos_y
        
        # Distance et temps de vol
        distance_totale = nb_photos_y * field_length_m + (nb_photos_y - 1) * dy
        temps_vol = distance_totale / flight_speed_ms
        
        # Consommation batterie (8 min = 480s)
        autonomie_s = 8 * 60
        batterie_pct = (temps_vol / autonomie_s) * 100
        
        return {
            'gsd_mm': gsd * 1000,
            'footprint_wx_m': wx,
            'footprint_wy_m': wy,
            'spacing_dx_m': dx,
            'spacing_dy_m': dy,
            'nb_photos_x': nb_photos_x,
            'nb_photos_y': nb_photos_y,
            'nb_photos_total': nb_photos_total,
            'distance_totale_m': distance_totale,
            'temps_vol_s': temps_vol,
            'temps_vol_min': temps_vol / 60,
            'batterie_pct': batterie_pct,
            'vitesse_max_ms': v_max,
            'vitesse_consigne_ms': flight_speed_ms,
            'altitude_m': altitude_m
        }
    
    def summary(self, altitude_m: float) -> str:
        """
        Génère un résumé textuel des performances de la caméra à l'altitude H.
        
        Args:
            altitude_m: Hauteur de vol en mètres
            
        Returns:
            Chaîne de caractères avec le résumé
        """
        gsd_cm = self.get_gsd(altitude_m) * 100.0
        wx, wy = self.get_footprint(altitude_m)
        dx, dy = self.compute_spacing(altitude_m)
        v_max = self.get_max_flight_speed(altitude_m)
        
        lines = [
            f"=== Spécifications Optiques OV2640 à H = {altitude_m:.1f} m ===",
            f"FOV : {self.fov_x_deg:.1f}° (H) x {self.fov_y_deg:.1f}° (V)",
            f"GSD (Résolution au sol) : {gsd_cm:.2f} cm/pixel",
            f"Emprise au sol d'une image : {wx:.2f} m x {wy:.2f} m",
            f"Espacement photos (75% fwd) : {dx:.2f} m",
            f"Espacement lignes (65% side) : {dy:.2f} m",
            f"Vitesse max sans flou (1/1000s) : {v_max:.2f} m/s",
            f"Taille pixel : {self.pixel_pitch*1e6:.2f} µm",
            f"Focale : {self.focal_length*1e3:.2f} mm",
            f"Résolution : {self.nx} x {self.ny} pixels"
        ]
        return "\n".join(lines)


def main():
    """Fonction de test et démonstration"""
    
    print("=" * 60)
    print("MODÉLISATION OPTIQUE CAMÉRA OV2640")
    print("=" * 60)
    print()
    
    # Créer le modèle de caméra
    cam = CameraOV2640()
    
    # Altitude de travail
    altitude = 0.70  # mètres
    
    # Afficher le résumé
    print(cam.summary(altitude))
    print()
    
    # Paramètres de mission pour notre parcelle
    print("=== PARAMÈTRES DE MISSION ===")
    params = cam.compute_mission_params(
        field_length_m=2.0,  # longueur parcelle
        field_width_m=1.0,   # largeur parcelle
        altitude_m=altitude,
        flight_speed_ms=0.20
    )
    
    print(f"Parcelle : 2.0m x 1.0m")
    print(f"Altitude : {params['altitude_m']:.2f}m")
    print(f"GSD : {params['gsd_mm']:.2f} mm/pixel")
    print(f"Emprise : {params['footprint_wx_m']:.2f}m x {params['footprint_wy_m']:.2f}m")
    print(f"Photos : {params['nb_photos_total']} ({params['nb_photos_x']}x{params['nb_photos_y']})")
    print(f"Distance : {params['distance_totale_m']:.2f}m")
    print(f"Temps : {params['temps_vol_s']:.1f}s ({params['temps_vol_min']:.2f} min)")
    print(f"Batterie : {params['batterie_pct']:.1f}%")
    print(f"Vitesse max : {params['vitesse_max_ms']:.2f} m/s")
    
    print()
    print("=" * 60)
    print("✅ Modélisation optique terminée")
    print("=" * 60)


if __name__ == "__main__":
    main()