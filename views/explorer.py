"""Data Explorer View: Streamlined query interface, clean table, and simple entry forms."""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.layout import render_page_header, render_section_divider
from core.data_manager import add_transaction, delete_transaction, import_csv_transactions
from core.config import (
    CATEGORIES_EXPENSE,
    CATEGORIES_INCOME,
    COLOR_PRIMARY_BLUE,
    COLOR_BORDERS,
    COLOR_MUTED_LABELS,
    COLOR_SECONDARY_TEXT
)


def render_explorer_view(df: pd.DataFrame):
    """Render clean, functional transaction ledger and entry manager."""
    render_page_header(
        title="Transaction Ledger",
        subtitle="Search, filter, record, or export transaction records across baseline and user datasets.",
        overline="DATA EXPLORER"
    )
    
    tab_query, tab_new, tab_io = st.tabs([
        "Ledger Query",
        "Add Transaction",
        "Import / Export"
    ])
    
    with tab_query:
        # Search & Filter bar
        f1, f2, f3, f4 = st.columns([2, 2, 3, 3])
        
        with f1:
            type_options = ["All"] + sorted(list(df["Type"].dropna().unique()))
            selected_type = st.selectbox("Type", type_options)
            
        with f2:
            cat_options = ["All"] + sorted(list(df["Category"].dropna().unique()))
            selected_cat = st.selectbox("Category", cat_options)
            
        with f3:
            min_d = df["Date"].min().date() if not df.empty else datetime.today().date()
            max_d = df["Date"].max().date() if not df.empty else datetime.today().date()
            date_range = st.date_input("Date Range", [min_d, max_d])
            
        with f4:
            search_query = st.text_input("Search", placeholder="Search description...")
            
        # Filter execution
        filtered = df.copy()
        if selected_type != "All":
            filtered = filtered[filtered["Type"] == selected_type]
        if selected_cat != "All":
            filtered = filtered[filtered["Category"] == selected_cat]
        if len(date_range) == 2:
            s_date, e_date = date_range
            filtered = filtered[(filtered["Date"].dt.date >= s_date) & (filtered["Date"].dt.date <= e_date)]
        if search_query and search_query.strip():
            q = search_query.strip().lower()
            filtered = filtered[
                filtered["Transaction Description"].str.lower().str.contains(q, na=False) |
                filtered["id"].str.lower().str.contains(q, na=False)
            ]
            
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 1.25rem 0 0.5rem 0;">
                <span style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: {COLOR_MUTED_LABELS};">
                    Showing {len(filtered):,} of {len(df):,} records
                </span>
                <span style="font-size: 0.85rem; font-weight: 600; color: {COLOR_PRIMARY_BLUE};">
                    Subtotal: ${filtered['Amount'].sum():,.2f}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        display_df = filtered[["Date", "Transaction Description", "Category", "Amount", "Type", "Source", "id"]].copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.TextColumn("Date", width="small"),
                "Transaction Description": st.column_config.TextColumn("Description", width="large"),
                "Category": st.column_config.TextColumn("Category", width="medium"),
                "Amount": st.column_config.NumberColumn("Amount", format="$%.2f", width="small"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Source": st.column_config.TextColumn("Source", width="small"),
                "id": st.column_config.TextColumn("ID", width="small")
            },
            height=480
        )
        
        user_ids = [t for t in filtered["id"].tolist() if str(t).startswith("usr_")]
        if user_ids:
            with st.expander("Delete User Transaction"):
                del_choice = st.selectbox("Select Transaction ID", user_ids)
                if st.button("Delete Record", type="primary"):
                    ok, msg = delete_transaction(del_choice)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
    with tab_new:
        st.caption("POST NEW TRANSACTION")
        
        with st.form("clean_add_form", border=False):
            c1, c2 = st.columns(2)
            with c1:
                tx_type = st.selectbox("Type", ["Expense", "Income"])
                cat_choices = CATEGORIES_EXPENSE if tx_type == "Expense" else CATEGORIES_INCOME
                tx_cat = st.selectbox("Category", cat_choices)
                tx_amount = st.number_input("Amount ($)", min_value=0.01, value=150.00, step=10.0, format="%.2f")
            with c2:
                tx_date = st.date_input("Date", value=datetime.today())
                tx_desc = st.text_input("Description", placeholder="e.g. Office Supplies")
                
            st.write("")
            create_btn = st.form_submit_button("Save Transaction", use_container_width=True)
            if create_btn:
                ok, msg = add_transaction(
                    tx_date=tx_date.strftime("%Y-%m-%d"),
                    description=tx_desc,
                    category=tx_cat,
                    amount=tx_amount,
                    tx_type=tx_type
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    with tab_io:
        c_exp, c_imp = st.columns(2, gap="large")
        with c_exp:
            st.caption("EXPORT LEDGER")
            st.write("Download current ledger view in RFC 4180 CSV format.")
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_bytes,
                file_name=f"finance_records_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with c_imp:
            st.caption("IMPORT CSV")
            st.write("Upload CSV with columns: Date, Transaction Description, Category, Amount, Type.")
            uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
            if uploaded and st.button("Import File", use_container_width=True):
                succ, fail, errs = import_csv_transactions(uploaded)
                if succ > 0:
                    st.success(f"Imported {succ:,} transaction(s).")
                if fail > 0:
                    st.warning(f"Skipped {fail} invalid row(s).")
                if succ > 0:
                    st.rerun()
