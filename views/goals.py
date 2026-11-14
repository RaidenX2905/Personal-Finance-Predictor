"""Savings Goals View: Capital accumulation targets, milestone projections, and progress tracking."""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.layout import render_page_header, render_section_divider
from components.cards import render_kpi_metric
from core.goals_service import (
    load_goals,
    add_goal,
    update_goal_progress,
    delete_goal
)
from core.config import (
    COLOR_PRIMARY_BLUE,
    COLOR_BORDERS,
    COLOR_WHITE,
    COLOR_PRIMARY_TEXT
)


def render_goals_view(df: pd.DataFrame):
    """Render capital goals surveillance and milestone tracking."""
    render_page_header(
        title="CAPITAL TARGETS & GOALS",
        subtitle="Long-range capital accumulation objectives, liquidity reserves, and milestone execution metrics.",
        index_label="WEALTH ACCUMULATION / HORIZON OBJECTIVES"
    )
    
    goals = load_goals()
    
    total_target = sum(g.get("target_amount", 0.0) for g in goals)
    total_saved = sum(g.get("current_amount", 0.0) for g in goals)
    aggregate_progress = (total_saved / total_target * 100.0) if total_target > 0 else 0.0
    
    # KPI Row
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        render_kpi_metric(
            label="AGGREGATE TARGET",
            value=f"${total_target:,.2f}",
            secondary_text=f"{len(goals)} ACTIVE OBJECTIVES"
        )
    with g2:
        render_kpi_metric(
            label="COMMITTED CAPITAL",
            value=f"${total_saved:,.2f}",
            secondary_text=f"EQUITY ALLOCATED",
            is_primary=True
        )
    with g3:
        render_kpi_metric(
            label="REMAINING GAP",
            value=f"${max(0.0, total_target - total_saved):,.2f}",
            secondary_text="CAPITAL DEFICIT"
        )
    with g4:
        render_kpi_metric(
            label="OVERALL COMPLETION",
            value=f"{aggregate_progress:.1f}%",
            secondary_text="FUNDING TRAJECTORY"
        )
        
    render_section_divider("ACTIVE CAPITAL ACCUMULATION PORTFOLIO", "01")
    
    if not goals:
        st.info("No savings objectives recorded. Define a target below to begin tracking.")
    else:
        # Display each goal as a clean Poster Modernist card
        for goal in goals:
            g_id = goal.get("id")
            g_name = goal.get("name", "Unnamed Goal")
            g_target = goal.get("target_amount", 0.0)
            g_current = goal.get("current_amount", 0.0)
            g_date = goal.get("target_date", "N/A")
            g_cat = goal.get("category", "General")
            pct = (g_current / g_target * 100.0) if g_target > 0 else 0.0
            
            st.markdown(f"""
                <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem; margin-bottom: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <div>
                            <span class="pm-label">{g_cat} TARGET</span>
                            <div style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; text-transform: uppercase;">{g_name}</div>
                        </div>
                        <div style="text-align: right;">
                            <span class="pm-label">TARGET DEADLINE</span>
                            <div style="font-size: 1.1rem; font-weight: 700; color: {COLOR_PRIMARY_BLUE};">{g_date}</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 1.25rem;">
                        <div style="font-size: 1.2rem; font-weight: 800;">
                            ${g_current:,.2f} <span style="font-size: 0.9rem; font-weight: 400; color: #7A7A7A;">of ${g_target:,.2f}</span>
                        </div>
                        <div style="font-size: 1.3rem; font-weight: 800; color: {COLOR_PRIMARY_BLUE};">
                            {pct:.1f}%
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Progress bar native
            st.progress(min(1.0, max(0.0, pct / 100.0)))
            
    # Management & Creation
    render_section_divider("ESTABLISH NEW OBJECTIVE / UPDATE BALANCE", "02")
    
    col_new, col_mod = st.columns(2, gap="large")
    
    with col_new:
        st.markdown(f"""
            <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem;">
                <div class="pm-label">ESTABLISH CAPITAL GOAL</div>
        """, unsafe_allow_html=True)
        
        with st.form("new_goal_form", border=False):
            g_name_in = st.text_input("Objective Name", placeholder="e.g. Liquidity Reserve")
            g_cat_in = st.selectbox("Category", ["Security", "Growth", "Real Estate", "Equipment", "Discretionary"])
            g_tgt_in = st.number_input("Target Amount ($)", min_value=1.0, value=5000.0, step=100.0, format="%.2f")
            g_cur_in = st.number_input("Initial Saved ($)", min_value=0.0, value=500.0, step=50.0, format="%.2f")
            g_dt_in = st.date_input("Target Completion Date", value=datetime.today())
            
            submit_goal = st.form_submit_button("CREATE OBJECTIVE", use_container_width=True)
            if submit_goal:
                ok, msg = add_goal(
                    name=g_name_in,
                    target_amount=g_tgt_in,
                    current_amount=g_cur_in,
                    target_date=g_dt_in.strftime("%Y-%m-%d"),
                    category=g_cat_in
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_mod:
        st.markdown(f"""
            <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem;">
                <div class="pm-label">UPDATE FUNDING LEVEL</div>
        """, unsafe_allow_html=True)
        
        if goals:
            goal_options = {g["id"]: f"{g['name']} (${g['current_amount']:,.2f} / ${g['target_amount']:,.2f})" for g in goals}
            selected_gid = st.selectbox("Select Target", options=list(goal_options.keys()), format_func=lambda x: goal_options[x])
            
            current_target_obj = next((g for g in goals if g["id"] == selected_gid), None)
            curr_val = current_target_obj.get("current_amount", 0.0) if current_target_obj else 0.0
            
            new_amount = st.number_input(
                "Updated Total Balance ($)",
                min_value=0.0,
                value=float(curr_val),
                step=50.0,
                format="%.2f"
            )
            
            c_u1, c_u2 = st.columns(2)
            with c_u1:
                if st.button("UPDATE BALANCE", use_container_width=True):
                    ok, msg = update_goal_progress(selected_gid, new_amount)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with c_u2:
                if st.button("REMOVE GOAL", type="primary", use_container_width=True):
                    ok, msg = delete_goal(selected_gid)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("No active goals to update.")
        st.markdown("</div>", unsafe_allow_html=True)
