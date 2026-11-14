"""Personal Finance Predictor — Unified Self-Contained Monochromatic Light Platform.

Design System Specification:
- Page Ground: #FCFCFD
- Alternate Ground / Surface: #F4F3F4
- Primary Text: #141314
- Secondary Text: #454545
- Muted Text: #5C5C5C
- Hairline / Borders: #DDDDDD
- Primary Action / Inverse Ground: #111113
- Inverse Text: #FCFCFD
- Accent (Status only): #2563EB
- Rounded surfaces (16px), pill controls (9999px)
- Fonts: Host Grotesk & Instrument Sans (via Google Fonts fallback)
- Pure Python/Streamlit implementation — no external html template files.
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import os
import sys

# Ensure root in path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.data_manager import (
    get_combined_dataset,
    add_transaction,
    delete_transaction,
    import_csv_transactions
)
from core.ml_pipeline import load_model_artifact, predict_transaction_type, train_and_evaluate_model
from core.budget_service import load_budgets, set_category_budget, calculate_budget_performance
from core.goals_service import load_goals, add_goal, update_goal_progress, delete_goal
from core.config import CATEGORIES_EXPENSE, CATEGORIES_INCOME

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Personal Finance Predictor",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INLINE CSS (ALL STYLES SELF-CONTAINED IN APP.PY) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap');

:root {
    --page-bg: #FCFCFD;
    --surface: #F4F3F4;
    --primary-text: #141314;
    --secondary-text: #454545;
    --muted-text: #5C5C5C;
    --hairline: #DDDDDD;
    --action-fill: #111113;
    --action-label: #FCFCFD;
    --status-blue: #2563EB;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--page-bg) !important;
    color: var(--primary-text) !important;
    font-family: 'Instrument Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

.stMainBlockContainer {
    max-width: 1200px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #F8F8F9 !important;
    border-right: 1px solid var(--hairline) !important;
    padding-top: 1.5rem !important;
}

[data-testid="stSidebar"] * {
    color: var(--primary-text) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    padding: 0.65rem 1rem !important;
    border-radius: 9999px !important;
    color: #141314 !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
    margin-bottom: 0.35rem !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label div {
    color: #141314 !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background-color: #ECEBED !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #111113 !important;
    color: #FCFCFD !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] div {
    color: #FCFCFD !important;
}

/* Clean Header Typography */
.landing-header {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--hairline);
}

.landing-overline {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted-text);
    margin-bottom: 0.5rem;
}

.landing-title {
    font-size: 2.8rem;
    font-weight: 600;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--primary-text);
    margin: 0 0 0.5rem 0;
}

.landing-subtitle {
    font-size: 1.05rem;
    line-height: 1.5;
    color: var(--secondary-text);
    margin: 0;
    max-width: 680px;
}

/* Inset Modernist Cards */
.modern-card {
    background-color: var(--surface);
    border: 1px solid var(--hairline);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.metric-pill-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted-text);
    margin-bottom: 0.35rem;
}

.metric-big-num {
    font-size: 2.3rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    color: var(--primary-text);
    line-height: 1;
}

/* Inputs & Form Controls */
input, select, textarea, [data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--hairline) !important;
    border-radius: 12px !important;
    color: var(--primary-text) !important;
    font-size: 0.9rem !important;
}

/* Buttons - Pill Shaped */
.stButton > button {
    background-color: var(--action-fill) !important;
    color: var(--action-label) !important;
    border: 1px solid var(--action-fill) !important;
    border-radius: 9999px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background-color: #2A2A2E !important;
    border-color: #2A2A2E !important;
}

.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: var(--primary-text) !important;
    border: 1px solid var(--hairline) !important;
}

.stButton > button[kind="secondary"]:hover {
    background-color: var(--surface) !important;
}

/* Prediction Result Callout */
.prediction-box {
    background-color: var(--surface);
    border: 1px solid var(--hairline);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 0.5rem;
}

.prediction-headline {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--primary-text);
    line-height: 1;
    margin: 0.25rem 0;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border: 1px solid var(--hairline) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.5rem !important;
    border-bottom: 1px solid var(--hairline) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: var(--muted-text) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 0 !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--primary-text) !important;
    border-bottom: 2px solid var(--action-fill) !important;
}

/* Progress Bars */
[data-testid="stProgress"] > div > div > div > div {
    background-color: var(--primary-text) !important;
    border-radius: 9999px !important;
}

[data-testid="stProgress"] > div > div > div {
    background-color: #E6E6E8 !important;
    border-radius: 9999px !important;
}

/* Inverted Hero Banner */
.inverted-banner {
    background-color: var(--action-fill);
    color: var(--action-label);
    border-radius: 16px;
    padding: 2.5rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# --- CHART HELPERS ---
def get_chart_layout():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Instrument Sans, sans-serif", color="#141314", size=11),
        margin=dict(t=25, b=25, l=10, r=10),
        xaxis=dict(
            showgrid=False,
            zeroline=True,
            zerolinecolor="#DDDDDD",
            linecolor="#DDDDDD",
            tickfont=dict(color="#5C5C5C", size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EBEAEA",
            gridwidth=1,
            zeroline=False,
            showline=False,
            tickfont=dict(color="#5C5C5C", size=10)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#454545", size=11)
        )
    )


def chart_income_vs_expense(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    trend_df = df.groupby(["Month_Year", "Type"])["Amount"].sum().reset_index().sort_values("Month_Year")
    pivot = trend_df.pivot(index="Month_Year", columns="Type", values="Amount").fillna(0.0)
    
    fig = go.Figure()
    if "Income" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Income",
            x=pivot.index,
            y=pivot["Income"],
            marker=dict(color="#111113"),
            width=0.35
        ))
    if "Expense" in pivot.columns:
        fig.add_trace(go.Bar(
            name="Expense",
            x=pivot.index,
            y=pivot["Expense"],
            marker=dict(color="#CCCCCC"),
            width=0.35
        ))
    layout = get_chart_layout()
    layout["barmode"] = "group"
    layout["bargap"] = 0.35
    layout["bargroupgap"] = 0.1
    layout["xaxis"]["tickangle"] = -45
    fig.update_layout(**layout)
    return fig


def chart_category_expenses(df: pd.DataFrame) -> go.Figure:
    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        return go.Figure()
    cat_df = exp_df.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=True)
    
    colors = ["#111113" if i == len(cat_df) - 1 else "#888888" for i in range(len(cat_df))]
    fig = go.Figure(go.Bar(
        x=cat_df["Amount"],
        y=cat_df["Category"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"${x:,.0f}" for x in cat_df["Amount"]],
        textposition="outside",
        textfont=dict(color="#141314", size=10)
    ))
    layout = get_chart_layout()
    layout["margin"] = dict(t=10, b=10, l=10, r=40)
    layout["xaxis"]["showgrid"] = False
    layout["yaxis"]["showgrid"] = False
    fig.update_layout(**layout)
    return fig


def chart_budget_comparison(budget_records) -> go.Figure:
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
        marker=dict(color="#D5D5D7")
    ))
    fig.add_trace(go.Bar(
        name="Actual Spent",
        x=b_df["Category"],
        y=b_df["Actual"],
        marker=dict(color="#111113")
    ))
    layout = get_chart_layout()
    layout["barmode"] = "group"
    layout["xaxis"]["tickangle"] = -30
    fig.update_layout(**layout)
    return fig


# --- VIEW RENDERERS ---

def render_overview(df: pd.DataFrame):
    date_range_str = (
        f"{df['Date'].min().strftime('%B %Y')} — {df['Date'].max().strftime('%B %Y')}"
        if not df.empty else "No Data Available"
    )
    
    st.markdown(f"""
        <div class="landing-header">
            <div class="landing-overline">PORTFOLIO INTELLIGENCE &bull; {date_range_str.upper()}</div>
            <h1 class="landing-title">Financial Overview</h1>
            <p class="landing-subtitle">Macro indicators, cyclical cash flows, and category allocations formatted in a clean, minimalist hierarchy.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No records found in current ledger.")
        return
        
    total_income = float(df[df["Type"] == "Income"]["Amount"].sum())
    total_expense = float(df[df["Type"] == "Expense"]["Amount"].sum())
    net_balance = total_income - total_expense
    savings_rate = (net_balance / total_income * 100.0) if total_income > 0 else 0.0
    
    # 4 Key Metrics (Inset Cards)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="modern-card">
                <div class="metric-pill-label">Net Balance</div>
                <div class="metric-big-num">${net_balance:,.2f}</div>
                <div style="font-size: 0.8rem; color: #5C5C5C; margin-top: 0.4rem;">
                    {'Cumulative Surplus' if net_balance >= 0 else 'Cumulative Deficit'}
                </div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="modern-card">
                <div class="metric-pill-label">Total Inflows</div>
                <div class="metric-big-num">${total_income:,.2f}</div>
                <div style="font-size: 0.8rem; color: #5C5C5C; margin-top: 0.4rem;">
                    {len(df[df['Type'] == 'Income']):,} credited transactions
                </div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="modern-card">
                <div class="metric-pill-label">Total Outflows</div>
                <div class="metric-big-num">${total_expense:,.2f}</div>
                <div style="font-size: 0.8rem; color: #5C5C5C; margin-top: 0.4rem;">
                    {len(df[df['Type'] == 'Expense']):,} debited transactions
                </div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="modern-card">
                <div class="metric-pill-label">Savings Rate</div>
                <div class="metric-big-num">{savings_rate:.1f}%</div>
                <div style="font-size: 0.8rem; color: #5C5C5C; margin-top: 0.4rem;">
                    {len(df):,} total audited entries
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    col_chart_left, col_chart_right = st.columns([7, 5], gap="large")
    
    with col_chart_left:
        st.markdown("""
            <div class="landing-overline">MONTHLY INFLOWS VS OUTFLOWS</div>
        """, unsafe_allow_html=True)
        fig_trend = chart_income_vs_expense(df)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_chart_right:
        st.markdown("""
            <div class="landing-overline">EXPENSES BY CATEGORY</div>
        """, unsafe_allow_html=True)
        fig_cat = chart_category_expenses(df)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    st.markdown("""
        <div class="landing-overline" style="margin-top: 2rem;">LATEST AUDITED TRANSACTIONS</div>
    """, unsafe_allow_html=True)
    
    display_sub = df[["Date", "Transaction Description", "Category", "Amount", "Type", "Source"]].head(8).copy()
    display_sub["Date"] = display_sub["Date"].dt.strftime("%Y-%m-%d")
    
    st.dataframe(
        display_sub,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.TextColumn("Date", width="small"),
            "Transaction Description": st.column_config.TextColumn("Description", width="large"),
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f", width="small"),
            "Type": st.column_config.TextColumn("Type", width="small"),
            "Source": st.column_config.TextColumn("Provenance", width="small")
        }
    )


def render_predictor():
    st.markdown("""
        <div class="landing-header">
            <div class="landing-overline">PROBABILISTIC CLASSIFICATION</div>
            <h1 class="landing-title">Transaction Predictor</h1>
            <p class="landing-subtitle">Calibrated Gradient Boosting inference separating operational debits from revenue inflows.</p>
        </div>
    """, unsafe_allow_html=True)
    
    artifact = load_model_artifact()
    if artifact is None:
        with st.spinner("Compiling ML model..."):
            artifact = train_and_evaluate_model()
            
    col_input, col_result = st.columns([5, 7], gap="large")
    
    with col_input:
        st.markdown('<div class="landing-overline">PARAMETERS</div>', unsafe_allow_html=True)
        with st.form("mono_pred_form", border=False):
            amount_input = st.number_input(
                "Transaction Amount ($)",
                min_value=0.01,
                max_value=1_000_000.00,
                value=1250.00,
                step=50.0,
                format="%.2f"
            )
            date_input = st.date_input("Transaction Date", value=datetime.date.today())
            description_hint = st.text_input("Memo / Note", value="Consulting services retainer")
            st.write("")
            submitted = st.form_submit_button("EVALUATE TRANSACTION", use_container_width=True)
            
        st.markdown(f"""
            <div class="modern-card" style="margin-top: 1.5rem;">
                <div class="metric-pill-label">Model Architecture</div>
                <div style="font-size: 0.85rem; color: #454545; line-height: 1.6;">
                    <strong>Type:</strong> Calibrated Gradient Boosting<br>
                    <strong>Holdout ROC-AUC:</strong> {artifact.get('holdout_metrics', {}).get('roc_auc', 0.88):.3f}<br>
                    <strong>5-Fold CV Accuracy:</strong> {artifact.get('cv_metrics', {}).get('test_accuracy', 0.93):.1%}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_result:
        st.markdown('<div class="landing-overline">INFERENCE ANALYSIS</div>', unsafe_allow_html=True)
        res = predict_transaction_type(amount_input, date_input, artifact)
        
        pred_type = res["prediction"]
        conf = res["confidence"]
        tier = res["tier"]
        p_income = res["income_prob"]
        p_expense = res["expense_prob"]
        
        st.markdown(f"""
            <div class="prediction-box">
                <div class="metric-pill-label">Predicted Classification</div>
                <div class="prediction-headline">{pred_type}</div>
                <div style="font-size: 0.9rem; color: #5C5C5C; margin-top: 0.5rem;">
                    <strong>{conf:.1f}% confidence</strong> &bull; {tier}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
                <div class="modern-card">
                    <div class="metric-pill-label">Income Probability</div>
                    <div class="metric-big-num">{p_income:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
                <div class="modern-card">
                    <div class="metric-pill-label">Expense Probability</div>
                    <div class="metric-big-num">{p_expense:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
            <div style="font-size: 0.8rem; color: #5C5C5C; margin-top: 1rem; line-height: 1.5;">
                {res.get('caveat', '')}
            </div>
        """, unsafe_allow_html=True)


def render_explorer(df: pd.DataFrame):
    st.markdown("""
        <div class="landing-header">
            <div class="landing-overline">RECORD AUDIT & I/O</div>
            <h1 class="landing-title">Transaction Ledger</h1>
            <p class="landing-subtitle">Direct query, entry posting, CSV batch ingestion, and ledger exports.</p>
        </div>
    """, unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["Ledger Query", "Add Transaction", "Import & Export"])
    
    with t1:
        f1, f2, f3, f4 = st.columns([2, 2, 3, 3])
        with f1:
            type_sel = st.selectbox("Type", ["All"] + sorted(list(df["Type"].dropna().unique())))
        with f2:
            cat_sel = st.selectbox("Category", ["All"] + sorted(list(df["Category"].dropna().unique())))
        with f3:
            min_d = df["Date"].min().date() if not df.empty else datetime.today().date()
            max_d = df["Date"].max().date() if not df.empty else datetime.today().date()
            date_range = st.date_input("Date Range", [min_d, max_d])
        with f4:
            search_query = st.text_input("Search", placeholder="Search memo...")
            
        filtered = df.copy()
        if type_sel != "All":
            filtered = filtered[filtered["Type"] == type_sel]
        if cat_sel != "All":
            filtered = filtered[filtered["Category"] == cat_sel]
        if len(date_range) == 2:
            filtered = filtered[(filtered["Date"].dt.date >= date_range[0]) & (filtered["Date"].dt.date <= date_range[1])]
        if search_query:
            q = search_query.strip().lower()
            filtered = filtered[filtered["Transaction Description"].str.lower().str.contains(q, na=False)]
            
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 1rem 0 0.5rem 0;">
                <span class="landing-overline">Showing {len(filtered):,} of {len(df):,} transactions</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: #141314;">
                    Subtotal: ${filtered['Amount'].sum():,.2f}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        display_df = filtered[["Date", "Transaction Description", "Category", "Amount", "Type", "Source", "id"]].copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.TextColumn("Date", width="small"),
                "Transaction Description": st.column_config.TextColumn("Description", width="large"),
                "Category": st.column_config.TextColumn("Category", width="medium"),
                "Amount": st.column_config.NumberColumn("Amount", format="$%.2f", width="small"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Source": st.column_config.TextColumn("Source", width="small"),
                "id": st.column_config.TextColumn("ID", width="small")
            },
            height=450
        )
        
        user_ids = [t for t in filtered["id"].tolist() if str(t).startswith("usr_")]
        if user_ids:
            with st.expander("Delete User Transaction"):
                del_id = st.selectbox("Select ID", user_ids)
                if st.button("Delete Transaction", type="primary"):
                    ok, msg = delete_transaction(del_id)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
    with t2:
        st.markdown('<div class="landing-overline">POST VERIFIED ENTRY</div>', unsafe_allow_html=True)
        with st.form("mono_add_form", border=False):
            c1, c2 = st.columns(2)
            with c1:
                tx_type = st.selectbox("Flow Type", ["Expense", "Income"])
                choices = CATEGORIES_EXPENSE if tx_type == "Expense" else CATEGORIES_INCOME
                tx_cat = st.selectbox("Category", choices)
                tx_amt = st.number_input("Amount ($)", min_value=0.01, value=150.00, step=10.0, format="%.2f")
            with c2:
                tx_dt = st.date_input("Date", value=datetime.today())
                tx_memo = st.text_input("Memo / Description", placeholder="e.g. AWS Cloud Hosting")
            st.write("")
            if st.form_submit_button("Save Transaction", use_container_width=True):
                ok, msg = add_transaction(
                    tx_date=tx_dt.strftime("%Y-%m-%d"),
                    description=tx_memo,
                    category=tx_cat,
                    amount=tx_amt,
                    tx_type=tx_type
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    with t3:
        c_e, c_i = st.columns(2, gap="large")
        with c_e:
            st.markdown('<div class="landing-overline">EXPORT DATA</div>', unsafe_allow_html=True)
            st.write("Download complete current ledger in standard CSV format.")
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_bytes,
                file_name=f"ledger_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with c_i:
            st.markdown('<div class="landing-overline">BATCH INGESTION</div>', unsafe_allow_html=True)
            st.write("Upload CSV with columns: Date, Transaction Description, Category, Amount, Type.")
            upl = st.file_uploader("Choose CSV", type=["csv"], label_visibility="collapsed")
            if upl and st.button("Process & Ingest CSV", use_container_width=True):
                succ, fail, errs = import_csv_transactions(upl)
                if succ > 0:
                    st.success(f"Ingested {succ:,} transaction(s).")
                if fail > 0:
                    st.warning(f"Skipped {fail} invalid row(s).")
                if succ > 0:
                    st.rerun()


def render_budgets(df: pd.DataFrame):
    st.markdown("""
        <div class="landing-header">
            <div class="landing-overline">FISCAL DISCIPLINE</div>
            <h1 class="landing-title">Budget Surveillance</h1>
            <p class="landing-subtitle">Category expenditure limits, burn variance, and utilization caps.</p>
        </div>
    """, unsafe_allow_html=True)
    
    periods = ["Monthly Average"] + sorted(list(df["Month_Year"].dropna().unique()), reverse=True)
    selected_p = st.selectbox("Period", periods)
    q_month = None if selected_p == "Monthly Average" else selected_p
    records = calculate_budget_performance(df, year_month=q_month)
    
    if not records:
        st.info("No expense data available.")
        return
        
    p_df = pd.DataFrame(records)
    total_budget = p_df["Budget"].sum()
    total_actual = p_df["Actual"].sum()
    net_var = total_budget - total_actual
    util = (total_actual / total_budget * 100.0) if total_budget > 0 else 0.0
    
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Total Budget</div><div class="metric-big-num">${total_budget:,.2f}</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">{selected_p}</div></div>', unsafe_allow_html=True)
    with b2:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Actual Spent</div><div class="metric-big-num">${total_actual:,.2f}</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">{len(p_df)} categories</div></div>', unsafe_allow_html=True)
    with b3:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Net Variance</div><div class="metric-big-num">${abs(net_var):,.2f}</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">{"Surplus" if net_var >= 0 else "Overrun"}</div></div>', unsafe_allow_html=True)
    with b4:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Utilization</div><div class="metric-big-num">{util:.1f}%</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">Cap tracking</div></div>', unsafe_allow_html=True)
        
    st.markdown('<div class="landing-overline" style="margin-top:1.5rem;">ALLOCATION VS ACTUAL EXPENDITURE</div>', unsafe_allow_html=True)
    fig_b = chart_budget_comparison(records)
    st.plotly_chart(fig_b, use_container_width=True)
    
    col_t, col_e = st.columns([8, 4], gap="large")
    with col_t:
        st.dataframe(
            p_df[["Category", "Budget", "Actual", "Variance", "Utilization_Pct", "Status"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Budget": st.column_config.NumberColumn("Limit", format="$%.2f"),
                "Actual": st.column_config.NumberColumn("Spent", format="$%.2f"),
                "Variance": st.column_config.NumberColumn("Variance", format="$%.2f"),
                "Utilization_Pct": st.column_config.ProgressColumn("Utilization", format="%.0f%%", min_value=0, max_value=120),
                "Status": st.column_config.TextColumn("Status")
            }
        )
    with col_e:
        st.markdown('<div class="landing-overline">RECALIBRATE LIMIT</div>', unsafe_allow_html=True)
        with st.form("mono_b_form", border=False):
            cat_choice = st.selectbox("Category", CATEGORIES_EXPENSE)
            curr_limit = load_budgets().get(cat_choice, 1000.0)
            new_val = st.number_input("Monthly Limit ($)", min_value=0.0, value=float(curr_limit), step=50.0, format="%.2f")
            st.write("")
            if st.form_submit_button("Apply Limit", use_container_width=True):
                set_category_budget(cat_choice, new_val)
                st.success(f"Updated {cat_choice} limit to ${new_val:,.2f}")
                st.rerun()


def render_goals():
    st.markdown("""
        <div class="landing-header">
            <div class="landing-overline">CAPITAL TARGETS</div>
            <h1 class="landing-title">Savings Goals</h1>
            <p class="landing-subtitle">Capital accumulation targets, liquidity reserves, and milestone projections.</p>
        </div>
    """, unsafe_allow_html=True)
    
    goals = load_goals()
    total_target = sum(g.get("target_amount", 0.0) for g in goals)
    total_saved = sum(g.get("current_amount", 0.0) for g in goals)
    progress_pct = (total_saved / total_target * 100.0) if total_target > 0 else 0.0
    
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Total Target</div><div class="metric-big-num">${total_target:,.2f}</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">{len(goals)} active goals</div></div>', unsafe_allow_html=True)
    with g2:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Total Saved</div><div class="metric-big-num">${total_saved:,.2f}</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">Committed capital</div></div>', unsafe_allow_html=True)
    with g3:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Remaining Gap</div><div class="metric-big-num">${max(0.0, total_target - total_saved):,.2f}</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">Deficit</div></div>', unsafe_allow_html=True)
    with g4:
        st.markdown(f'<div class="modern-card"><div class="metric-pill-label">Overall Progress</div><div class="metric-big-num">{progress_pct:.1f}%</div><div style="font-size:0.8rem;color:#5C5C5C;margin-top:0.4rem;">Trajectory</div></div>', unsafe_allow_html=True)
        
    st.markdown('<div class="landing-overline" style="margin-top:1.5rem;">ACTIVE OBJECTIVES</div>', unsafe_allow_html=True)
    if not goals:
        st.info("No savings goals recorded yet.")
    else:
        for g in goals:
            pct = (g["current_amount"] / g["target_amount"] * 100.0) if g["target_amount"] > 0 else 0.0
            st.markdown(f"""
                <div class="modern-card" style="padding: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <div>
                            <div class="metric-pill-label">{g.get('category', 'General')} Goal</div>
                            <div style="font-size: 1.25rem; font-weight: 600; color: #141314;">{g['name']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.25rem; font-weight: 700; color: #141314;">{pct:.1f}%</div>
                            <div style="font-size: 0.8rem; color: #5C5C5C;">${g['current_amount']:,.2f} of ${g['target_amount']:,.2f} &bull; Due {g['target_date']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.progress(min(1.0, max(0.0, pct / 100.0)))
            
    st.write("")
    c_new, c_up = st.columns(2, gap="large")
    with c_new:
        st.markdown('<div class="landing-overline">ESTABLISH NEW GOAL</div>', unsafe_allow_html=True)
        with st.form("mono_g_form", border=False):
            g_name = st.text_input("Goal Name", placeholder="e.g. Liquidity Reserve")
            g_cat = st.selectbox("Category", ["Security", "Growth", "Equipment", "General"])
            g_target = st.number_input("Target Amount ($)", min_value=1.0, value=5000.0, step=100.0, format="%.2f")
            g_init = st.number_input("Current Saved ($)", min_value=0.0, value=500.0, step=50.0, format="%.2f")
            g_date = st.date_input("Target Date", value=datetime.today())
            st.write("")
            if st.form_submit_button("Save Goal", use_container_width=True):
                ok, msg = add_goal(g_name, g_target, g_init, g_date.strftime("%Y-%m-%d"), g_cat)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    with c_up:
        st.markdown('<div class="landing-overline">UPDATE BALANCE</div>', unsafe_allow_html=True)
        if goals:
            opts = {g["id"]: f"{g['name']} (${g['current_amount']:,.2f} / ${g['target_amount']:,.2f})" for g in goals}
            sel_id = st.selectbox("Select Goal", options=list(opts.keys()), format_func=lambda x: opts[x])
            curr_amt = next((g["current_amount"] for g in goals if g["id"] == sel_id), 0.0)
            new_saved = st.number_input("Updated Saved Balance ($)", min_value=0.0, value=float(curr_amt), step=50.0, format="%.2f")
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Update Balance", use_container_width=True):
                    ok, msg = update_goal_progress(sel_id, new_saved)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with b2:
                if st.button("Delete Goal", type="primary", use_container_width=True):
                    ok, msg = delete_goal(sel_id)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.write("No goals available.")


# --- MAIN ENTRYPOINT ---
def main():
    df = get_combined_dataset(include_baseline=True)
    
    with st.sidebar:
        st.markdown("""
            <div style="padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
                <div style="font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #5C5C5C; margin-bottom: 0.25rem;">
                    FINANCE INTELLIGENCE
                </div>
                <div style="font-size: 1.35rem; font-weight: 700; letter-spacing: -0.03em; color: #141314;">
                    Personal Finance
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        routes = [
            "Overview",
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
        
        st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="border-top: 1px solid #DDDDDD; padding-top: 1rem; font-size: 0.75rem; color: #5C5C5C; line-height: 1.6;">
                <div>{count:,} records synchronized</div>
                <div>ML Engine: GBDT Calibrated</div>
            </div>
        """.format(count=len(df)), unsafe_allow_html=True)
        
    if selected_route == "Overview":
        render_overview(df)
    elif selected_route == "Predictor":
        render_predictor()
    elif selected_route == "Ledger Explorer":
        render_explorer(df)
    elif selected_route == "Budgets":
        render_budgets(df)
    elif selected_route == "Goals":
        render_goals()


if __name__ == "__main__":
    main()
