"""Minimalist, editorial layout components adhering strictly to Swiss modernist standards."""

import os
import streamlit as st
from core.config import (
    COLOR_PRIMARY_BLUE,
    COLOR_BORDERS,
    COLOR_BG,
    COLOR_PRIMARY_TEXT,
    COLOR_MUTED_LABELS,
    COLOR_SECONDARY_TEXT
)


def inject_custom_css():
    """Load and inject central Swiss Minimalist stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, overline: str = "FINANCIAL ANALYTICS"):
    """Clean, restrained editorial header."""
    st.markdown(f"""
        <div class="swiss-header">
            <div class="swiss-overline">{overline}</div>
            <h1 class="swiss-title">{title}</h1>
            <p class="swiss-subtitle">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def render_section_divider(heading: str):
    """Subtle 1px hairline rule with uppercase section heading."""
    st.markdown(f"""
        <div class="swiss-section-rule">
            <div class="swiss-section-heading">{heading}</div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_unit(label: str, value: str, subtext: str = "", is_primary: bool = False):
    """Pure typographic metric unit with top hairline rule (no cards, no shadows, no bubbles)."""
    cobalt_cls = "primary-cobalt" if is_primary else ""
    st.markdown(f"""
        <div class="swiss-metric-unit">
            <div class="swiss-metric-label">{label}</div>
            <div class="swiss-metric-value {cobalt_cls}">{value}</div>
            {f'<div class="swiss-metric-sub">{subtext}</div>' if subtext else ''}
        </div>
    """, unsafe_allow_html=True)
