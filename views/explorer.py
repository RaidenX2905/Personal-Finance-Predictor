"""Data Explorer View: Transaction management, CRUD, CSV I/O, search, and dense filtering."""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.layout import render_page_header, render_section_divider
from core.data_manager import (
    add_transaction,
    delete_transaction,
    import_csv_transactions,
    load_user_transactions
)
from core.config import (
    CATEGORIES_EXPENSE,
    CATEGORIES_INCOME,
    ALL_CATEGORIES,
    COLOR_PRIMARY_BLUE,
    COLOR_BORDERS,
    COLOR_WHITE
)


def render_explorer_view(df: pd.DataFrame):
    """Render dense, readable transaction explorer with functional data modifications."""
    render_page_header(
        title="DATA EXPLORER & LEDGER",
        subtitle="Dense interactive financial registry. Query historical records, execute verified journal entries, import external CSVs, and audit data integrity.",
        index_label="RECORD ARCHITECTURE / RECONCILIATION"
    )
    
    # Action Tabs: Ledger View, Record New Entry, CSV Import / Export
    tab_ledger, tab_add, tab_import = st.tabs([
        "AUDITED LEDGER QUERY",
        "RECORD TRANSACTION",
        "BATCH CSV IMPORT & EXPORT"
    ])
    
    with tab_ledger:
        # Filter controls in structured columns
        st.markdown("""
            <div style="border-top: 1px solid #C7C7C7; padding-top: 0.75rem; margin-bottom: 1rem;">
                <span class="pm-label">QUERY FILTERS</span>
            </div>
        """, unsafe_allow_html=True)
        
        f1, f2, f3, f4 = st.columns([2, 2, 3, 3])
        
        with f1:
            types_available = ["All"] + sorted(list(df["Type"].dropna().unique()))
            selected_type = st.selectbox("Transaction Type", types_available)
            
        with f2:
            cats_available = ["All"] + sorted(list(df["Category"].dropna().unique()))
            selected_cat = st.selectbox("Category", cats_available)
            
        with f3:
            min_date = df["Date"].min().date() if not df.empty else datetime.today().date()
            max_date = df["Date"].max().date() if not df.empty else datetime.today().date()
            date_range = st.date_input("Date Range", [min_date, max_date])
            
        with f4:
            search_query = st.text_input("Search Description / ID", placeholder="Search transactions...")
            
        # Filter logic
        filtered_df = df.copy()
        
        if selected_type != "All":
            filtered_df = filtered_df[filtered_df["Type"] == selected_type]
            
        if selected_cat != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_cat]
            
        if len(date_range) == 2:
            s_date, e_date = date_range
            filtered_df = filtered_df[
                (filtered_df["Date"].dt.date >= s_date) & 
                (filtered_df["Date"].dt.date <= e_date)
            ]
            
        if search_query and search_query.strip():
            q = search_query.strip().lower()
            filtered_df = filtered_df[
                filtered_df["Transaction Description"].str.lower().str.contains(q, na=False) |
                filtered_df["id"].str.lower().str.contains(q, na=False)
            ]
            
        # Summary row
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 1rem 0 0.5rem 0;">
                <span class="pm-label">MATCHING ENTRIES: {len(filtered_df):,} / {len(df):,} TOTAL</span>
                <span style="font-size: 0.85rem; font-weight: 700; color: {COLOR_PRIMARY_BLUE};">
                    SUBTOTAL: ${filtered_df['Amount'].sum():,.2f}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Display dense dataframe
        display_df = filtered_df[["id", "Date", "Transaction Description", "Category", "Amount", "Type", "Source"]].copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("Identifier", width="medium"),
                "Amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
                "Date": st.column_config.TextColumn("Posting Date"),
                "Transaction Description": st.column_config.TextColumn("Description", width="large"),
                "Source": st.column_config.TextColumn("Integrity Tier")
            },
            height=500
        )
        
        # Deletion for user records
        user_records = [t for t in filtered_df["id"].tolist() if str(t).startswith("usr_")]
        if user_records:
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            with st.expander("MANAGE / REMOVE USER RECORD"):
                del_id = st.selectbox("Select User Transaction ID to Remove", user_records)
                if st.button("DELETE USER RECORD", type="primary"):
                    ok, msg = delete_transaction(del_id)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
    with tab_add:
        st.markdown("""
            <div style="border-top: 1px solid #C7C7C7; padding-top: 0.75rem; margin-bottom: 1.5rem;">
                <span class="pm-label">POST VERIFIED JOURNAL ENTRY</span>
            </div>
        """, unsafe_allow_html=True)
        
        col_form, col_hint = st.columns([7, 5], gap="large")
        
        with col_form:
            with st.form("add_transaction_form", border=False):
                tx_type = st.selectbox("Flow Type", ["Expense", "Income"])
                
                cat_choices = CATEGORIES_EXPENSE if tx_type == "Expense" else CATEGORIES_INCOME
                tx_cat = st.selectbox("Category Allocation", cat_choices)
                
                tx_amount = st.number_input("Amount ($)", min_value=0.01, value=125.00, step=5.0, format="%.2f")
                tx_date = st.date_input("Transaction Date", value=datetime.today())
                tx_desc = st.text_input("Transaction Description", placeholder="e.g. AWS Cloud Infrastructure")
                
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                create_submit = st.form_submit_button("COMMITT TO PERSISTENT LEDGER", use_container_width=True)
                
                if create_submit:
                    success, msg = add_transaction(
                        tx_date=tx_date.strftime("%Y-%m-%d"),
                        description=tx_desc,
                        category=tx_cat,
                        amount=tx_amount,
                        tx_type=tx_type
                    )
                    if success:
                        st.success(f"{msg} Reloading ledger...")
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with col_hint:
            st.markdown(f"""
                <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem;">
                    <div class="pm-label">DATA INTEGRITY STANDARDS</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #444343; margin-top: 0.5rem;">
                        Entries recorded through this interface are written directly to <code>data/user_transactions.json</code>.
                        The baseline sample corpus remains untouched in immutable storage.
                    </p>
                    <div class="pm-label" style="margin-top: 1rem;">VERIFICATION CRITERIA</div>
                    <ul style="font-size: 0.85rem; color: #444343; padding-left: 1.2rem; line-height: 1.6;">
                        <li>Strictly positive monetary amounts.</li>
                        <li>Valid calendar posting date.</li>
                        <li>Non-empty merchant/description string.</li>
                        <li>Categorization adheres to uniform taxonomy.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
    with tab_import:
        st.markdown("""
            <div style="border-top: 1px solid #C7C7C7; padding-top: 0.75rem; margin-bottom: 1.5rem;">
                <span class="pm-label">BATCH DATA INGESTION & LEDGER EXPORT</span>
            </div>
        """, unsafe_allow_html=True)
        
        col_exp, col_imp = st.columns(2, gap="large")
        
        with col_exp:
            st.markdown(f"""
                <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem; height: 100%;">
                    <div class="pm-label">EXPORT AUDITED LEDGER</div>
                    <p class="pm-body" style="font-size: 0.9rem; margin-bottom: 1.5rem;">
                        Download current ledger snapshot in standard RFC 4180 CSV format.
                    </p>
            """, unsafe_allow_html=True)
            
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="DOWNLOAD COMPLETE CSV LEDGER",
                data=csv_data,
                file_name=f"finance_ledger_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_imp:
            st.markdown(f"""
                <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem; height: 100%;">
                    <div class="pm-label">IMPORT EXTERNAL CSV</div>
                    <p class="pm-body" style="font-size: 0.9rem; margin-bottom: 1rem;">
                        Upload CSV containing required columns: <code>Date, Transaction Description, Category, Amount, Type</code>.
                    </p>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], label_visibility="collapsed")
            if uploaded_file is not None:
                if st.button("PROCESS & INGEST CSV", use_container_width=True):
                    succ, fail, errs = import_csv_transactions(uploaded_file)
                    if succ > 0:
                        st.success(f"Successfully ingested {succ:,} transaction(s).")
                    if fail > 0:
                        st.warning(f"Skipped {fail} invalid row(s).")
                        for e in errs:
                            st.caption(f"• {e}")
                    if succ > 0:
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
