"""Unit tests for transaction CRUD, storage validation, and CSV I/O."""

import os
import io
import pytest
import pandas as pd
from core.data_manager import (
    load_baseline_data,
    add_transaction,
    delete_transaction,
    load_user_transactions,
    save_user_transactions,
    get_combined_dataset,
    import_csv_transactions
)


def test_baseline_data_loading():
    df = load_baseline_data()
    assert not df.empty
    assert "Amount" in df.columns
    assert "Type" in df.columns
    assert "Date" in df.columns
    assert (df["Source"] == "Baseline").all()


def test_add_transaction_validation():
    # Invalid amount
    ok, msg = add_transaction("2026-05-01", "Coffee", "Food & Drink", -10.0, "Expense")
    assert not ok
    
    # Invalid date
    ok, msg = add_transaction("invalid-date", "Coffee", "Food & Drink", 10.0, "Expense")
    assert not ok
    
    # Invalid type
    ok, msg = add_transaction("2026-05-01", "Coffee", "Food & Drink", 10.0, "InvalidType")
    assert not ok

    # Valid transaction
    ok, msg = add_transaction("2026-05-01", "Test Cloud Server", "Utilities", 99.50, "Expense")
    assert ok
    
    txs = load_user_transactions()
    latest = txs[0]
    assert latest["Transaction Description"] == "Test Cloud Server"
    assert latest["Amount"] == 99.50
    assert latest["Type"] == "Expense"
    
    # Clean up test transaction
    delete_ok, _ = delete_transaction(latest["id"])
    assert delete_ok


def test_delete_protection_for_baseline():
    ok, msg = delete_transaction("base_10")
    assert not ok
    assert "Cannot delete baseline" in msg


def test_csv_import_validation():
    csv_content = """Date,Transaction Description,Category,Amount,Type
2026-06-01,Client Retainer,Investment,3500.00,Income
2026-06-02,Office Lease,Rent,1200.00,Expense
2026-06-03,Bad Row,Rent,-50.00,Expense
"""
    buf = io.StringIO(csv_content)
    succ, fail, errs = import_csv_transactions(buf)
    assert succ == 2
    assert fail == 1
    
    # Clean up created user transactions
    txs = load_user_transactions()
    cleaned = [t for t in txs if not t.get("Transaction Description") in ["Client Retainer", "Office Lease"]]
    save_user_transactions(cleaned)
