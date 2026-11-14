"""Data persistence, transaction management, and dataset handling."""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Optional, Tuple, Dict, Any, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USER_TRANSACTIONS_FILE = os.path.join(DATA_DIR, "user_transactions.json")
BASELINE_CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Personal_Finance_Dataset.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def load_baseline_data() -> pd.DataFrame:
    """Load baseline historical CSV dataset with cleaned columns and types."""
    if not os.path.exists(BASELINE_CSV_FILE):
        return pd.DataFrame(columns=["Date", "Transaction Description", "Category", "Amount", "Type", "Source"])
    
    df = pd.read_csv(BASELINE_CSV_FILE)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Type"] = df["Type"].astype(str).str.strip()
    df["Transaction Description"] = df["Transaction Description"].astype(str).str.strip()
    df["Source"] = "Baseline"
    df["id"] = ["base_" + str(i) for i in range(len(df))]
    return df.dropna(subset=["Date"])


def load_user_transactions() -> List[Dict[str, Any]]:
    """Load persistent user-created transactions from JSON store."""
    if not os.path.exists(USER_TRANSACTIONS_FILE):
        return []
    try:
        with open(USER_TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_user_transactions(transactions: List[Dict[str, Any]]) -> bool:
    """Persist user transactions to disk."""
    try:
        with open(USER_TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=2, default=str)
        return True
    except Exception:
        return False


def get_combined_dataset(include_baseline: bool = True) -> pd.DataFrame:
    """Combine baseline demo data and persistent user records with provenance labels."""
    user_txs = load_user_transactions()
    user_df = pd.DataFrame(user_txs)
    
    if not user_df.empty:
        user_df["Date"] = pd.to_datetime(user_df["Date"], errors="coerce")
        user_df["Amount"] = pd.to_numeric(user_df["Amount"], errors="coerce").fillna(0.0)
        user_df["Source"] = "User"
        if "id" not in user_df.columns:
            user_df["id"] = ["usr_" + str(i) for i in range(len(user_df))]
    else:
        user_df = pd.DataFrame(columns=["id", "Date", "Transaction Description", "Category", "Amount", "Type", "Source"])
    
    if include_baseline:
        base_df = load_baseline_data()
        combined = pd.concat([user_df, base_df], ignore_index=True)
    else:
        combined = user_df
    
    if not combined.empty:
        combined["Date"] = pd.to_datetime(combined["Date"], errors="coerce")
        combined = combined.dropna(subset=["Date"])
        combined["Month_Year"] = combined["Date"].dt.to_period("M").astype(str)
        combined = combined.sort_values("Date", ascending=False).reset_index(drop=True)
    return combined


def add_transaction(
    tx_date: str,
    description: str,
    category: str,
    amount: float,
    tx_type: str
) -> Tuple[bool, str]:
    """Validate and append a new user transaction to persistent storage."""
    try:
        val_date = pd.to_datetime(tx_date)
    except Exception:
        return False, "Invalid date format. Use YYYY-MM-DD."
    
    if not description or not description.strip():
        return False, "Transaction description cannot be empty."
    
    try:
        val_amount = float(amount)
        if val_amount <= 0:
            return False, "Amount must be strictly positive."
    except (ValueError, TypeError):
        return False, "Amount must be a valid numeric figure."
    
    if tx_type not in ["Income", "Expense"]:
        return False, "Type must be either 'Income' or 'Expense'."
    
    new_record = {
        "id": f"usr_{int(datetime.now().timestamp() * 1000)}",
        "Date": val_date.strftime("%Y-%m-%d"),
        "Transaction Description": description.strip(),
        "Category": category.strip(),
        "Amount": round(val_amount, 2),
        "Type": tx_type,
        "Source": "User",
        "created_at": datetime.now().isoformat()
    }
    
    txs = load_user_transactions()
    txs.insert(0, new_record)
    saved = save_user_transactions(txs)
    if saved:
        return True, "Transaction recorded successfully."
    return False, "Failed to persist transaction to disk."


def delete_transaction(tx_id: str) -> Tuple[bool, str]:
    """Delete a user-created transaction by ID."""
    if not tx_id.startswith("usr_"):
        return False, "Cannot delete baseline dataset records. Only user records can be removed."
    
    txs = load_user_transactions()
    original_count = len(txs)
    txs = [t for t in txs if t.get("id") != tx_id]
    if len(txs) == original_count:
        return False, "Transaction ID not found."
    
    if save_user_transactions(txs):
        return True, "Transaction deleted successfully."
    return False, "Failed to update storage."


def import_csv_transactions(file_buffer) -> Tuple[int, int, List[str]]:
    """Parse, validate, and batch import transactions from CSV upload."""
    errors = []
    try:
        import_df = pd.read_csv(file_buffer)
    except Exception as e:
        return 0, 0, [f"Failed to read CSV: {str(e)}"]
    
    import_df.columns = import_df.columns.str.strip()
    required = ["Date", "Transaction Description", "Category", "Amount", "Type"]
    missing = [c for c in required if c not in import_df.columns]
    if missing:
        return 0, 0, [f"Missing required columns: {', '.join(missing)}"]
    
    txs = load_user_transactions()
    success_count = 0
    fail_count = 0
    
    for idx, row in import_df.iterrows():
        try:
            val_date = pd.to_datetime(row["Date"])
            val_amount = float(row["Amount"])
            val_desc = str(row["Transaction Description"]).strip()
            val_cat = str(row["Category"]).strip()
            val_type = str(row["Type"]).strip().capitalize()
            
            if val_type not in ["Income", "Expense"]:
                fail_count += 1
                errors.append(f"Row {idx+1}: Type '{val_type}' invalid.")
                continue
            if val_amount <= 0:
                fail_count += 1
                errors.append(f"Row {idx+1}: Non-positive amount.")
                continue
            
            txs.append({
                "id": f"usr_imp_{int(datetime.now().timestamp() * 1000)}_{idx}",
                "Date": val_date.strftime("%Y-%m-%d"),
                "Transaction Description": val_desc,
                "Category": val_cat,
                "Amount": round(val_amount, 2),
                "Type": val_type,
                "Source": "User",
                "created_at": datetime.now().isoformat()
            })
            success_count += 1
        except Exception as ex:
            fail_count += 1
            errors.append(f"Row {idx+1}: {str(ex)}")
            
    if success_count > 0:
        save_user_transactions(txs)
    return success_count, fail_count, errors[:10]
