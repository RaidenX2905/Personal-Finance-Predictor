"""Swiss Minimalist Dashboard: Typographic clarity, prominent numbers, uncluttered layout."""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.layout import render_page_header, render_section_divider, render_metric_unit
from components.charts import create_income_expense_trend_chart, create_category_breakdown_chart
from core.config import COLOR_BORDERS, COLOR_PRIMARY_BLUE, COLOR_PRIMARY_TEXT, COLOR_MUTED_LABELS


def render_dashboard_view(df: pd.DataFrame):
    """Render refined minimalist financial overview."""
    date_range_str = (
        f"{df['Date'].min().strftime('%B %Y')} — {df['Date'].max().strftime('%B %Y')}"
        if not df.empty else "No Data Available"
    )
    
    render_page_header(
        title="Financial Overview",
        subtitle=f"Macro indicators, monthly income versus expenses, and categorized spending distributions.",
        overline=f"PORTFOLIO TIMELINE / {date_range_str.upper()}"
    )
    
    if df.empty:
        st.info("No records found in current ledger.")
        return
        
    # Core Aggregations
    total_income = float(df[df["Type"] == "Income"]["Amount"].sum())
    total_expense = float(df[df["Type"] == "Expense"]["Amount"].sum())
    net_balance = total_income - total_expense
    savings_rate = (net_balance / total_income * 100.0) if total_income > 0 else 0.0
    
    # 4 Essential Metrics (Clean typographic units, no cards)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_unit(
            label="Net Balance",
            value=f"${net_balance:,.2f}",
            subtext=f"{'Cumulative Surplus' if net_balance >= 0 else 'Cumulative Deficit'}",
            is_primary=True
        )
    with m2:
        render_metric_unit(
            label="Total Income",
            value=f"${total_income:,.2f}",
            subtext=f"{len(df[df['Type'] == 'Income']):,} entries"
        )
    with m3:
        render_metric_unit(
            label="Total Expenses",
            value=f"${total_expense:,.2f}",
            subtext=f"{len(df[df['Type'] == 'Expense']):,} entries"
        )
    with m4:
        render_metric_unit(
            label="Savings Rate",
            value=f"{savings_rate:.1f}%",
            subtext=f"{len(df):,} total transactions"
        )
        
    # Visual Analytics Grid
    render_section_divider("Cash Flow & Category Allocation")
    
    col_chart_left, col_chart_right = st.columns([7, 5], gap="large")
    
    with col_chart_left:
        st.caption("MONTHLY INCOME VS EXPENSES")
        fig_trend = create_income_expense_trend_chart(df)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_chart_right:
        st.caption("EXPENSES BY CATEGORY")
        fig_cat = create_category_breakdown_chart(df)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    # Recent Transactions Ledger
    render_section_divider("Recent Transactions")
    
    display_sub = df[["Date", "Transaction Description", "Category", "Amount", "Type", "Source"]].head(8).copy()
    display_sub["Date"] = display_sub["Date"].dt.strftime("%Y-%m-%d")
    
    st.dataframe(
        display_sub,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.TextColumn("Date", width="small"),
            "Transaction Description": st.column_config.TextColumn("Description", width="large"),
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f", width="small"),
            "Type": st.column_config.TextColumn("Type", width="small"),
            "Source": st.column_config.TextColumn("Source", width="small")
        }
    )
