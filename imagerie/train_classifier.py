#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entraînement du Classificateur de Stress Hydrique

Projet : Suivi du stress hydrique par imagerie aérienne
Binôme A — Fyh & Liwingston

Ce module implémente :
- Entraînement d'un classificateur RandomForest
- Validation croisée 5-fold
- Export du modèle (.pkl)
- Métriques de performance

IMPORTANT : 4 features seulement (conformément au CDC) :
1. ExG moyen
2. ExG écart-type
3. GRVI moyen
4. GRVI écart-type

Références :
- RandomForest : Breiman (2001) - "Random Forests"
- Validation croisée : Kohavi (1995) - "A study of cross-validation"
"""

import os
import json
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from datetime import datetime


class StressClassifierTrainer:
    """
    Entraîneur de classificateur de stress hydrique.
    
    Utilise un RandomForest avec 4 features :
    1. ExG moyen
    2. ExG écart-type
    3. GRVI moyen
    4. GRVI écart-type
    
    Référence : Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.
    """
    
    def __init__(self, 
                 n_estimators: int = 150,
                 max_depth: int = 6,
                 min_samples_leaf: int = 3,
                 random_state: int = 42):
        """
        Initialise l'entraîneur de classificateur.
        
        Args:
            n_estimators: Nombre d'arbres dans la forêt (défaut 150)
            max_depth: Profondeur maximale des arbres (défaut 6)
            min_samples_leaf: Nombre minimum d'échantillons par feuille (défaut 3)
            random_state: Graine aléatoire pour la reproductibilité
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        
        # Pipeline : StandardScaler + RandomForest
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestClassifier(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                class_weight='balanced',
                random_state=self.random_state,
                n_jobs=-1
            ))
        ])
        
        # Métriques d'entraînement
        self.cv_scores = None
        self.cv_mean = None
        self.cv_std = None
        self.feature_importances = None
    
    def generate_synthetic_dataset(self, 
                                   n_healthy: int = 60,
                                   n_stressed: int = 60) -> tuple:
        """
        Génère un dataset synthétique calibré pour la validation.
        
        Les valeurs sont basées sur les observations de notre caméra OV2640 NIR-modified :
        - Végétation saine : ExG élevé (~0.49), GRVI faible (~0.10)
        - Végétation stressée : ExG faible (~0.10), GRVI élevé (~0.30)
        
        Args:
            n_healthy: Nombre d'échantillons sains
            n_stressed: Nombre d'échantillons stressés
            
        Returns:
            Tuple (X, y) avec les features et les labels
        """
        np.random.seed(self.random_state)
        
        # Features pour végétation saine
        # ExG élevé (forte réflectance verte), GRVI faible (faible réflectance rouge)
        X_healthy = np.column_stack([
            np.random.normal(0.49, 0.025, n_healthy),  # ExG moyen
            np.random.normal(0.03, 0.008, n_healthy),  # ExG écart-type
            np.random.normal(0.10, 0.02, n_healthy),   # GRVI moyen
            np.random.normal(0.05, 0.01, n_healthy)    # GRVI écart-type
        ])
        
        # Features pour végétation stressée
        # ExG faible (chlorophylle réduite), GRVI élevé (réflectance rouge accrue)
        X_stressed = np.column_stack([
            np.random.normal(0.10, 0.022, n_stressed),  # ExG moyen
            np.random.normal(0.04, 0.01, n_stressed),   # ExG écart-type
            np.random.normal(0.30, 0.03, n_stressed),   # GRVI moyen
            np.random.normal(0.08, 0.02, n_stressed)    # GRVI écart-type
        ])
        
        # Concaténation
        X = np.vstack([X_healthy, X_stressed])
        y = np.array([0] * n_healthy + [1] * n_stressed)  # 0=sain, 1=stressé
        
        return X, y
    
    def train(self, X: np.ndarray, y: np.ndarray) -> dict:
        """
        Entraîne le classificateur avec validation croisée.
        
        Args:
            X: Features (n_samples, 4)
            y: Labels (0=sain, 1=stressé)
            
        Returns:
            Dictionnaire avec les métriques d'entraînement
        """
        print(f"Dataset : {X.shape[0]} échantillons, {X.shape[1]} features")
        print(f"Classes : Sain={np.sum(y==0)}, Stressé={np.sum(y==1)}")
        print()
        
        # Validation croisée stratifiée 5-fold
        # Référence : Kohavi, R. (1995). "A study of cross-validation and bootstrap 
        # for accuracy estimation and model selection." IJCAI, 14(2), 1137-1145.
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        
        # Calcul des scores
        self.cv_scores = cross_val_score(self.pipeline, X, y, cv=cv, scoring='f1')
        self.cv_mean = float(self.cv_scores.mean())
        self.cv_std = float(self.cv_scores.std())
        
        print(f"Validation croisée 5-fold :")
        print(f"  F1 moyen : {self.cv_mean:.3f} ± {self.cv_std:.3f}")
        print(f"  Accuracy : {cross_val_score(self.pipeline, X, y, cv=cv).mean():.3f}")
        print()
        
        # Entraînement final sur tout le dataset
        self.pipeline.fit(X, y)
        
        # Importance des features
        rf_model = self.pipeline.named_steps['rf']
        self.feature_importances = rf_model.feature_importances_
        
        # Rapport de classification
        y_pred = self.pipeline.predict(X)
        
        print("=== RAPPORT DE CLASSIFICATION ===")
        print(classification_report(y, y_pred, target_names=['Sain', 'Stressé']))
        print("Matrice de confusion :")
        print(confusion_matrix(y, y_pred))
        print()
        
        # Importance des features
        feature_names = ['ExG_moyen', 'ExG_std', 'GRVI_moyen', 'GRVI_std']
        print("=== IMPORTANCE DES FEATURES ===")
        for name, importance in sorted(zip(feature_names, self.feature_importances), 
                                      key=lambda x: -x[1]):
            print(f"  {name:15s} : {importance:.3f}")
        
        return {
            'cv_f1_mean': self.cv_mean,
            'cv_f1_std': self.cv_std,
            'feature_importances': dict(zip(feature_names, self.feature_importances.tolist())),
            'n_samples': len(y),
            'n_healthy': int(np.sum(y == 0)),
            'n_stressed': int(np.sum(y == 1))
        }
    
    def predict(self, features: np.ndarray) -> int:
        """
        Prédit la classe d'un échantillon.
        
        Args:
            features: Array de 4 features [exg_mean, exg_std, grvi_mean, grvi_std]
            
        Returns:
            0 = Sain, 1 = Stressé
        """
        return self.pipeline.predict(features.reshape(1, -1))[0]
    
    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        """
        Retourne les probabilités de classe.
        
        Args:
            features: Array de 4 features
            
        Returns:
            Array de probabilités [P(sain), P(stressé)]
        """
        return self.pipeline.predict_proba(features.reshape(1, -1))[0]
    
    def save_model(self, output_dir: str = "models") -> dict:
        """
        Sauvegarde le modèle entraîné et les métadonnées.
        
        Args:
            output_dir: Dossier de sortie
            
        Returns:
            Dictionnaire avec les chemins des fichiers sauvegardés
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Sauvegarder le modèle
        model_path = os.path.join(output_dir, "stress_rf_v1.pkl")
        joblib.dump(self.pipeline, model_path)
        
        # Sauvegarder les métadonnées
        metadata = {
            "model": "RandomForestClassifier",
            "features": ["ExG_moyen", "ExG_std", "GRVI_moyen", "GRVI_std"],
            "n_samples": int(self.cv_scores.shape[0] * 5) if self.cv_scores is not None else 0,
            "cv_f1_mean": self.cv_mean,
            "cv_f1_std": self.cv_std,
            "threshold_exg": 0.20,
            "threshold_grvi": 0.15,
            "date": datetime.now().isoformat(),
            "seed": self.random_state,
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth
        }
        
        metadata_path = os.path.join(output_dir, "stress_rf_v1_meta.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Modèle sauvegardé : {model_path}")
        print(f"✅ Métadonnées sauvegardées : {metadata_path}")
        
        return {
            'model_path': model_path,
            'metadata_path': metadata_path
        }


def main():
    """Fonction principale d'entraînement"""
    
    print("=" * 60)
    print("ENTRAÎNEMENT DU CLASSIFICATEUR DE STRESS HYDRIQUE")
    print("=" * 60)
    print()
    
    # Créer l'entraîneur
    trainer = StressClassifierTrainer(
        n_estimators=150,
        max_depth=6,
        min_samples_leaf=3,
        random_state=42
    )
    
    # Générer le dataset synthétique
    print("1. Génération du dataset synthétique...")
    X, y = trainer.generate_synthetic_dataset(n_healthy=60, n_stressed=60)
    
    # Entraîner le modèle
    print("2. Entraînement du modèle...")
    metrics = trainer.train(X, y)
    
    # Sauvegarder le modèle
    print("3. Sauvegarde du modèle...")
    paths = trainer.save_model(output_dir="models")
    
    # Résumé
    print()
    print("=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"Précision (F1) : {metrics['cv_f1_mean']:.3f} ± {metrics['cv_f1_std']:.3f}")
    print(f"Dataset : {metrics['n_samples']} échantillons")
    print(f"  - Sains : {metrics['n_healthy']}")
    print(f"  - Stressés : {metrics['n_stressed']}")
    print()
    print("Features utilisées :")
    for name, importance in metrics['feature_importances'].items():
        print(f"  - {name} : {importance:.3f}")
    print()
    print("Utilisation :")
    print(f"  model = joblib.load('{paths['model_path']}')")
    print(f"  prediction = model.predict([[exg_mean, exg_std, grvi_mean, grvi_std]])")
    print()
    print("=" * 60)
    print("✅ Entraînement terminé avec succès")
    print("=" * 60)


if __name__ == "__main__":
    main()