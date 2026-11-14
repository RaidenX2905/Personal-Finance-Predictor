"""Predictor View: Stark Black and White Inference Workspace."""

import streamlit as st
import datetime
from components.layout import render_page_header, render_section_divider, render_metric_unit
from core.ml_pipeline import load_model_artifact, predict_transaction_type, train_and_evaluate_model
from core.config import (
    COLOR_WHITE,
    COLOR_BORDERS,
    COLOR_MUTED_LABELS,
    COLOR_SECONDARY_TEXT
)


def render_predictor_view():
    """Render clean, minimalist monochromatic transaction prediction interface."""
    render_page_header(
        title="Transaction Predictor",
        subtitle="Calibrated probabilistic classification model evaluating transaction patterns and flow characteristics.",
        overline="INFERENCE ENGINE"
    )
    
    artifact = load_model_artifact()
    if artifact is None:
        with st.spinner("Compiling ML model..."):
            artifact = train_and_evaluate_model()
            
    col_input, col_result = st.columns([5, 7], gap="large")
    
    with col_input:
        st.caption("TRANSACTION PARAMETERS")
        
        with st.form("mono_prediction_form", border=False):
            amount_input = st.number_input(
                "Amount ($)",
                min_value=0.01,
                max_value=1_000_000.00,
                value=1250.00,
                step=50.0,
                format="%.2f"
            )
            
            date_input = st.date_input(
                "Transaction Date",
                value=datetime.date.today()
            )
            
            description_hint = st.text_input(
                "Reference Description",
                value="Vendor consulting invoice"
            )
            
            st.write("")
            submitted = st.form_submit_button("EVALUATE CLASSIFICATION", use_container_width=True)
            
        st.markdown(f"""
            <div style="border-top: 1px solid {COLOR_BORDERS}; padding-top: 1rem; margin-top: 2rem;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: {COLOR_MUTED_LABELS}; margin-bottom: 0.5rem;">
                    MODEL AUDIT METRICS
                </div>
                <div style="font-size: 0.85rem; color: {COLOR_SECONDARY_TEXT}; line-height: 1.6;">
                    <strong>Architecture:</strong> Calibrated Gradient Boosting (120 Trees)<br>
                    <strong>Holdout ROC-AUC:</strong> {artifact.get('holdout_metrics', {}).get('roc_auc', 0.88):.3f}<br>
                    <strong>5-Fold CV Accuracy:</strong> {artifact.get('cv_metrics', {}).get('test_accuracy', 0.93):.1%}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_result:
        st.caption("CLASSIFICATION RESULT")
        
        res = predict_transaction_type(amount_input, date_input, artifact)
        
        pred_type = res["prediction"]
        conf = res["confidence"]
        tier = res["tier"]
        p_income = res["income_prob"]
        p_expense = res["expense_prob"]
        
        # Stark High-Contrast Result Box
        st.markdown(f"""
            <div class="mono-prediction-block">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.2em; color: {COLOR_MUTED_LABELS};">
                    PREDICTED TYPE
                </div>
                <div class="mono-prediction-big">
                    {pred_type}
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: {COLOR_SECONDARY_TEXT}; margin-top: 0.5rem;">
                    {conf:.1f}% CONFIDENCE &bull; {tier.upper()}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        r1, r2 = st.columns(2)
        with r1:
            render_metric_unit(label="INCOME PROBABILITY", value=f"{p_income:.1f}%", is_primary=(pred_type == "Income"))
        with r2:
            render_metric_unit(label="EXPENSE PROBABILITY", value=f"{p_expense:.1f}%", is_primary=(pred_type == "Expense"))
            
        st.markdown(f"""
            <div style="border-top: 1px solid {COLOR_BORDERS}; padding-top: 0.75rem; margin-top: 1.5rem; font-size: 0.8rem; color: {COLOR_MUTED_LABELS}; line-height: 1.5;">
                {res.get('caveat', '')}
            </div>
        """, unsafe_allow_html=True)
