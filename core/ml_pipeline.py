"""Machine Learning pipeline: features, evaluation, training, calibration, and inference."""

import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, date

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.calibration import CalibratedClassifierCV

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model.pkl")
METRICS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "model_metrics.json")


def extract_features_df(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer robust tabular features from transaction dates and amounts."""
    feat = pd.DataFrame(index=df.index)
    
    # Amounts
    amounts = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
    feat["Amount"] = amounts
    feat["Log_Amount"] = np.log1p(np.maximum(0.0, amounts))
    
    # Dates
    dates = pd.to_datetime(df["Date"], errors="coerce")
    feat["Month"] = dates.dt.month.fillna(1).astype(int)
    feat["Day"] = dates.dt.day.fillna(1).astype(int)
    feat["DayOfWeek"] = dates.dt.day_of_week.fillna(0).astype(int)
    feat["IsWeekend"] = feat["DayOfWeek"].isin([5, 6]).astype(int)
    feat["IsMonthEnd"] = dates.dt.is_month_end.fillna(False).astype(int)
    feat["DaysInMonth"] = dates.dt.days_in_month.fillna(30).astype(int)
    
    return feat


FEATURE_COLS = ["Amount", "Log_Amount", "Month", "Day", "DayOfWeek", "IsWeekend", "IsMonthEnd"]


def train_and_evaluate_model(
    csv_path: Optional[str] = None,
    save_artifact: bool = True
) -> Dict[str, Any]:
    """Train Gradient Boosting model with calibrated probabilities and k-fold cross validation."""
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Personal_Finance_Dataset.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Training dataset not found: {csv_path}")
        
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "Amount", "Type"])
    
    # Target: Income = 1, Expense = 0
    y = (df["Type"].astype(str).str.strip().str.lower() == "income").astype(int)
    X = extract_features_df(df)[FEATURE_COLS]
    
    # Train / Test split for honest holdout
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Base model: Gradient Boosting
    base_model = GradientBoostingClassifier(
        n_estimators=120,
        learning_rate=0.08,
        max_depth=3,
        random_state=42
    )
    
    # Stratified K-Fold CV Evaluation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc"
    }
    cv_results = cross_validate(base_model, X, y, cv=cv, scoring=scoring)
    
    # Train model on train split and evaluate on holdout
    base_model.fit(X_train, y_train)
    y_pred = base_model.predict(X_test)
    y_prob = base_model.predict_proba(X_test)[:, 1]
    
    holdout_metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob))
    }
    
    cv_metrics = {k: float(np.mean(v)) for k, v in cv_results.items() if k.startswith("test_")}
    
    # Fit final calibrated model across full dataset
    final_estimator = GradientBoostingClassifier(
        n_estimators=120,
        learning_rate=0.08,
        max_depth=3,
        random_state=42
    )
    # Calibrated Classifier for honest probabilities
    calibrated_model = CalibratedClassifierCV(estimator=final_estimator, cv=5, method="sigmoid")
    calibrated_model.fit(X, y)
    
    payload = {
        "model": calibrated_model,
        "feature_names": FEATURE_COLS,
        "trained_at": datetime.now().isoformat(),
        "n_samples": len(X),
        "class_distribution": {
            "Income": int(y.sum()),
            "Expense": int((1 - y).sum())
        },
        "holdout_metrics": holdout_metrics,
        "cv_metrics": cv_metrics,
        "algorithm": "CalibratedClassifierCV(GradientBoostingClassifier)"
    }
    
    if save_artifact:
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(payload, f)
        
        # Save metrics JSON for quick dashboard reporting
        metrics_meta = {k: v for k, v in payload.items() if k != "model"}
        import json
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics_meta, f, indent=2)
            
    return payload


def load_model_artifact() -> Optional[Dict[str, Any]]:
    """Safely load model artifact bundle. Retrain automatically if artifact missing or legacy."""
    if not os.path.exists(MODEL_PATH):
        try:
            return train_and_evaluate_model(save_artifact=True)
        except Exception:
            return None
            
    try:
        with open(MODEL_PATH, "rb") as f:
            loaded = pickle.load(f)
            # Check if modern dict bundle or legacy raw scikit-learn estimator
            if isinstance(loaded, dict) and "model" in loaded and "feature_names" in loaded:
                return loaded
            else:
                # Legacy uncalibrated model object - retrain cleanly
                return train_and_evaluate_model(save_artifact=True)
    except Exception:
        # Pickle incompatibility or corruption
        return train_and_evaluate_model(save_artifact=True)


def predict_transaction_type(
    amount: float,
    tx_date: date,
    artifact: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Classify transaction as Income or Expense with statistical calibration and limit disclosure."""
    if artifact is None:
        artifact = load_model_artifact()
        
    if artifact is None or "model" not in artifact:
        return {
            "error": "ML model artifact unavailable.",
            "prediction": "Unknown",
            "confidence": 0.0,
            "income_prob": 0.0,
            "expense_prob": 0.0
        }
    
    model = artifact["model"]
    
    # Feature construction
    d = pd.to_datetime(tx_date)
    amount_clean = max(0.01, float(amount))
    row_data = {
        "Amount": [amount_clean],
        "Log_Amount": [np.log1p(amount_clean)],
        "Month": [d.month],
        "Day": [d.day],
        "DayOfWeek": [d.day_of_week],
        "IsWeekend": [1 if d.day_of_week in [5, 6] else 0],
        "IsMonthEnd": [1 if d.is_month_end else 0]
    }
    feat_df = pd.DataFrame(row_data)[artifact.get("feature_names", FEATURE_COLS)]
    
    probs = model.predict_proba(feat_df)[0]  # [p_expense, p_income]
    p_expense = float(probs[0])
    p_income = float(probs[1])
    
    predicted_type = "Income" if p_income >= 0.50 else "Expense"
    confidence = max(p_income, p_expense) * 100.0
    
    # Statistical limitations explanation
    is_high_certainty = confidence >= 80.0
    certainty_tier = "High Probability" if is_high_certainty else "Moderate Ambiguity"
    
    return {
        "prediction": predicted_type,
        "confidence": round(confidence, 1),
        "income_prob": round(p_income * 100.0, 1),
        "expense_prob": round(p_expense * 100.0, 1),
        "tier": certainty_tier,
        "features_evaluated": row_data,
        "algorithm": artifact.get("algorithm", "GradientBoostingClassifier"),
        "caveat": (
            "Model classification is driven primarily by transaction magnitude clustering and historical date patterns. "
            "In real personal accounting, category semantics ('Salary' vs 'Groceries') provide ground-truth certainty."
        )
    }
