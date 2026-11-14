"""Black and White Monochromatic Plotly charts: stark high contrast, clean white strokes, subtle grey fills."""

import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List

from core.config import (
    COLOR_BG,
    COLOR_WHITE,
    COLOR_BORDERS,
    COLOR_PRIMARY_TEXT,
    COLOR_SECONDARY_TEXT,
    COLOR_MUTED_LABELS
)

# Stark Black & White Plotly Base Layout
MONO_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Space Grotesk, JetBrains Mono, sans-serif",
        color="#F4F4F4",
        size=11
    ),
    margin=dict(t=30, b=25, l=10, r=10),
    xaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor="#242424",
        zerolinewidth=1,
        linecolor="#242424",
        tickfont=dict(color="#666666", size=10, family="JetBrains Mono")
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#181818",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(color="#666666", size=10, family="JetBrains Mono")
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color="#A0A0A0", size=11, family="JetBrains Mono")
    )
)


def create_income_expense_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Monthly cash flow: Stark White for Income, Deep Charcoal for Expense."""
    if df.empty:
        return go.Figure()
        
    trend_df = df.groupby(["Month_Year", "Type"])["Amount"].sum().reset_index()
    trend_df = trend_df.sort_values("Month_Year")
    pivot = trend_df.pivot(index="Month_Year", columns="Type", values="Amount").fillna(0.0)
    
    fig = go.Figure()
    
    if "Income" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Income",
            x=pivot.index,
            y=pivot["Income"],
            marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF", width=1)),
            width=0.35
        ))
        
    if "Expense" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Expense",
            x=pivot.index,
            y=pivot["Expense"],
            marker=dict(color="#2E2E2E", line=dict(color="#4A4A4A", width=1)),
            width=0.35
        ))
        
    layout = MONO_LAYOUT.copy()
    layout["barmode"] = "group"
    layout["bargap"] = 0.35
    layout["bargroupgap"] = 0.1
    layout["xaxis"]["tickangle"] = -45
    fig.update_layout(**layout)
    return fig


def create_category_breakdown_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal categorical bar chart in pure monochrome hierarchy."""
    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        return go.Figure()
        
    cat_df = exp_df.groupby("Category")["Amount"].sum().reset_index()
    cat_df = cat_df.sort_values("Amount", ascending=True)
    
    # Highest category in pure white, descending in greys
    n = len(cat_df)
    colors = []
    for i in range(n):
        if i == n - 1:
            colors.append("#FFFFFF")
        elif i >= n - 3:
            colors.append("#888888")
        else:
            colors.append("#3A3A3A")
            
    fig = go.Figure(go.Bar(
        x=cat_df["Amount"],
        y=cat_df["Category"],
        orientation="h",
        marker=dict(color=colors, line=dict(color="#242424", width=1)),
        text=[f"${x:,.0f}" for x in cat_df["Amount"]],
        textposition="outside",
        textfont=dict(color="#A0A0A0", size=10, family="JetBrains Mono")
    ))
    
    layout = MONO_LAYOUT.copy()
    layout["margin"] = dict(t=10, b=10, l=10, r=40)
    layout["xaxis"]["showgrid"] = False
    layout["yaxis"]["showgrid"] = False
    fig.update_layout(**layout)
    return fig


def create_budget_variance_chart(budget_records: List[Dict[str, Any]]) -> go.Figure:
    """Monochrome comparison of budget allocations vs actual expenditures."""
    if not budget_records:
        return go.Figure()
        
    b_df = pd.DataFrame(budget_records)
    b_df = b_df[b_df["Budget"] > 0].copy()
    
    if b_df.empty:
        return go.Figure()
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Budget Limit",
        x=b_df["Category"],
        y=b_df["Budget"],
        marker=dict(color="#2A2A2A", line=dict(color="#444444", width=1))
    ))
    fig.add_trace(go.Bar(
        name="Actual Spent",
        x=b_df["Category"],
        y=b_df["Actual"],
        marker=dict(color="#FFFFFF", line=dict(color="#FFFFFF", width=1))
    ))
    
    layout = MONO_LAYOUT.copy()
    layout["barmode"] = "group"
    layout["xaxis"]["tickangle"] = -30
    fig.update_layout(**layout)
    return fig
