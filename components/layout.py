"""Black and White Monochromatic layout components, headers, rules, and typography."""

import os
import streamlit as st
from core.config import (
    COLOR_BG,
    COLOR_WHITE,
    COLOR_BORDERS,
    COLOR_PRIMARY_TEXT,
    COLOR_SECONDARY_TEXT,
    COLOR_MUTED_LABELS
)


def inject_custom_css():
    """Load and inject central Black and White stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, overline: str = "FINANCIAL INTELLIGENCE"):
    """Clean monochromatic architectural header."""
    st.markdown(f"""
        <div class="mono-header">
            <div class="mono-overline">{overline}</div>
            <h1 class="mono-title">{title}</h1>
            <p class="mono-subtitle">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def render_section_divider(heading: str):
    """Architectural 1px hairline rule with monospace overline."""
    st.markdown(f"""
        <div class="mono-section-rule">
            <div class="mono-section-heading">{heading}</div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_unit(label: str, value: str, subtext: str = "", is_primary: bool = False):
    """Pure typographic metric unit in black and white."""
    focus_cls = "invert-focus" if is_primary else ""
    st.markdown(f"""
        <div class="mono-metric-unit">
            <div class="mono-metric-label">{label}</div>
            <div class="mono-metric-value {focus_cls}">{value}</div>
            {f'<div class="mono-metric-sub">{subtext}</div>' if subtext else ''}
        </div>
    """, unsafe_allow_html=True)
