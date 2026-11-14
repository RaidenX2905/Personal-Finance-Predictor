"""Dashboard View: Poster Modernist Financial Intelligence publication."""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.layout import render_page_header, render_section_divider
from components.cards import render_kpi_metric, render_editorial_card
from components.charts import (
    create_income_expense_trend_chart,
    create_category_breakdown_chart,
    create_cumulative_balance_chart
)
from core.config import COLOR_BORDERS, COLOR_PRIMARY_BLUE, COLOR_PRIMARY_TEXT


def render_dashboard_view(df: pd.DataFrame):
    """Render full editorial financial intelligence overview."""
    # Header
    current_period = (
        f"{df['Date'].min().strftime('%b %Y')} – {df['Date'].max().strftime('%b %Y')}"
        if not df.empty else "NO DATA"
    )
    render_page_header(
        title="FINANCIAL INTELLIGENCE",
        subtitle="Macro portfolio balances, liquidity runway, cyclical cash flow trends, and categorical expenditure distributions.",
        index_label=f"PORTFOLIO SURVEILLANCE / {current_period}"
    )
    
    if df.empty:
        st.warning("No financial transactions discovered in local registry.")
        return
        
    # Financial Aggregations
    total_income = float(df[df["Type"] == "Income"]["Amount"].sum())
    total_expense = float(df[df["Type"] == "Expense"]["Amount"].sum())
    net_balance = total_income - total_expense
    savings_rate = (net_balance / total_income * 100.0) if total_income > 0 else 0.0
    tx_count = len(df)
    
    # Hero Metric Grid (4 columns)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_kpi_metric(
            label="NET BALANCE",
            value=f"${net_balance:,.2f}",
            secondary_text=f"{'SURPLUS' if net_balance >= 0 else 'DEFICIT'} CUMULATIVE",
            is_primary=True
        )
    with m2:
        render_kpi_metric(
            label="TOTAL INFLOWS",
            value=f"${total_income:,.2f}",
            secondary_text=f"{len(df[df['Type'] == 'Income'])} CREDIT EVENTS"
        )
    with m3:
        render_kpi_metric(
            label="TOTAL OUTFLOWS",
            value=f"${total_expense:,.2f}",
            secondary_text=f"{len(df[df['Type'] == 'Expense'])} DEBIT EVENTS"
        )
    with m4:
        render_kpi_metric(
            label="SAVINGS RATE",
            value=f"{savings_rate:.1f}%",
            secondary_text=f"{tx_count:,} TOTAL TRANSACTIONS"
        )
        
    # Visual Analytics Grid (12-Column Layout Simulation)
    render_section_divider("CASH FLOW DYNAMICS & LIQUIDITY", "01")
    
    col_chart_left, col_chart_right = st.columns([7, 5])
    
    with col_chart_left:
        st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <span class="pm-label">CHRONOLOGICAL INFLOW / OUTFLOW CYCLES</span>
            </div>
        """, unsafe_allow_html=True)
        fig_trend = create_income_expense_trend_chart(df)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_chart_right:
        st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <span class="pm-label">OUTFLOW DISTRIBUTION BY CATEGORY</span>
            </div>
        """, unsafe_allow_html=True)
        fig_cat = create_category_breakdown_chart(df)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    # Cumulative Liquidity Timeline
    render_section_divider("CUMULATIVE LIQUIDITY RUNWAY", "02")
    fig_cum = create_cumulative_balance_chart(df)
    st.plotly_chart(fig_cum, use_container_width=True)
    
    # Editorial Insights & Recent Audit Ledger
    render_section_divider("PORTFOLIO INSIGHTS & RECENT LEDGER", "03")
    
    col_insights, col_table = st.columns([4, 8])
    
    with col_insights:
        # Dynamic statistical insights
        avg_monthly_burn = total_expense / max(1, df["Month_Year"].nunique())
        top_category = (
            df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().idxmax()
            if not df[df["Type"] == "Expense"].empty else "N/A"
        )
        
        render_editorial_card(
            title="EXPENDITURE CONCENTRATION",
            text=f"The dominant budget drain is <strong>{top_category}</strong>. Restructuring discretionary contracts in this vertical directly yields the fastest liquidity expansion.",
            index="A"
        )
        render_editorial_card(
            title="AVERAGE MONTHLY BURN",
            text=f"Normalized monthly outflow sits at <strong>${avg_monthly_burn:,.2f}</strong>. Maintaining a baseline liquidity runway demands at least ${(avg_monthly_burn * 6):,.2f} in liquid reserves.",
            index="B"
        )
        render_editorial_card(
            title="DATA PROVENANCE NOTICE",
            text="Ledger includes verified user entries alongside historical baseline transactions. Provenance badges denote integrity tier.",
            index="C"
        )
        
    with col_table:
        st.markdown("""
            <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: baseline;">
                <span class="pm-label">LATEST 10 AUDITED ENTRIES</span>
                <span style="font-size: 0.72rem; color: #7A7A7A; font-weight: 700;">CHRONOLOGICAL ORDER</span>
            </div>
        """, unsafe_allow_html=True)
        
        display_sub = df[["Date", "Transaction Description", "Category", "Amount", "Type", "Source"]].head(10).copy()
        display_sub["Date"] = display_sub["Date"].dt.strftime("%Y-%m-%d")
        
        st.dataframe(
            display_sub,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
                "Date": st.column_config.TextColumn("Date"),
                "Type": st.column_config.TextColumn("Type"),
                "Source": st.column_config.TextColumn("Source")
            }
        )
