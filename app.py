"""Personal Finance Predictor — Main Streamlit Application Entrypoint.

Adheres strictly to the Poster Modernist design system:
Palette: #E3E2DE, #1351AA, #141414, #444343, #7A7A7A, #C7C7C7.
Zero radius, flat surfaces, editorial typography, 12-column architectural discipline.
"""

import streamlit as st
import pandas as pd
import os
import sys

# Configure root path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from components.layout import inject_custom_css
from core.data_manager import get_combined_dataset
from core.ml_pipeline import load_model_artifact

# Views
from views.dashboard import render_dashboard_view
from views.predictor import render_predictor_view
from views.explorer import render_explorer_view
from views.budgets import render_budgets_view
from views.goals import render_goals_view


# Page Configuration
st.set_page_config(
    page_title="PERSONAL FINANCE INTELLIGENCE",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Poster Modernist CSS
inject_custom_css()


def main():
    # Load dataset with provenance tracking
    df = get_combined_dataset(include_baseline=True)
    
    # Sidebar Navigation & Context Metadata
    with st.sidebar:
        st.markdown("""
            <div style="border-bottom: 1px solid #C7C7C7; padding-bottom: 1.25rem; margin-bottom: 1.5rem;">
                <div class="pm-label">PORTFOLIO INTELLIGENCE</div>
                <div style="font-size: 1.6rem; font-weight: 900; letter-spacing: -0.03em; line-height: 0.95; text-transform: uppercase;">
                    PERSONAL FINANCE<br><span style="color: #1351AA;">PREDICTOR</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation Options
        routes = [
            "01 / PORTFOLIO DASHBOARD",
            "02 / TRANSACTION PREDICTOR",
            "03 / DATA EXPLORER & LEDGER",
            "04 / BUDGET SURVEILLANCE",
            "05 / CAPITAL GOALS"
        ]
        
        selected_route = st.radio(
            "SYSTEM NAVIGATION",
            routes,
            index=0,
            label_visibility="collapsed"
        )
        
        # System Provenance & Status Telemetry
        st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="border-top: 1px solid #C7C7C7; padding-top: 1rem;">
                <div class="pm-label">TELEMETRY & PROVENANCE</div>
                <div style="font-size: 0.8rem; line-height: 1.6; color: #444343;">
                    <strong>Design System:</strong> Poster Modernist<br>
                    <strong>ML Engine:</strong> Calibrated GBDT<br>
                    <strong>Records:</strong> {record_count:,}<br>
                    <strong>State:</strong> Synchronized
                </div>
            </div>
            <div style="margin-top: 2rem; font-size: 0.72rem; color: #7A7A7A; letter-spacing: 0.15em; text-transform: uppercase;">
                © 2026 PERSONAL FINANCE AI
            </div>
        """.format(record_count=len(df)), unsafe_allow_html=True)
        
    # Route Dispatcher
    if selected_route == "01 / PORTFOLIO DASHBOARD":
        render_dashboard_view(df)
    elif selected_route == "02 / TRANSACTION PREDICTOR":
        render_predictor_view()
    elif selected_route == "03 / DATA EXPLORER & LEDGER":
        render_explorer_view(df)
    elif selected_route == "04 / BUDGET SURVEILLANCE":
        render_budgets_view(df)
    elif selected_route == "05 / CAPITAL GOALS":
        render_goals_view(df)


if __name__ == "__main__":
    main()
