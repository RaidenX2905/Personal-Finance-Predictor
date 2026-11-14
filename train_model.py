"""Independent script to reproduce, evaluate, and serialize the ML model."""

import sys
import os
import json

# Ensure project root in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ml_pipeline import train_and_evaluate_model


def main():
    print("=" * 60)
    print("PERSONAL FINANCE PREDICTOR — REPRODUCIBLE ML PIPELINE")
    print("=" * 60)
    
    csv_path = "Personal_Finance_Dataset.csv"
    if not os.path.exists(csv_path):
        print(f"Error: Could not find training file '{csv_path}'")
        sys.exit(1)
        
    print(f"Training and calibrating model from '{csv_path}'...")
    result = train_and_evaluate_model(csv_path=csv_path, save_artifact=True)
    
    print("\n--- Model Architecture & Artifact ---")
    print(f"Algorithm:       {result['algorithm']}")
    print(f"Sample Count:    {result['n_samples']}")
    print(f"Features:        {', '.join(result['feature_names'])}")
    print(f"Distribution:    {result['class_distribution']}")
    
    print("\n--- Cross-Validation Metrics (Stratified 5-Fold) ---")
    for k, v in result["cv_metrics"].items():
        metric_name = k.replace("test_", "").upper()
        print(f"{metric_name:<16}: {v:.4f}")
        
    print("\n--- Holdout Test Split Metrics (20% Holdout) ---")
    for k, v in result["holdout_metrics"].items():
        print(f"{k.upper():<16}: {v:.4f}")
        
    print("\nArtifact successfully serialized to 'model.pkl' & 'data/model_metrics.json'")
    print("=" * 60)


if __name__ == "__main__":
    main()
