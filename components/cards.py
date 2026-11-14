"""Poster Modernist metric blocks, editorial KPI units, and structured callouts."""

import streamlit as st
from core.config import (
    COLOR_PRIMARY_BLUE,
    COLOR_PRIMARY_TEXT,
    COLOR_MUTED_LABELS,
    COLOR_BORDERS,
    COLOR_WHITE,
    COLOR_SECONDARY_TEXT
)


def render_kpi_metric(
    label: str,
    value: str,
    secondary_text: str = "",
    is_primary: bool = False,
    is_positive: bool = True
):
    """Render high-contrast zero-radius metric block."""
    bg_style = f"background-color: {COLOR_WHITE};" if not is_primary else f"background-color: {COLOR_PRIMARY_BLUE}; color: {COLOR_WHITE} !important;"
    border_style = f"border: 1px solid {COLOR_BORDERS};" if not is_primary else f"border: 1px solid {COLOR_PRIMARY_BLUE};"
    num_color = COLOR_PRIMARY_TEXT if not is_primary else COLOR_WHITE
    label_color = COLOR_MUTED_LABELS if not is_primary else "#D2E2FC"
    sec_color = COLOR_SECONDARY_TEXT if not is_primary else "#E5EFFF"
    
    st.markdown(f"""
        <div style="{bg_style} {border_style} padding: 1.5rem; margin-bottom: 1rem; width: 100%;">
            <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: {label_color}; margin-bottom: 0.5rem;">
                {label}
            </div>
            <div style="font-size: clamp(1.8rem, 3vw, 3.2rem); font-weight: 800; line-height: 0.95; letter-spacing: -0.03em; color: {num_color};">
                {value}
            </div>
            {f'<div style="font-size: 0.85rem; font-weight: 500; color: {sec_color}; margin-top: 0.5rem;">{secondary_text}</div>' if secondary_text else ''}
        </div>
    """, unsafe_allow_html=True)


def render_editorial_card(title: str, text: str, index: str = ""):
    """Render structured editorial commentary card."""
    index_tag = f"<span style='color: {COLOR_PRIMARY_BLUE}; font-weight: 800; margin-right: 0.4rem;'>{index}</span>" if index else ""
    st.markdown(f"""
        <div style="background-color: {COLOR_WHITE}; border: 1px solid {COLOR_BORDERS}; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: {COLOR_MUTED_LABELS}; margin-bottom: 0.5rem;">
                {index_tag}{title}
            </div>
            <div style="font-size: 1rem; line-height: 1.5; color: {COLOR_SECONDARY_TEXT};">
                {text}
            </div>
        </div>
    """, unsafe_allow_html=True)
