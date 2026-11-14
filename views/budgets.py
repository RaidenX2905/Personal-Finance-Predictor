"""Budgets View: Category expenditure caps, variance tracking, and utilization rates."""

import streamlit as st
import pandas as pd
from components.layout import render_page_header, render_section_divider
from components.cards import render_kpi_metric
from components.charts import create_budget_variance_chart
from core.budget_service import (
    load_budgets,
    set_category_budget,
    calculate_budget_performance
)
from core.config import (
    CATEGORIES_EXPENSE,
    COLOR_PRIMARY_BLUE,
    COLOR_BORDERS,
    COLOR_WHITE,
    COLOR_PRIMARY_TEXT
)


def render_budgets_view(df: pd.DataFrame):
    """Render budget surveillance and expense cap management."""
    render_page_header(
        title="BUDGET SURVEILLANCE",
        subtitle="Category-level expenditure limits, burn variance analysis, and spending discipline metrics.",
        index_label="FISCAL DISCIPLINE / CATEGORY LIMITS"
    )
    
    # Available months for selection
    available_months = ["Monthly Average"] + sorted(list(df["Month_Year"].dropna().unique()), reverse=True)
    selected_period = st.selectbox("Inspection Period", available_months)
    
    query_month = None if selected_period == "Monthly Average" else selected_period
    perf_records = calculate_budget_performance(df, year_month=query_month)
    
    if not perf_records:
        st.info("No expense data available to evaluate budget performance.")
        return
        
    p_df = pd.DataFrame(perf_records)
    total_budget = p_df["Budget"].sum()
    total_actual = p_df["Actual"].sum()
    net_variance = total_budget - total_actual
    overall_util = (total_actual / total_budget * 100.0) if total_budget > 0 else 0.0
    
    # KPI Row
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        render_kpi_metric(
            label="AGGREGATE BUDGET",
            value=f"${total_budget:,.2f}",
            secondary_text=f"ALLOCATED FOR {selected_period.upper()}"
        )
    with b2:
        render_kpi_metric(
            label="ACTUAL EXPENDITURE",
            value=f"${total_actual:,.2f}",
            secondary_text=f"{len(p_df)} CATEGORIES MONITORED",
            is_primary=True
        )
    with b3:
        render_kpi_metric(
            label="NET VARIANCE",
            value=f"${abs(net_variance):,.2f}",
            secondary_text=f"{'SURPLUS (UNDER)' if net_variance >= 0 else 'OVERRUN (DEFICIT)'}"
        )
    with b4:
        render_kpi_metric(
            label="UTILIZATION RATE",
            value=f"{overall_util:.1f}%",
            secondary_text=f"{'EXCEEDED' if overall_util > 100 else 'CONTROLLED'}"
        )
        
    render_section_divider("ALLOCATION VS EXPENDITURE COMPARISON", "01")
    fig_b = create_budget_variance_chart(perf_records)
    st.plotly_chart(fig_b, use_container_width=True)
    
    # Table & Edit Controls
    render_section_divider("CATEGORY BUDGET DETAILS & LIMIT ADJUSTMENT", "02")
    
    col_table, col_edit = st.columns([8, 4], gap="large")
    
    with col_table:
        st.dataframe(
            p_df[["Category", "Budget", "Actual", "Variance", "Utilization_Pct", "Status"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Budget": st.column_config.NumberColumn("Budget Limit ($)", format="$%.2f"),
                "Actual": st.column_config.NumberColumn("Actual Spent ($)", format="$%.2f"),
                "Variance": st.column_config.NumberColumn("Variance ($)", format="$%.2f"),
                "Utilization_Pct": st.column_config.ProgressColumn(
                    "Utilization %",
                    format="%.1f%%",
                    min_value=0,
                    max_value=150
                ),
                "Status": st.column_config.TextColumn("Status")
            }
        )
        
    with col_edit:
        st.markdown(f"""
            <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem;">
                <div class="pm-label">RECALIBRATE CATEGORY CAP</div>
                <p style="font-size: 0.85rem; color: #444343; line-height: 1.5; margin-top: 0.5rem;">
                    Update monthly spending thresholds to enforce portfolio discipline.
                </p>
        """, unsafe_allow_html=True)
        
        with st.form("budget_update_form", border=False):
            edit_cat = st.selectbox("Category", CATEGORIES_EXPENSE)
            current_budgets = load_budgets()
            current_val = current_budgets.get(edit_cat, 1000.0)
            
            new_limit = st.number_input(
                "New Monthly Limit ($)",
                min_value=0.0,
                max_value=100000.0,
                value=float(current_val),
                step=50.0,
                format="%.2f"
            )
            
            update_btn = st.form_submit_button("APPLY BUDGET LIMIT", use_container_width=True)
            if update_btn:
                set_category_budget(edit_cat, new_limit)
                st.success(f"Budget for '{edit_cat}' updated to ${new_limit:,.2f}.")
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)
