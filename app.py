"""Personal Finance Predictor — Streamlit Entrypoint.

Pure Black & White Monochromatic Architectural Interface:
- Background: #000000
- Borders: #242424
- Primary Text: #F4F4F4
- Active Elements & Highlights: #FFFFFF
- Clean typographic scale: Space Grotesk + JetBrains Mono
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
    page_title="Personal Finance Predictor",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Monochromatic CSS
inject_custom_css()


def main():
    df = get_combined_dataset(include_baseline=True)
    
    with st.sidebar:
        st.markdown("""
            <div style="padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #666666; margin-bottom: 0.25rem;">
                    FINANCIAL INTELLIGENCE
                </div>
                <div style="font-size: 1.35rem; font-weight: 700; letter-spacing: -0.03em; color: #FFFFFF; text-transform: uppercase;">
                    Personal Finance
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        routes = [
            "Overview",
            "Predictor",
            "Ledger Explorer",
            "Budgets",
            "Capital Goals"
        ]
        
        selected_route = st.radio(
            "Navigation",
            routes,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="border-top: 1px solid #242424; padding-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #666666; line-height: 1.6;">
                <div>{count:,} RECORDS SYNCHRONIZED</div>
                <div>ML ENGINE: GBDT CALIBRATED</div>
            </div>
        """.format(count=len(df)), unsafe_allow_html=True)
        
    if selected_route == "Overview":
        render_dashboard_view(df)
    elif selected_route == "Predictor":
        render_predictor_view()
    elif selected_route == "Ledger Explorer":
        render_explorer_view(df)
    elif selected_route == "Budgets":
        render_budgets_view(df)
    elif selected_route == "Capital Goals":
        render_goals_view(df)


if __name__ == "__main__":
    main()
