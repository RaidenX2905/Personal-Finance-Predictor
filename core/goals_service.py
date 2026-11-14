"""Savings goals tracking, milestone projections, and progress calculations."""

import os
import json
from datetime import datetime, date
from typing import Dict, Any, List, Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
GOALS_FILE = os.path.join(DATA_DIR, "savings_goals.json")


def load_goals() -> List[Dict[str, Any]]:
    """Load user savings goals from persistent JSON store."""
    if not os.path.exists(GOALS_FILE):
        defaults = [
            {
                "id": "goal_emergency",
                "name": "Emergency Reserve",
                "target_amount": 10000.0,
                "current_amount": 4200.0,
                "target_date": "2026-12-31",
                "category": "Security"
            },
            {
                "id": "goal_capital",
                "name": "Venture Capital Seed",
                "target_amount": 25000.0,
                "current_amount": 12500.0,
                "target_date": "2027-06-30",
                "category": "Growth"
            }
        ]
        save_goals(defaults)
        return defaults
    try:
        with open(GOALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_goals(goals: List[Dict[str, Any]]) -> bool:
    """Save goals to disk."""
    try:
        with open(GOALS_FILE, "w", encoding="utf-8") as f:
            json.dump(goals, f, indent=2)
        return True
    except Exception:
        return False


def add_goal(name: str, target_amount: float, current_amount: float, target_date: str, category: str = "General") -> Tuple[bool, str]:
    """Create a new savings goal."""
    if not name or not name.strip():
        return False, "Goal name required."
    try:
        tgt = float(target_amount)
        cur = float(current_amount)
        if tgt <= 0:
            return False, "Target amount must be positive."
        if cur < 0:
            return False, "Current saved amount cannot be negative."
    except (ValueError, TypeError):
        return False, "Invalid numeric values for amounts."
    
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."
        
    goals = load_goals()
    goals.append({
        "id": f"goal_{int(datetime.now().timestamp() * 1000)}",
        "name": name.strip(),
        "target_amount": round(tgt, 2),
        "current_amount": round(cur, 2),
        "target_date": target_date,
        "category": category.strip()
    })
    if save_goals(goals):
        return True, "Savings goal established."
    return False, "Failed to save goal."


def update_goal_progress(goal_id: str, new_current: float) -> Tuple[bool, str]:
    """Update current saved amount for an existing goal."""
    goals = load_goals()
    found = False
    for g in goals:
        if g.get("id") == goal_id:
            g["current_amount"] = max(0.0, round(float(new_current), 2))
            found = True
            break
    if not found:
        return False, "Goal not found."
    if save_goals(goals):
        return True, "Goal progress updated."
    return False, "Failed to save."


def delete_goal(goal_id: str) -> Tuple[bool, str]:
    """Remove a goal."""
    goals = load_goals()
    new_goals = [g for g in goals if g.get("id") != goal_id]
    if len(new_goals) == len(goals):
        return False, "Goal ID not found."
    if save_goals(new_goals):
        return True, "Goal deleted."
    return False, "Failed to save."
