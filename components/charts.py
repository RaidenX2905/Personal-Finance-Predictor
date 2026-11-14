"""Poster Modernist Plotly charts adhering to restrained palette, zero gradients, and clean borders."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List

from core.config import (
    COLOR_BG,
    COLOR_PRIMARY_BLUE,
    COLOR_PRIMARY_TEXT,
    COLOR_SECONDARY_TEXT,
    COLOR_MUTED_LABELS,
    COLOR_BORDERS,
    CHART_PALETTE
)

# Standard Plotly Poster Modernist Layout
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="General Sans, Aileron, Space Grotesk, sans-serif",
        color=COLOR_PRIMARY_TEXT,
        size=12
    ),
    margin=dict(t=40, b=30, l=10, r=10),
    xaxis=dict(
        showgrid=True,
        gridcolor="#D4D3CE",
        gridwidth=1,
        zeroline=True,
        zerolinecolor=COLOR_BORDERS,
        zerolinewidth=1,
        linecolor=COLOR_BORDERS,
        tickfont=dict(color=COLOR_SECONDARY_TEXT, size=11)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#D4D3CE",
        gridwidth=1,
        zeroline=True,
        zerolinecolor=COLOR_BORDERS,
        zerolinewidth=1,
        linecolor=COLOR_BORDERS,
        tickfont=dict(color=COLOR_SECONDARY_TEXT, size=11)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color=COLOR_PRIMARY_TEXT, size=11)
    )
)


def create_income_expense_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Monthly Income vs Expense comparison with cobalt and deep ink flat bars."""
    if df.empty:
        return go.Figure()
        
    trend_df = df.groupby(["Month_Year", "Type"])["Amount"].sum().reset_index()
    trend_df = trend_df.sort_values("Month_Year")
    
    # Pivot for clean multi-trace bars
    pivot = trend_df.pivot(index="Month_Year", columns="Type", values="Amount").fillna(0.0)
    
    fig = go.Figure()
    
    if "Income" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Income",
            x=pivot.index,
            y=pivot["Income"],
            marker=dict(
                color=COLOR_PRIMARY_BLUE,
                line=dict(color=COLOR_PRIMARY_BLUE, width=1)
            )
        ))
        
    if "Expense" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Expense",
            x=pivot.index,
            y=pivot["Expense"],
            marker=dict(
                color=COLOR_PRIMARY_TEXT,
                line=dict(color=COLOR_PRIMARY_TEXT, width=1)
            )
        ))
        
    layout = BASE_LAYOUT.copy()
    layout["barmode"] = "group"
    layout["bargap"] = 0.25
    layout["bargroupgap"] = 0.05
    layout["xaxis"]["tickangle"] = -45
    fig.update_layout(**layout)
    return fig


def create_category_breakdown_chart(df: pd.DataFrame) -> go.Figure:
    """Sharp editorial category bar chart (horizontal) with cobalt leading highlight."""
    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        return go.Figure()
        
    cat_df = exp_df.groupby("Category")["Amount"].sum().reset_index()
    cat_df = cat_df.sort_values("Amount", ascending=True)
    
    # Max category highlighted in Cobalt, others in charcoal shades
    colors = [COLOR_PRIMARY_BLUE if i == len(cat_df) - 1 else "#363636" for i in range(len(cat_df))]
    
    fig = go.Figure(go.Bar(
        x=cat_df["Amount"],
        y=cat_df["Category"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color=COLOR_BORDERS, width=1)
        ),
        text=[f"${x:,.0f}" for x in cat_df["Amount"]],
        textposition="outside",
        textfont=dict(color=COLOR_PRIMARY_TEXT, size=11, family="sans-serif")
    ))
    
    layout = BASE_LAYOUT.copy()
    layout["margin"] = dict(t=20, b=20, l=10, r=50)
    layout["xaxis"]["showgrid"] = False
    fig.update_layout(**layout)
    return fig


def create_cumulative_balance_chart(df: pd.DataFrame) -> go.Figure:
    """Cumulative Net Balance Timeline."""
    if df.empty:
        return go.Figure()
        
    chronological = df.sort_values("Date").copy()
    chronological["Signed_Amount"] = chronological.apply(
        lambda r: r["Amount"] if r["Type"] == "Income" else -r["Amount"], axis=1
    )
    chronological["Cumulative_Balance"] = chronological["Signed_Amount"].cumsum()
    
    # Aggregate by day
    daily = chronological.groupby(chronological["Date"].dt.date)["Cumulative_Balance"].last().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["Date"],
        y=daily["Cumulative_Balance"],
        mode="lines",
        line=dict(color=COLOR_PRIMARY_BLUE, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(19, 81, 170, 0.08)"
    ))
    
    layout = BASE_LAYOUT.copy()
    layout["showlegend"] = False
    fig.update_layout(**layout)
    return fig


def create_budget_variance_chart(budget_records: List[Dict[str, Any]]) -> go.Figure:
    """Visualizes allocated budget vs actual spending per category."""
    if not budget_records:
        return go.Figure()
        
    b_df = pd.DataFrame(budget_records)
    b_df = b_df[b_df["Budget"] > 0].copy()
    
    if b_df.empty:
        return go.Figure()
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Allocated Budget",
        x=b_df["Category"],
        y=b_df["Budget"],
        marker=dict(color="#B0AFA9", line=dict(color=COLOR_BORDERS, width=1))
    ))
    fig.add_trace(go.Bar(
        name="Actual Spending",
        x=b_df["Category"],
        y=b_df["Actual"],
        marker=dict(color=COLOR_PRIMARY_BLUE, line=dict(color=COLOR_PRIMARY_BLUE, width=1))
    ))
    
    layout = BASE_LAYOUT.copy()
    layout["barmode"] = "group"
    layout["xaxis"]["tickangle"] = -30
    fig.update_layout(**layout)
    return fig
