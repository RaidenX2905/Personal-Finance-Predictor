"""Budgets View: Minimalist category expenditure caps and utilization tracking."""

import streamlit as st
import pandas as pd
from components.layout import render_page_header, render_section_divider, render_metric_unit
from components.charts import create_budget_variance_chart
from core.budget_service import load_budgets, set_category_budget, calculate_budget_performance
from core.config import CATEGORIES_EXPENSE, COLOR_BORDERS, COLOR_PRIMARY_BLUE, COLOR_MUTED_LABELS


def render_budgets_view(df: pd.DataFrame):
    """Render clean, functional budget monitor."""
    render_page_header(
        title="Budget Tracking",
        subtitle="Category-level expenditure limits, utilization rates, and spending variance.",
        overline="FISCAL DISCIPLINE"
    )
    
    # Filter selection
    periods = ["Monthly Average"] + sorted(list(df["Month_Year"].dropna().unique()), reverse=True)
    c_sel, _ = st.columns([4, 8])
    with c_sel:
        selected_period = st.selectbox("Period", periods)
        
    query_month = None if selected_period == "Monthly Average" else selected_period
    records = calculate_budget_performance(df, year_month=query_month)
    
    if not records:
        st.info("No expense data available for this period.")
        return
        
    p_df = pd.DataFrame(records)
    total_budget = p_df["Budget"].sum()
    total_actual = p_df["Actual"].sum()
    net_variance = total_budget - total_actual
    overall_util = (total_actual / total_budget * 100.0) if total_budget > 0 else 0.0
    
    # Metrics row
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        render_metric_unit("Total Budget", f"${total_budget:,.2f}", selected_period)
    with b2:
        render_metric_unit("Actual Spent", f"${total_actual:,.2f}", f"{len(p_df)} categories", is_primary=True)
    with b3:
        render_metric_unit("Net Variance", f"${abs(net_variance):,.2f}", "Surplus" if net_variance >= 0 else "Overrun")
    with b4:
        render_metric_unit("Utilization", f"{overall_util:.1f}%", "Cap tracking")
        
    render_section_divider("Budget Comparison Chart")
    fig_b = create_budget_variance_chart(records)
    st.plotly_chart(fig_b, use_container_width=True)
    
    render_section_divider("Category Limits")
    col_t, col_e = st.columns([8, 4], gap="large")
    
    with col_t:
        st.dataframe(
            p_df[["Category", "Budget", "Actual", "Variance", "Utilization_Pct", "Status"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Budget": st.column_config.NumberColumn("Limit", format="$%.2f"),
                "Actual": st.column_config.NumberColumn("Spent", format="$%.2f"),
                "Variance": st.column_config.NumberColumn("Variance", format="$%.2f"),
                "Utilization_Pct": st.column_config.ProgressColumn("Utilization", format="%.0f%%", min_value=0, max_value=120),
                "Status": st.column_config.TextColumn("Status")
            }
        )
        
    with col_e:
        st.caption("SET CATEGORY LIMIT")
        with st.form("set_budget_form", border=False):
            cat_choice = st.selectbox("Category", CATEGORIES_EXPENSE)
            curr_limit = load_budgets().get(cat_choice, 1000.0)
            new_val = st.number_input("Monthly Limit ($)", min_value=0.0, value=float(curr_limit), step=50.0, format="%.2f")
            
            st.write("")
            if st.form_submit_button("Update Limit", use_container_width=True):
                set_category_budget(cat_choice, new_val)
                st.success(f"Updated {cat_choice} limit to ${new_val:,.2f}")
                st.rerun()
