#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithme Lawnmower (Boustrophédon) - Planification de Trajectoires
Binôme A - Fyh & Liwingston

Référence : Choset, H. (2001). "Coverage for robotics."
            Annals of Mathematics and Artificial Intelligence, 31(1), 113-126.
"""

import numpy as np
from typing import List, Tuple, Dict


class LawnmowerPlanner:
    """
    Planificateur de trajectoire en lacets (Lawnmower Coverage Path Planning).
    Optimisé pour les micro-parcelles agricoles et le profil de vol du Pydrone.
    """
    
    def __init__(self):
        pass
    
    def plan_rectangular_field(self,
                               field_length_m: float,
                               field_width_m: float,
                               altitude_m: float,
                               flight_speed_ms: float = 0.20,
                               forward_overlap: float = 0.75,
                               side_overlap: float = 0.65,
                               pixel_pitch_m: float = 2.24e-6,
                               focal_length_m: float = 3.6e-3,
                               resolution_x: int = 1600,
                               resolution_y: int = 1200,
                               takeoff_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Dict:
        """
        Génère les waypoints 3D et les points de prise de vue pour une parcelle rectangulaire.
        
        :param field_length_m: Longueur de la parcelle selon l'axe X (m)
        :param field_width_m: Largeur de la parcelle selon l'axe Y (m)
        :param altitude_m: Altitude de survol Z (m)
        :param flight_speed_ms: Vitesse du drone (m/s)
        :param forward_overlap: Recouvrement frontal (0 à 1)
        :param side_overlap: Recouvrement latéral (0 à 1)
        :param pixel_pitch_m: Taille d'un pixel en mètres
        :param focal_length_m: Distance focale en mètres
        :param resolution_x: Résolution horizontale (pixels)
        :param resolution_y: Résolution verticale (pixels)
        :param takeoff_point: Coordonnées (X, Y, Z) du point de décollage
        :return: Dictionnaire contenant waypoints, photo_locations, et métriques de vol
        """
        
        # Calcul de l'emprise au sol
        sensor_width = resolution_x * pixel_pitch_m
        sensor_height = resolution_y * pixel_pitch_m
        
        wx = (sensor_width * altitude_m) / focal_length_m
        wy = (sensor_height * altitude_m) / focal_length_m
        
        # Calcul de l'espacement
        dx_photo = wx * (1.0 - forward_overlap)
        dy_intertrace = wy * (1.0 - side_overlap)
        
        # Marge pour couverture complète
        x_min = wx / 2.0
        x_max = field_length_m - wx / 2.0
        y_min = wy / 2.0
        y_max = field_width_m - wy / 2.0
        
        # Si la parcelle est plus petite qu'une seule photo, on centre
        if x_max < x_min:
            x_min = x_max = field_length_m / 2.0
        if y_max < y_min:
            y_min = y_max = field_width_m / 2.0
        
        # Génération des lignes Y
        y_lines = []
        y = y_min
        while y <= y_max:
            y_lines.append(y)
            y += dy_intertrace
        if not y_lines or y_lines[-1] < y_max:
            y_lines.append(y_max)
        
        waypoints = []
        photo_locations = []
        
        # 1. Point de décollage
        waypoints.append(takeoff_point)
        
        # 2. Montée verticale
        first_x = x_min
        first_y = y_lines[0]
        waypoints.append((takeoff_point[0], takeoff_point[1], altitude_m))
        waypoints.append((first_x, first_y, altitude_m))
        
        direction = 1  # 1 : gauche à droite, -1 : droite à gauche
        
        for i, y_curr in enumerate(y_lines):
            if direction == 1:
                x_start, x_end = x_min, x_max
            else:
                x_start, x_end = x_max, x_min
            
            # Waypoint de début de ligne
            if i > 0:
                waypoints.append((x_start, y_curr, altitude_m))
            
            # Échantillonnage des photos le long de la ligne
            dist_line = abs(x_end - x_start)
            num_photos = max(1, int(np.ceil(dist_line / dx_photo)) + 1)
            x_photos = np.linspace(x_start, x_end, num_photos)
            
            for xp in x_photos:
                photo_locations.append((xp, y_curr, altitude_m))
            
            # Waypoint de fin de ligne
            waypoints.append((x_end, y_curr, altitude_m))
            
            # Inverser la direction
            direction *= -1
        
        # 3. Retour au point de décollage (RTH)
        waypoints.append((takeoff_point[0], takeoff_point[1], altitude_m))
        waypoints.append(takeoff_point)
        
        # Calcul des distances et temps de vol
        total_distance = 0.0
        for j in range(len(waypoints) - 1):
            p1 = np.array(waypoints[j])
            p2 = np.array(waypoints[j+1])
            total_distance += np.linalg.norm(p2 - p1)
        
        flight_time_s = total_distance / flight_speed_ms
        battery_autonomy_s = 8.0 * 60.0  # 8 minutes
        battery_percent_used = (flight_time_s / battery_autonomy_s) * 100.0
        
        # GSD
        gsd_m = (pixel_pitch_m * altitude_m) / focal_length_m
        
        return {
            "waypoints": waypoints,
            "photo_locations": photo_locations,
            "total_distance_m": total_distance,
            "flight_time_s": flight_time_s,
            "flight_time_min": flight_time_s / 60.0,
            "battery_percent_used": battery_percent_used,
            "num_photos": len(photo_locations),
            "num_lines": len(y_lines),
            "wx": wx,
            "wy": wy,
            "gsd_mm": gsd_m * 1000,
            "dx_photo": dx_photo,
            "dy_intertrace": dy_intertrace
        }


def main():
    """Fonction de test"""
    planner = LawnmowerPlanner()
    
    # Paramètres du banc expérimental
    plan = planner.plan_rectangular_field(
        field_length_m=3.5,
        field_width_m=2.5,
        altitude_m=0.70,
        flight_speed_ms=0.20
    )
    
    print("=" * 60)
    print("PLANIFICATION LAWNMOWER - BANC EXPÉRIMENTAL")
    print("=" * 60)
    print()
    print(f"Parcelle : 3.5m × 2.5m")
    print(f"Altitude : 0.70m")
    print(f"GSD : {plan['gsd_mm']:.2f} mm/pixel")
    print(f"Emprise : {plan['wx']:.2f}m × {plan['wy']:.2f}m")
    print(f"Espacement photos : {plan['dx_photo']:.2f}m")
    print(f"Espacement lignes : {plan['dy_intertrace']:.2f}m")
    print(f"Nombre de lignes : {plan['num_lines']}")
    print(f"Nombre de photos : {plan['num_photos']}")
    print(f"Distance totale : {plan['total_distance_m']:.2f}m")
    print(f"Temps de vol : {plan['flight_time_s']:.1f}s ({plan['flight_time_min']:.2f} min)")
    print(f"Consommation batterie : {plan['battery_percent_used']:.1f}%")
    print()


if __name__ == "__main__":
    main()