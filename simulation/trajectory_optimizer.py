#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimisation Multi-Critères des Trajectoires
Binôme A - Fyh & Liwingston

Optimise les paramètres de mission selon :
- Temps de vol
- Consommation batterie
- Couverture de la parcelle
- Qualité d'image (GSD)
"""

import numpy as np
from typing import Dict, List, Tuple


class TrajectoryOptimizer:
    """
    Optimiseur multi-critères pour les trajectoires de drone.
    """
    
    def __init__(self, 
                 battery_capacity_mah: float = 400,
                 battery_voltage_v: float = 3.7,
                 autonomy_s: float = 480):
        """
        Initialise l'optimiseur.
        
        :param battery_capacity_mah: Capacité batterie (mAh)
        :param battery_voltage_v: Tension nominale (V)
        :param autonomy_s: Autonomie théorique (secondes)
        """
        self.battery_capacity = battery_capacity_mah
        self.battery_voltage = battery_voltage_v
        self.autonomy_s = autonomy_s
    
    def compute_gsd(self, altitude_m: float, 
                    pixel_pitch_m: float = 2.24e-6,
                    focal_length_m: float = 3.6e-3) -> float:
        """Calcule le GSD en mm/pixel"""
        gsd_m = (pixel_pitch_m * altitude_m) / focal_length_m
        return gsd_m * 1000
    
    def compute_footprint(self, altitude_m: float,
                         pixel_pitch_m: float = 2.24e-6,
                         focal_length_m: float = 3.6e-3,
                         resolution_x: int = 1600,
                         resolution_y: int = 1200) -> Tuple[float, float]:
        """Calcule l'emprise au sol (wx, wy) en mètres"""
        sensor_width = resolution_x * pixel_pitch_m
        sensor_height = resolution_y * pixel_pitch_m
        wx = (sensor_width * altitude_m) / focal_length_m
        wy = (sensor_height * altitude_m) / focal_length_m
        return wx, wy
    
    def compute_max_speed(self, altitude_m: float,
                         exposure_time_s: float = 1.0/1000.0,
                         blur_limit_px: float = 0.5) -> float:
        """Calcule la vitesse maximale sans flou cinétique"""
        gsd_m = self.compute_gsd(altitude_m) / 1000  # Convertir en mètres
        v_max = (gsd_m * blur_limit_px) / exposure_time_s
        return v_max
    
    def optimize_mission(self,
                        field_length_m: float,
                        field_width_m: float,
                        altitudes: List[float] = None,
                        speeds: List[float] = None,
                        overlaps_fwd: List[float] = None,
                        overlaps_side: List[float] = None) -> Dict:
        """
        Optimise les paramètres de mission.
        
        Retourne les meilleurs paramètres selon un score multi-critères.
        """
        if altitudes is None:
            altitudes = [0.5, 0.7, 1.0, 1.2, 1.5]
        if speeds is None:
            speeds = [0.10, 0.15, 0.20, 0.25, 0.30]
        if overlaps_fwd is None:
            overlaps_fwd = [0.60, 0.70, 0.75, 0.80]
        if overlaps_side is None:
            overlaps_side = [0.50, 0.60, 0.65, 0.70]
        
        best_score = -1
        best_params = None
        results = []
        
        for alt in altitudes:
            for speed in speeds:
                for of in overlaps_fwd:
                    for os in overlaps_side:
                        # Vérifier la contrainte de flou
                        v_max = self.compute_max_speed(alt)
                        if speed > v_max:
                            continue
                        
                        # Calculer les paramètres
                        wx, wy = self.compute_footprint(alt)
                        dx = wx * (1 - of)
                        dy = wy * (1 - os)
                        
                        # Nombre de photos et lignes
                        nb_photos_x = max(1, int(np.ceil(field_length_m / dx)))
                        nb_photos_y = max(1, int(np.ceil(field_width_m / dy)))
                        nb_photos = nb_photos_x * nb_photos_y
                        
                        # Distance et temps
                        distance = nb_photos_y * field_length_m
                        time_s = distance / speed
                        time_min = time_s / 60
                        
                        # Consommation batterie
                        battery_pct = (time_s / self.autonomy_s) * 100
                        
                        # Vérifier la faisabilité
                        if battery_pct > 100:
                            continue
                        
                        # Score multi-critères (à maximiser)
                        # Plus le score est élevé, mieux c'est
                        score = self._compute_score(
                            time_s=time_s,
                            battery_pct=battery_pct,
                            gsd_mm=self.compute_gsd(alt),
                            nb_photos=nb_photos,
                            coverage=100.0  # Lawnmower garantit 100%
                        )
                        
                        result = {
                            'altitude_m': alt,
                            'speed_ms': speed,
                            'overlap_fwd': of,
                            'overlap_side': os,
                            'gsd_mm': self.compute_gsd(alt),
                            'wx': wx,
                            'wy': wy,
                            'nb_photos': nb_photos,
                            'distance_m': distance,
                            'time_s': time_s,
                            'time_min': time_min,
                            'battery_pct': battery_pct,
                            'score': score,
                            'feasible': battery_pct <= 100
                        }
                        
                        results.append(result)
                        
                        if score > best_score:
                            best_score = score
                            best_params = result
        
        return {
            'best_params': best_params,
            'all_results': results,
            'num_combinations': len(results)
        }
    
    def _compute_score(self, time_s: float, battery_pct: float, 
                      gsd_mm: float, nb_photos: int, coverage: float) -> float:
        """
        Calcule un score multi-critères.
        
        Pondérations :
        - Temps : 30% (minimiser)
        - Batterie : 30% (minimiser)
        - GSD : 20% (minimiser = meilleure résolution)
        - Couverture : 20% (maximiser)
        """
        # Normalisation
        time_score = 1.0 / (1.0 + time_s / 100)  # Plus le temps est court, mieux c'est
        battery_score = 1.0 / (1.0 + battery_pct / 100)  # Plus la batterie est conservée, mieux c'est
        gsd_score = 1.0 / (1.0 + gsd_mm)  # Plus le GSD est petit, mieux c'est
        coverage_score = coverage / 100.0  # 100% = optimal
        
        # Score pondéré
        score = (0.30 * time_score + 
                 0.30 * battery_score + 
                 0.20 * gsd_score + 
                 0.20 * coverage_score)
        
        return score


def main():
    """Fonction de test"""
    optimizer = TrajectoryOptimizer()
    
    print("=" * 60)
    print("OPTIMISATION MULTI-CRITÈRES DES TRAJECTOIRES")
    print("=" * 60)
    print()
    
    # Optimisation pour la parcelle 3.5×2.5m
    result = optimizer.optimize_mission(
        field_length_m=3.5,
        field_width_m=2.5
    )
    
    print(f"Combinaisons testées : {result['num_combinations']}")
    print()
    print("MEILLEURE SOLUTION :")
    print("-" * 40)
    
    best = result['best_params']
    print(f"Altitude : {best['altitude_m']:.2f} m")
    print(f"Vitesse : {best['speed_ms']:.2f} m/s")
    print(f"Recouvrement frontal : {best['overlap_fwd']*100:.0f}%")
    print(f"Recouvrement latéral : {best['overlap_side']*100:.0f}%")
    print(f"GSD : {best['gsd_mm']:.2f} mm/pixel")
    print(f"Emprise : {best['wx']:.2f}m × {best['wy']:.2f}m")
    print(f"Photos : {best['nb_photos']}")
    print(f"Distance : {best['distance_m']:.2f} m")
    print(f"Temps : {best['time_s']:.1f}s ({best['time_min']:.2f} min)")
    print(f"Batterie : {best['battery_pct']:.1f}%")
    print(f"Score : {best['score']:.4f}")
    print()


if __name__ == "__main__":
    main()