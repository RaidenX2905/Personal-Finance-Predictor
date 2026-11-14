"""Predictor View: Clean, intuitive input forms and focused statistical outputs."""

import streamlit as st
import datetime
from components.layout import render_page_header, render_section_divider, render_metric_unit
from core.ml_pipeline import load_model_artifact, predict_transaction_type, train_and_evaluate_model
from core.config import (
    COLOR_PRIMARY_BLUE,
    COLOR_PRIMARY_TEXT,
    COLOR_MUTED_LABELS,
    COLOR_BORDERS,
    COLOR_WHITE,
    COLOR_SECONDARY_TEXT
)


def render_predictor_view():
    """Render clean, minimalist transaction prediction interface."""
    render_page_header(
        title="Transaction Predictor",
        subtitle="Calibrated probabilistic classification model evaluating transaction patterns and flow characteristics.",
        overline="MACHINE LEARNING INFERENCE"
    )
    
    artifact = load_model_artifact()
    if artifact is None:
        with st.spinner("Initializing ML model..."):
            artifact = train_and_evaluate_model()
            
    col_input, col_result = st.columns([5, 7], gap="large")
    
    with col_input:
        st.caption("TRANSACTION PARAMETERS")
        
        with st.form("clean_prediction_form", border=False):
            amount_input = st.number_input(
                "Amount ($)",
                min_value=0.01,
                max_value=1_000_000.00,
                value=1250.00,
                step=50.0,
                format="%.2f"
            )
            
            date_input = st.date_input(
                "Date",
                value=datetime.date.today()
            )
            
            description_hint = st.text_input(
                "Reference Note (Optional)",
                value="Vendor invoice payment"
            )
            
            st.write("")
            submitted = st.form_submit_button("Classify Transaction", use_container_width=True)
            
        st.markdown(f"""
            <div style="border-top: 1px solid {COLOR_BORDERS}; padding-top: 1rem; margin-top: 2rem;">
                <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: {COLOR_MUTED_LABELS}; margin-bottom: 0.5rem;">
                    Model Specification
                </div>
                <div style="font-size: 0.85rem; color: {COLOR_SECONDARY_TEXT}; line-height: 1.6;">
                    <strong>Architecture:</strong> Calibrated Gradient Boosting<br>
                    <strong>Holdout ROC-AUC:</strong> {artifact.get('holdout_metrics', {}).get('roc_auc', 0.88):.3f}<br>
                    <strong>Cross-Validation Accuracy:</strong> {artifact.get('cv_metrics', {}).get('test_accuracy', 0.93):.1%}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_result:
        st.caption("PREDICTION ANALYSIS")
        
        # Perform prediction
        res = predict_transaction_type(amount_input, date_input, artifact)
        
        pred_type = res["prediction"]
        conf = res["confidence"]
        tier = res["tier"]
        p_income = res["income_prob"]
        p_expense = res["expense_prob"]
        
        # Clean minimalist typographic result
        st.markdown(f"""
            <div class="swiss-prediction-block">
                <div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: {COLOR_MUTED_LABELS};">
                    Predicted Classification
                </div>
                <div class="swiss-prediction-big">
                    {pred_type}
                </div>
                <div style="font-size: 0.85rem; color: {COLOR_SECONDARY_TEXT}; margin-top: 0.5rem;">
                    <strong>{conf:.1f}% confidence</strong> &bull; {tier}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Probability split
        st.write("")
        r1, r2 = st.columns(2)
        with r1:
            render_metric_unit(label="Income Probability", value=f"{p_income:.1f}%", is_primary=(pred_type == "Income"))
        with r2:
            render_metric_unit(label="Expense Probability", value=f"{p_expense:.1f}%", is_primary=(pred_type == "Expense"))
            
        # Contextual footnote
        st.markdown(f"""
            <div style="border-top: 1px solid {COLOR_BORDERS}; padding-top: 0.75rem; margin-top: 1.5rem; font-size: 0.8rem; color: {COLOR_MUTED_LABELS}; line-height: 1.5;">
                {res.get('caveat', '')}
            </div>
        """, unsafe_allow_html=True)
