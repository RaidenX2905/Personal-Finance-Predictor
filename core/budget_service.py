"""Budget management and spending cap tracking."""

import os
import json
from typing import Dict, Any, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
BUDGET_FILE = os.path.join(DATA_DIR, "budgets.json")


def load_budgets() -> Dict[str, float]:
    """Load monthly category budget limits from persistent JSON store."""
    if not os.path.exists(BUDGET_FILE):
        # Default starting budget estimates
        defaults = {
            "Food & Drink": 1500.0,
            "Rent": 1800.0,
            "Utilities": 800.0,
            "Shopping": 1000.0,
            "Entertainment": 600.0,
            "Health & Fitness": 500.0,
            "Travel": 1200.0,
            "Other Expense": 500.0
        }
        save_budgets(defaults)
        return defaults
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {k: float(v) for k, v in data.items()}
    except Exception:
        return {}


def save_budgets(budgets: Dict[str, float]) -> bool:
    """Save category budget limits."""
    try:
        with open(BUDGET_FILE, "w", encoding="utf-8") as f:
            json.dump(budgets, f, indent=2)
        return True
    except Exception:
        return False


def set_category_budget(category: str, limit: float) -> bool:
    """Set or update budget for a given category."""
    budgets = load_budgets()
    budgets[category.strip()] = max(0.0, round(float(limit), 2))
    return save_budgets(budgets)


def calculate_budget_performance(df, year_month: str = None) -> List[Dict[str, Any]]:
    """Compare actual spending against allocated budgets for a chosen month or all-time average."""
    budgets = load_budgets()
    if df.empty:
        return []
    
    exp_df = df[df["Type"] == "Expense"].copy()
    if year_month:
        exp_df = exp_df[exp_df["Month_Year"] == year_month]
        period_label = year_month
    else:
        # Average per month
        months_count = max(1, exp_df["Month_Year"].nunique())
        period_label = f"Monthly Avg ({months_count} mos)"
    
    actuals = exp_df.groupby("Category")["Amount"].sum().to_dict()
    if not year_month:
        months_count = max(1, exp_df["Month_Year"].nunique())
        actuals = {k: v / months_count for k, v in actuals.items()}
        
    records = []
    all_categories = sorted(list(set(list(budgets.keys()) + list(actuals.keys()))))
    
    for cat in all_categories:
        budget_limit = budgets.get(cat, 0.0)
        spent = actuals.get(cat, 0.0)
        variance = budget_limit - spent
        pct = (spent / budget_limit * 100.0) if budget_limit > 0 else 0.0
        records.append({
            "Category": cat,
            "Budget": round(budget_limit, 2),
            "Actual": round(spent, 2),
            "Variance": round(variance, 2),
            "Utilization_Pct": round(pct, 1),
            "Status": "Exceeded" if spent > budget_limit and budget_limit > 0 else "Within Budget" if budget_limit > 0 else "Unbudgeted",
            "Period": period_label
        })
    return records
