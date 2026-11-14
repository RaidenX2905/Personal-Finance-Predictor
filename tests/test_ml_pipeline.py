"""Unit tests for ML pipeline feature extraction, training, metrics, and inference."""

import os
import pytest
from datetime import date
import pandas as pd
from core.ml_pipeline import (
    extract_features_df,
    train_and_evaluate_model,
    load_model_artifact,
    predict_transaction_type,
    FEATURE_COLS
)


def test_feature_engineering():
    dummy = pd.DataFrame({
        "Date": ["2026-01-15", "2026-05-31"],
        "Amount": [150.0, 3200.0]
    })
    feat = extract_features_df(dummy)
    for col in FEATURE_COLS:
        assert col in feat.columns
    assert feat.loc[0, "Month"] == 1
    assert feat.loc[0, "Day"] == 15
    assert feat.loc[1, "IsMonthEnd"] == 1


def test_model_training_and_metrics():
    res = train_and_evaluate_model(save_artifact=False)
    assert "model" in res
    assert "holdout_metrics" in res
    assert res["holdout_metrics"]["roc_auc"] > 0.80
    assert res["cv_metrics"]["test_accuracy"] > 0.85


def test_prediction_inference():
    artifact = load_model_artifact()
    assert artifact is not None
    
    # Large amount should lean toward Income in synthetic dataset
    res_high = predict_transaction_type(amount=4500.0, tx_date=date(2026, 6, 15), artifact=artifact)
    assert res_high["prediction"] in ["Income", "Expense"]
    assert 0.0 <= res_high["confidence"] <= 100.0
    assert "caveat" in res_high
    
    # Small amount should lean toward Expense
    res_low = predict_transaction_type(amount=120.0, tx_date=date(2026, 6, 15), artifact=artifact)
    assert res_low["prediction"] == "Expense"
    assert res_low["confidence"] > 50.0
