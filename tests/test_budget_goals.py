"""Unit tests for budget calculation and savings goals services."""

import pytest
import pandas as pd
from core.budget_service import (
    load_budgets,
    set_category_budget,
    calculate_budget_performance
)
from core.goals_service import (
    load_goals,
    add_goal,
    update_goal_progress,
    delete_goal
)


def test_budget_service():
    set_category_budget("Test Category", 500.0)
    budgets = load_budgets()
    assert budgets.get("Test Category") == 500.0
    
    # Performance with dummy df
    dummy_df = pd.DataFrame({
        "Date": pd.to_datetime(["2026-01-10", "2026-01-15"]),
        "Category": ["Test Category", "Test Category"],
        "Amount": [200.0, 150.0],
        "Type": ["Expense", "Expense"],
        "Month_Year": ["2026-01", "2026-01"]
    })
    
    perf = calculate_budget_performance(dummy_df, year_month="2026-01")
    cat_perf = next((p for p in perf if p["Category"] == "Test Category"), None)
    assert cat_perf is not None
    assert cat_perf["Actual"] == 350.0
    assert cat_perf["Budget"] == 500.0
    assert cat_perf["Variance"] == 150.0
    assert cat_perf["Status"] == "Within Budget"


def test_goals_service():
    ok, msg = add_goal(
        name="Unit Test Fund",
        target_amount=2000.0,
        current_amount=400.0,
        target_date="2027-01-01",
        category="Security"
    )
    assert ok
    
    goals = load_goals()
    target_g = next((g for g in goals if g["name"] == "Unit Test Fund"), None)
    assert target_g is not None
    assert target_g["current_amount"] == 400.0
    
    # Update progress
    up_ok, _ = update_goal_progress(target_g["id"], 1200.0)
    assert up_ok
    
    # Delete
    del_ok, _ = delete_goal(target_g["id"])
    assert del_ok
