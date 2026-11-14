"""Savings Goals View: Minimalist wealth accumulation target monitor."""

import streamlit as st
import pandas as pd
from datetime import datetime
from components.layout import render_page_header, render_section_divider, render_metric_unit
from core.goals_service import load_goals, add_goal, update_goal_progress, delete_goal
from core.config import COLOR_PRIMARY_BLUE, COLOR_BORDERS, COLOR_MUTED_LABELS


def render_goals_view(df: pd.DataFrame):
    """Render clean, functional savings goals tracker."""
    render_page_header(
        title="Savings Goals",
        subtitle="Long-range capital accumulation targets, liquidity reserves, and milestone projections.",
        overline="CAPITAL TARGETS"
    )
    
    goals = load_goals()
    total_target = sum(g.get("target_amount", 0.0) for g in goals)
    total_saved = sum(g.get("current_amount", 0.0) for g in goals)
    overall_progress = (total_saved / total_target * 100.0) if total_target > 0 else 0.0
    
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        render_metric_unit("Total Target", f"${total_target:,.2f}", f"{len(goals)} active goals")
    with g2:
        render_metric_unit("Total Saved", f"${total_saved:,.2f}", "Accumulated balance", is_primary=True)
    with g3:
        render_metric_unit("Remaining Deficit", f"${max(0.0, total_target - total_saved):,.2f}", "Capital gap")
    with g4:
        render_metric_unit("Progress", f"{overall_progress:.1f}%", "Overall execution")
        
    render_section_divider("Active Objectives")
    
    if not goals:
        st.info("No savings objectives created yet.")
    else:
        for g in goals:
            pct = (g["current_amount"] / g["target_amount"] * 100.0) if g["target_amount"] > 0 else 0.0
            st.markdown(f"""
                <div style="border-top: 1px solid {COLOR_BORDERS}; padding: 1rem 0; margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <div>
                            <span style="font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: {COLOR_MUTED_LABELS};">
                                {g.get('category', 'General')}
                            </span>
                            <div style="font-size: 1.25rem; font-weight: 700; color: #141414;">{g['name']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.1rem; font-weight: 700; color: {COLOR_PRIMARY_BLUE};">{pct:.1f}%</div>
                            <div style="font-size: 0.75rem; color: {COLOR_MUTED_LABELS};">${g['current_amount']:,.2f} of ${g['target_amount']:,.2f} &bull; Due {g['target_date']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.progress(min(1.0, max(0.0, pct / 100.0)))
            
    render_section_divider("Manage Goals")
    c_new, c_up = st.columns(2, gap="large")
    
    with c_new:
        st.caption("CREATE NEW TARGET")
        with st.form("create_goal_form", border=False):
            g_name = st.text_input("Goal Name", placeholder="e.g. Tax Reserve")
            g_cat = st.selectbox("Category", ["Security", "Growth", "Equipment", "General"])
            g_target = st.number_input("Target Amount ($)", min_value=1.0, value=5000.0, step=100.0, format="%.2f")
            g_init = st.number_input("Current Saved ($)", min_value=0.0, value=500.0, step=50.0, format="%.2f")
            g_date = st.date_input("Target Date", value=datetime.today())
            
            st.write("")
            if st.form_submit_button("Save Goal", use_container_width=True):
                ok, msg = add_goal(g_name, g_target, g_init, g_date.strftime("%Y-%m-%d"), g_cat)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    with c_up:
        st.caption("UPDATE SAVED AMOUNT")
        if goals:
            opts = {g["id"]: f"{g['name']} (${g['current_amount']:,.2f} / ${g['target_amount']:,.2f})" for g in goals}
            sel_id = st.selectbox("Select Goal", options=list(opts.keys()), format_func=lambda x: opts[x])
            curr_amt = next((g["current_amount"] for g in goals if g["id"] == sel_id), 0.0)
            
            new_saved = st.number_input("Updated Saved Balance ($)", min_value=0.0, value=float(curr_amt), step=50.0, format="%.2f")
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Update Balance", use_container_width=True):
                    ok, msg = update_goal_progress(sel_id, new_saved)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with b2:
                if st.button("Delete Goal", type="primary", use_container_width=True):
                    ok, msg = delete_goal(sel_id)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.write("No goals available.")
