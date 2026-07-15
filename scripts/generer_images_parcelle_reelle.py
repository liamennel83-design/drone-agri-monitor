#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'Images Réalistes de Parcelle 1m × 2m
Binôme A - Fyh & Liwingston

Génère des images de haute qualité avec :
- 12 pots de tomates correctement positionnés
- Parcelle 1m × 2m respectée
- Pots Ø10.5cm, hauteur 12cm
- Espacement optimal calculé
- Visualisation du stress hydrique
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime
import json


class ParcelleImageGenerator:
    """Générateur d'images de parcelle réaliste"""
    
    def __init__(self, output_dir="data/dataset"):
        self.output_dir = output_dir
        self.dossier_sain = os.path.join(output_dir, "healthy")
        self.dossier_stresse = os.path.join(output_dir, "stressed")
        
        os.makedirs(self.dossier_sain, exist_ok=True)
        os.makedirs(self.dossier_stresse, exist_ok=True)
        
        # Paramètres de la parcelle
        self.field_width = 1.0   # m
        self.field_length = 2.0  # m
        self.pot_diameter = 0.105  # m (10.5 cm)
        self.pot_height = 0.12    # m (12 cm)
        self.margin = 0.10        # m (10 cm)
        self.num_cols = 3
        self.num_rows = 4
        
        # Calculer les positions optimales
        self.positions = self._compute_pot_positions()
        
        # Échelle pour l'affichage (pixels par mètre)
        self.scale = 400  # 400 pixels par mètre
        
    def _compute_pot_positions(self):
        """Calcule les positions optimales des pots"""
        usable_width = self.field_width - 2 * self.margin
        usable_length = self.field_length - 2 * self.margin
        
        spacing_x = usable_width / (self.num_cols - 1)
        spacing_y = usable_length / (self.num_rows - 1)
        
        positions = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = self.margin + col * spacing_x
                y = self.margin + row * spacing_y
                positions.append((x, y))
        
        return positions
    
    def _draw_pot(self, draw, x_px, y_px, radius_px, is_stressed=False, index=0):
        """Dessine un pot de tomate"""
        # Pot (cercle marron)
        pot_color = (139, 90, 43)  # Marron terre
        draw.ellipse([x_px - radius_px, y_px - radius_px,
                     x_px + radius_px, y_px + radius_px],
                    fill=pot_color, outline=(100, 60, 20), width=2)
        
        # Plante
        plant_radius = int(radius_px * 0.7)
        
        if is_stressed:
            # Plante stressée (jaunâtre)
            leaf_color = (180, 160, 60)
            highlight_color = (200, 180, 80)
        else:
            # Plante saine (verte)
            leaf_color = (34, 139, 34)
            highlight_color = (50, 180, 50)
        
        # Feuilles
        for i in range(5):
            angle = i * 72 * np.pi / 180
            lx = x_px + int(plant_radius * 0.6 * np.cos(angle))
            ly = y_px + int(plant_radius * 0.6 * np.sin(angle))
            lr = int(plant_radius * 0.4)
            draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr],
                        fill=leaf_color, outline=highlight_color, width=1)
        
        # Centre de la plante
        draw.ellipse([x_px - 5, y_px - 5, x_px + 5, y_px + 5],
                    fill=highlight_color)
        
        # Numéro du pot
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            font = ImageFont.load_default()
        
        draw.text((x_px - 5, y_px + radius_px + 2), f"P{index+1}", 
                 fill=(0, 0, 0), font=font)
    
    def generate_parcelle_image(self, index, is_stressed=False):
        """Génère une image réaliste de la parcelle"""
        # Dimensions de l'image
        img_width = int(self.field_width * self.scale)
        img_height = int(self.field_length * self.scale)
        
        # Créer l'image de base (terre)
        if is_stressed:
            bg_color = (160, 140, 80)  # Terre sèche
        else:
            bg_color = (120, 100, 60)  # Terre normale
        
        img = Image.new('RGB', (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Ajouter de la texture au sol
        for _ in range(500):
            tx = np.random.randint(0, img_width)
            ty = np.random.randint(0, img_height)
            tr = np.random.randint(1, 3)
            tc = np.random.randint(0, 30)
            color = (bg_color[0] + tc, bg_color[1] + tc, bg_color[2] + tc)
            draw.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], fill=color)
        
        # Dessiner les pots
        pot_radius_px = int(self.pot_diameter / 2 * self.scale)
        
        for i, (px, py) in enumerate(self.positions):
            x_px = int(px * self.scale)
            y_px = int((self.field_length - py) * self.scale)  # Inverser Y pour affichage
            
            # Variation aléatoire pour le réalisme
            x_px += np.random.randint(-3, 3)
            y_px += np.random.randint(-3, 3)
            
            self._draw_pot(draw, x_px, y_px, pot_radius_px, is_stressed, i)
        
        # Ajouter des bordures
        draw.rectangle([0, 0, img_width - 1, img_height - 1], 
                      outline=(80, 60, 30), width=3)
        
        # Ajouter le texte descriptif
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        if is_stressed:
            label = f"PARCELLE STRESSÉE - Image {index:03d}"
            info = "Stress hydrique | 50% ETc | Jaunissement visible"
            color = (255, 200, 200)
        else:
            label = f"PARCELLE SAINE - Image {index:03d}"
            info = "Irrigation normale | 100% ETc | Végétation vigoureuse"
            color = (200, 255, 200)
        
        draw.rectangle([5, 5, img_width - 5, 40], fill=(0, 0, 0, 128))
        draw.text((10, 10), label, fill=color, font=font)
        draw.text((10, img_height - 25), info, fill=(200, 200, 200), font=font_small)
        
        # Ajouter les dimensions
        draw.text((img_width - 80, img_height - 25), "1.0m × 2.0m", 
                 fill=(200, 200, 200), font=font_small)
        
        # Appliquer un léger flou pour réalisme
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        return img
    
    def generate_dataset(self, n_healthy=20, n_stressed=20):
        """Génère le dataset complet"""
        print("=" * 60)
        print("GÉNÉRATION D'IMAGES DE PARCELLE 1m × 2m")
        print("=" * 60)
        print()
        print(f"Configuration :")
        print(f"  Parcelle : {self.field_width}m × {self.field_length}m")
        print(f"  Pots : {self.num_cols} × {self.num_rows} = {len(self.positions)}")
        print(f"  Diamètre pot : {self.pot_diameter*100:.1f} cm")
        print(f"  Espacement X : {self.positions[1][0] - self.positions[0][0]:.2f} m")
        print(f"  Espacement Y : {self.positions[3][1] - self.positions[0][1]:.2f} m")
        print()
        
        # Générer les images saines
        print(f"📥 Génération de {n_healthy} images saines...")
        for i in range(1, n_healthy + 1):
            img = self.generate_parcelle_image(i, is_stressed=False)
            filename = f"parcelle_saine_{i:03d}.jpg"
            filepath = os.path.join(self.dossier_sain, filename)
            img.save(filepath, "JPEG", quality=95)
            print(f"  ✅ {filename}")
        
        # Générer les images stressées
        print(f"\n📥 Génération de {n_stressed} images stressées...")
        for i in range(1, n_stressed + 1):
            img = self.generate_parcelle_image(i, is_stressed=True)
            filename = f"parcelle_stressee_{i:03d}.jpg"
            filepath = os.path.join(self.dossier_stresse, filename)
            img.save(filepath, "JPEG", quality=95)
            print(f"  ✅ {filename}")
        
        # Métadonnées
        metadata = {
            "date_creation": datetime.now().isoformat(),
            "parcelle": {
                "largeur_m": self.field_width,
                "longueur_m": self.field_length,
                "surface_m2": self.field_width * self.field_length
            },
            "pots": {
                "nombre": len(self.positions),
                "diametre_cm": self.pot_diameter * 100,
                "hauteur_cm": self.pot_height * 100,
                "disposition": f"{self.num_cols}x{self.num_rows}",
                "positions": self.positions
            },
            "images": {
                "saines": n_healthy,
                "stressees": n_stressed,
                "total": n_healthy + n_stressed
            }
        }
        
        metadata_path = os.path.join(self.output_dir, "metadata_parcelle.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Métadonnées sauvegardées : {metadata_path}")
        print(f"\n{'='*60}")
        print(f"✅ DATASET GÉNÉRÉ : {n_healthy + n_stressed} images")
        print(f"{'='*60}")


def main():
    generator = ParcelleImageGenerator()
    generator.generate_dataset(n_healthy=20, n_stressed=20)


if __name__ == "__main__":
    main()