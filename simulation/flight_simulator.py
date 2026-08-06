#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulateur de Vol - Validation des Trajectoires
Binôme A - Fyh & Liwingston

Simule le vol du drone Pydrone sur une trajectoire Lawnmower
avec modèle cinématique réaliste.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict


class FlightSimulator:
    """
    Simulateur de vol pour le drone Pydrone.
    Modélise la cinématique avec profils de vitesse trapézoïdaux.
    """
    
    def __init__(self,
                 max_speed_ms: float = 0.20,
                 max_accel_ms2: float = 0.15,
                 hover_stabilization_s: float = 0.4):
        """
        Initialise le simulateur.
        
        :param max_speed_ms: Vitesse maximale (m/s)
        :param max_accel_ms2: Accélération maximale (m/s²)
        :param hover_stabilization_s: Temps de stabilisation avant photo (s)
        """
        self.max_speed = max_speed_ms
        self.max_accel = max_accel_ms2
        self.hover_time = hover_stabilization_s
    
    def compute_segment_time(self, distance_m: float, stop_at_end: bool = True) -> Tuple[float, Dict]:
        """
        Calcule le temps de parcours d'un segment avec profil trapézoïdal.
        
        :param distance_m: Distance du segment (m)
        :param stop_at_end: Si True, le drone s'arrête à la fin
        :return: (temps_total, détails)
        """
        if distance_m <= 0:
            return 0.0, {"type": "zero", "time": 0.0}
        
        # Distance d'accélération/décélération
        d_accel = (self.max_speed ** 2) / (2.0 * self.max_accel)
        
        if stop_at_end:
            if distance_m < 2.0 * d_accel:
                # Profil triangulaire
                v_peak = np.sqrt(distance_m * self.max_accel)
                t_accel = v_peak / self.max_accel
                t_total = 2.0 * t_accel
                profile = "Triangulaire"
            else:
                # Profil trapézoïdal
                t_accel = self.max_speed / self.max_accel
                d_cruise = distance_m - 2.0 * d_accel
                t_cruise = d_cruise / self.max_speed
                t_total = 2.0 * t_accel + t_cruise
                profile = "Trapézoïdal"
        else:
            # Vol continu
            t_total = distance_m / self.max_speed
            profile = "Continu"
        
        return t_total, {"profile": profile, "time": t_total}
    
    def simulate_continuous_flight(self, waypoints: List[Tuple[float, float, float]], 
                                  num_photos: int) -> Dict:
        """
        Simule un vol continu à vitesse constante.
        
        :param waypoints: Liste des waypoints (x, y, z)
        :param num_photos: Nombre de photos à prendre
        :return: Métriques de simulation
        """
        total_time_s = 0.0
        distances = []
        
        for i in range(len(waypoints) - 1):
            p1 = np.array(waypoints[i])
            p2 = np.array(waypoints[i+1])
            dist = np.linalg.norm(p2 - p1)
            distances.append(dist)
            
            t_seg, _ = self.compute_segment_time(dist, stop_at_end=False)
            total_time_s += t_seg
        
        total_dist = sum(distances)
        battery_percent = (total_time_s / (8.0 * 60.0)) * 100
        
        return {
            "mode": "Vol Continu",
            "total_distance_m": total_dist,
            "total_time_s": total_time_s,
            "total_time_min": total_time_s / 60.0,
            "battery_percent": battery_percent,
            "num_photos": num_photos,
            "blur_risk": "Faible (v < vmax)"
        }
    
    def simulate_stop_and_capture(self, photo_locations: List[Tuple[float, float, float]],
                                  takeoff_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Dict:
        """
        Simule un mode Stop-and-Capture.
        
        :param photo_locations: Points de prise de vue
        :param takeoff_point: Point de décollage
        :return: Métriques de simulation
        """
        full_path = [takeoff_point] + photo_locations + [takeoff_point]
        
        total_time_s = 0.0
        total_dist = 0.0
        time_stab = 0.0
        
        for i in range(len(full_path) - 1):
            p1 = np.array(full_path[i])
            p2 = np.array(full_path[i+1])
            dist = np.linalg.norm(p2 - p1)
            total_dist += dist
            
            t_seg, _ = self.compute_segment_time(dist, stop_at_end=True)
            total_time_s += t_seg
            
            # Temps de stabilisation pour chaque photo
            if i < len(photo_locations):
                total_time_s += self.hover_time
                time_stab += self.hover_time
        
        battery_percent = (total_time_s / (8.0 * 60.0)) * 100
        
        return {
            "mode": "Stop-and-Capture",
            "total_distance_m": total_dist,
            "total_time_s": total_time_s,
            "total_time_min": total_time_s / 60.0,
            "battery_percent": battery_percent,
            "time_stabilization_s": time_stab,
            "blur_risk": "Nul (v=0)"
        }


def main():
    """Fonction de test"""
    from lawnmower_planner import LawnmowerPlanner
    
    print("=" * 60)
    print("SIMULATION DE VOL - COMPARAISON DES MODES")
    print("=" * 60)
    print()
    
    # Générer la trajectoire
    planner = LawnmowerPlanner()
    plan = planner.plan_rectangular_field(
        field_length_m=3.5,
        field_width_m=2.5,
        altitude_m=0.70,
        flight_speed_ms=0.20
    )
    
    # Simuler les deux modes
    simulator = FlightSimulator()
    
    # Mode 1 : Vol continu
    res_continuous = simulator.simulate_continuous_flight(
        plan['waypoints'], 
        plan['num_photos']
    )
    
    # Mode 2 : Stop-and-Capture
    res_stop = simulator.simulate_stop_and_capture(
        plan['photo_locations']
    )
    
    # Affichage comparatif
    print(f"{'Métrique':<30} | {'Vol Continu':<20} | {'Stop-and-Capture':<20}")
    print("-" * 75)
    print(f"{'Distance totale':<30} | {res_continuous['total_distance_m']:<17.2f} m | {res_stop['total_distance_m']:<17.2f} m")
    print(f"{'Temps total':<30} | {res_continuous['total_time_s']:<14.1f} s ({res_continuous['total_time_min']:.2f} min) | {res_stop['total_time_s']:<14.1f} s ({res_stop['total_time_min']:.2f} min)")
    print(f"{'Consommation batterie':<30} | {res_continuous['battery_percent']:<17.1f} % | {res_stop['battery_percent']:<17.1f} %")
    print(f"{'Temps stabilisation':<30} | {'0.0 s':<20} | {res_stop['time_stabilization_s']:<17.1f} s")
    print(f"{'Risque flou':<30} | {res_continuous['blur_risk']:<20} | {res_stop['blur_risk']:<20}")
    print()
    
    # Verdict
    if res_continuous['battery_percent'] < 100:
        print("✅ MODE RECOMMANDÉ : Vol Continu")
    else:
        print("❌ AUCUN MODE VIABLE")
    
    if res_stop['battery_percent'] > 100:
        print("❌ MODE Stop-and-Capture : IMPOSSIBLE (dépassement batterie)")


if __name__ == "__main__":
    main()