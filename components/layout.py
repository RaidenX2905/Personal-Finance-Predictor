"""Poster Modernist reusable layout components, headers, dividers, and styling injector."""

import os
import streamlit as st
from core.config import COLOR_PRIMARY_BLUE, COLOR_BORDERS, COLOR_BG, COLOR_PRIMARY_TEXT, COLOR_MUTED_LABELS


def inject_custom_css():
    """Load and inject central Poster Modernist stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, index_label: str = "FINANCIAL INTELLIGENCE / 01"):
    """Render high-impact Poster Modernist editorial header."""
    st.markdown(f"""
        <div style="border-bottom: 1px solid {COLOR_BORDERS}; padding-bottom: 1.5rem; margin-bottom: 2rem;">
            <div class="pm-label" style="margin-bottom: 0.5rem;">{index_label}</div>
            <h1 class="pm-hero-title">{title}</h1>
            <p class="pm-body" style="max-width: 900px; margin: 0; font-size: 1.15rem;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def render_section_divider(label: str, index_num: str = ""):
    """Render architectural 1px hairline rule with category overline."""
    num_tag = f"<span style='color: {COLOR_PRIMARY_BLUE}; font-weight: 800; margin-right: 0.5rem;'>{index_num}</span>" if index_num else ""
    st.markdown(f"""
        <div style="border-top: 1px solid {COLOR_BORDERS}; margin: 2.5rem 0 1rem 0; padding-top: 0.75rem;">
            <span class="pm-label">{num_tag}{label}</span>
        </div>
    """, unsafe_allow_html=True)


def render_grid_row(meta_text: str, content_title: str):
    """Layout helper simulating 12-column grid editorial header."""
    st.markdown(f"""
        <div style="border-top: 1px solid {COLOR_BORDERS}; padding: 1rem 0 0.5rem 0; margin-top: 1.5rem;">
            <div style="display: flex; gap: 2rem;">
                <div style="flex: 0 0 25%; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: {COLOR_MUTED_LABELS};">
                    {meta_text}
                </div>
                <div style="flex: 0 0 75%;">
                    <div style="font-size: 1.3rem; font-weight: 700; text-transform: uppercase; letter-spacing: -0.02em; color: {COLOR_PRIMARY_TEXT};">
                        {content_title}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
