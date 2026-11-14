"""Personal Finance Predictor — Streamlit Entrypoint.

Swiss Minimalist design philosophy:
- Palette: #E3E2DE, #1351AA, #141414, #444343, #7A7A7A, #C7C7C7
- Typographic discipline (Inter, proportional hierarchy)
- Generous whitespace, zero radius, hairline 1px borders, zero card fluff
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
    page_title="Finance Analytics",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Swiss Minimalist CSS
inject_custom_css()


def main():
    df = get_combined_dataset(include_baseline=True)
    
    with st.sidebar:
        st.markdown("""
            <div style="padding-bottom: 0.5rem; margin-bottom: 1.25rem;">
                <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: #7A7A7A; margin-bottom: 0.25rem;">
                    ANALYTICS PLATFORM
                </div>
                <div style="font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; color: #141414;">
                    Personal Finance
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        routes = [
            "Dashboard",
            "Predictor",
            "Ledger Explorer",
            "Budgets",
            "Goals"
        ]
        
        selected_route = st.radio(
            "Navigation",
            routes,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="border-top: 1px solid #C7C7C7; padding-top: 1rem; font-size: 0.75rem; color: #7A7A7A; line-height: 1.6;">
                <div>{count:,} records loaded</div>
                <div>ML: Gradient Boosting</div>
            </div>
        """.format(count=len(df)), unsafe_allow_html=True)
        
    if selected_route == "Dashboard":
        render_dashboard_view(df)
    elif selected_route == "Predictor":
        render_predictor_view()
    elif selected_route == "Ledger Explorer":
        render_explorer_view(df)
    elif selected_route == "Budgets":
        render_budgets_view(df)
    elif selected_route == "Goals":
        render_goals_view(df)


if __name__ == "__main__":
    main()
