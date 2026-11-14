"""Swiss Minimalist charts: Clean white/cream plotting areas, minimal gridlines, cobalt primary accents."""

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
    COLOR_BORDERS
)

# Swiss Minimalist Plotly Configuration
SWISS_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Inter, -apple-system, sans-serif",
        color=COLOR_PRIMARY_TEXT,
        size=11
    ),
    margin=dict(t=25, b=25, l=10, r=10),
    xaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor=COLOR_BORDERS,
        zerolinewidth=1,
        linecolor=COLOR_BORDERS,
        tickfont=dict(color=COLOR_MUTED_LABELS, size=10)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#DCDAD4",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(color=COLOR_MUTED_LABELS, size=10)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color=COLOR_SECONDARY_TEXT, size=11)
    )
)


def create_income_expense_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Monthly financial performance: Inflows in Cobalt, Outflows in Ink Charcoal."""
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
            marker=dict(color=COLOR_PRIMARY_BLUE),
            width=0.35
        ))
        
    if "Expense" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Expense",
            x=pivot.index,
            y=pivot["Expense"],
            marker=dict(color=COLOR_PRIMARY_TEXT),
            width=0.35
        ))
        
    layout = SWISS_LAYOUT.copy()
    layout["barmode"] = "group"
    layout["bargap"] = 0.35
    layout["bargroupgap"] = 0.1
    layout["xaxis"]["tickangle"] = -45
    fig.update_layout(**layout)
    return fig


def create_category_breakdown_chart(df: pd.DataFrame) -> go.Figure:
    """Clean, horizontal expense breakdown by category."""
    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        return go.Figure()
        
    cat_df = exp_df.groupby("Category")["Amount"].sum().reset_index()
    cat_df = cat_df.sort_values("Amount", ascending=True)
    
    # Highest category gets primary cobalt, others slate charcoal
    colors = [COLOR_PRIMARY_BLUE if i == len(cat_df) - 1 else "#5A5958" for i in range(len(cat_df))]
    
    fig = go.Figure(go.Bar(
        x=cat_df["Amount"],
        y=cat_df["Category"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"${x:,.0f}" for x in cat_df["Amount"]],
        textposition="outside",
        textfont=dict(color=COLOR_PRIMARY_TEXT, size=10, family="Inter, sans-serif")
    ))
    
    layout = SWISS_LAYOUT.copy()
    layout["margin"] = dict(t=10, b=10, l=10, r=40)
    layout["xaxis"]["showgrid"] = False
    layout["yaxis"]["showgrid"] = False
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
        name="Budget Limit",
        x=b_df["Category"],
        y=b_df["Budget"],
        marker=dict(color="#BDBBB5")
    ))
    fig.add_trace(go.Bar(
        name="Actual Spent",
        x=b_df["Category"],
        y=b_df["Actual"],
        marker=dict(color=COLOR_PRIMARY_BLUE)
    ))
    
    layout = SWISS_LAYOUT.copy()
    layout["barmode"] = "group"
    layout["xaxis"]["tickangle"] = -30
    fig.update_layout(**layout)
    return fig
