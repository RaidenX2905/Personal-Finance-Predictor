"""Smoke test for Streamlit app and views."""

import pytest
import pandas as pd
from datetime import date
from core.data_manager import get_combined_dataset
from core.ml_pipeline import load_model_artifact, predict_transaction_type
from core.budget_service import calculate_budget_performance
from core.goals_service import load_goals
from components.charts import (
    create_income_expense_trend_chart,
    create_category_breakdown_chart,
    create_cumulative_balance_chart,
    create_budget_variance_chart
)


def test_full_system_smoke():
    # 1. Dataset loading
    df = get_combined_dataset(include_baseline=True)
    assert not df.empty
    assert len(df) >= 1500
    
    # 2. Charts render without errors
    fig1 = create_income_expense_trend_chart(df)
    assert fig1 is not None
    
    fig2 = create_category_breakdown_chart(df)
    assert fig2 is not None
    
    fig3 = create_cumulative_balance_chart(df)
    assert fig3 is not None
    
    # 3. Model artifact and prediction
    artifact = load_model_artifact()
    assert artifact is not None
    pred = predict_transaction_type(amount=150.0, tx_date=date.today(), artifact=artifact)
    assert pred["prediction"] in ["Income", "Expense"]
    
    # 4. Budget performance
    budgets = calculate_budget_performance(df)
    assert len(budgets) > 0
    fig4 = create_budget_variance_chart(budgets)
    assert fig4 is not None
    
    # 5. Goals
    goals = load_goals()
    assert isinstance(goals, list)
