# Personal Finance Predictor: Comprehensive Project Audit & Architectural Specification

**Date:** 2026-11-14  
**Author:** Autonomous Senior Software Engineer, ML Engineer & Product Designer  
**Status:** Audit Complete, Implementation In-Progress

---

## 1. Executive Summary & Existing System Analysis

The **Personal Finance Predictor** application is a single-file Streamlit prototype (`app.py`, 384 lines) coupled with an offline script (`train_model.py`, 53 lines) and a synthetic transaction dataset (`Personal_Finance_Dataset.csv`, 1,500 rows).

### Identified Critical Issues & Technical Debt

1. **Dependency Breakdown**:
   - `streamlit` imported but failed due to missing system package `protobuf` (resolved via `protobuf-7.36.2`).
   - `pytest` was missing from project dependencies.
   - `requirements.txt` lacked version pinning.

2. **Machine Learning Pipeline Defects**:
   - **Feature Mismatch & Arbitrary Prediction**: The model predicts transaction type (`Income` vs `Expense`) solely based on `[log1p(Amount), Month, Day]`. Calendar day and month have virtually zero predictive power for transaction type.
   - **Dataset Inconsistency / Synthetic Artifacts**: In `Personal_Finance_Dataset.csv`, transactions labeled `Salary` are classified as `Expense` (146 rows) with small random amounts ($67 to $1,993), while `Income` only contains `Investment` and `Other`.
   - **Pickle Deserialization Risk & Version Warning**: `model.pkl` was serialized with scikit-learn 1.8.0, producing `InconsistentVersionWarning` on scikit-learn 1.9+. Raw unvalidated pickle deserialization creates security and instability risks.
   - **Data Leakage & Evaluation Gaps**: `train_model.py` trained on 100% of data with no test split, no cross-validation, no hyperparameter evaluation, and no metric reporting.
   - **Uncalibrated Confidence Presentation**: The app treated raw random forest tree voting shares (`predict_proba`) as guaranteed certainty without calibration or caveat explanations.

3. **Application & Architectural Limitations**:
   - **Monolithic `app.py`**: Presentation, state mutation, CSS styling, and data handling were tightly coupled in one 384-line file.
   - **Ephemeral / Read-Only Storage**: No support for user-created transactions, category editing, budgeting, savings goals, or dynamic dataset management.
   - **External Asset Dependency**: The prediction page requested an unauthenticated third-party icon URL (`https://cdn-icons-png.flaticon.com/...`).
   - **Generic Dark Dashboard Aesthetics**: Generic dark card styling (`#1e1e2f`, gradient pill badges, green/red status indicators, rounded cards) violated the required Poster Modernist design system.

---

## 2. Poster Modernist Design System Specification

### Palette (Strictly Enforced)
- **Background**: `#E3E2DE` (Raw canvas / archival card stock)
- **Primary Cobalt**: `#1351AA` (Strategic focus / primary action)
- **Primary Text**: `#141414` (Near-black editorial ink)
- **Secondary Text**: `#444343` (Graphite charcoal body)
- **Muted Labels**: `#7A7A7A` (Stone grey taxonomy labels)
- **Borders & Rules**: `#C7C7C7` (1px solid architectural hairline borders)

### Typography Hierarchy
- **Font Stack**: `"General Sans", "Aileron", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`
- **Hero Headings**: `font-size: clamp(3.5rem, 8vw, 8rem)`, `font-weight: 900`, `line-height: 0.85`, `letter-spacing: -0.04em`, uppercase.
- **Section Headings**: `font-size: clamp(2.2rem, 5vw, 5rem)`, `font-weight: 700`, `line-height: 0.9`, `letter-spacing: -0.03em`.
- **Body**: `1.125rem`, `font-weight: 400`, `line-height: 1.5`, `#444343`.
- **Labels / Overlines**: `0.75rem`, `font-weight: 700`, `letter-spacing: 0.2em`, uppercase, `#7A7A7A`.

### Structural Rules
- **12-Column Grid Architecture**:
  - Columns 1–3: Metadata, filters, index labels, section markers.
  - Columns 4–12: Primary analytical tables, interactive tools, visualization canvases.
- **Zero Radius (`border-radius: 0px`)**: Flat, sharp geometric planes.
- **Zero Dropshadows / Zero Gradients**: No elevation blurs, no skeuomorphic lighting.
- **1px Hairline Borders**: `#C7C7C7` separating content zones.
- **Motion**: Linear, maximum 0.3s duration, respecting `prefers-reduced-motion`.

---

## 3. Modular System Architecture

```
Personal-Finance-Predictor-main/
├── app.py                     # Streamlit entrypoint & router
├── core/
│   ├── config.py              # Design tokens, palette, typography, constant definitions
│   ├── data_manager.py        # Persistent transactions, demo vs user data store, CSV I/O
│   ├── budget_service.py      # Budget limits, category caps, and progress calculation
│   ├── goals_service.py       # Savings targets, timelines, and allocation tracking
│   └── ml_pipeline.py         # Model training, evaluation, inference, calibration & pipeline packaging
├── components/
│   ├── layout.py              # Grid headers, section dividers, metadata sidebars, CSS injection
│   ├── charts.py              # Poster Modernist Plotly figures (cobalt, monochromatic scales)
│   └── cards.py               # Sharp zero-radius metric blocks and editorial callouts
├── views/
│   ├── dashboard.py           # Editorial Financial Intelligence overview & KPIs
│   ├── predictor.py           # Cobalt-accented Transaction Classifier & confidence analyzer
│   ├── explorer.py            # Data management, transaction editing, search, filters, export/import
│   ├── budgets.py             # Category-based budget monitoring & variance analysis
│   └── goals.py               # Savings targets, timeline projections, milestone tracking
├── tests/
│   ├── test_data_manager.py   # Unit tests for transaction CRUD, filtering, CSV export/import
│   ├── test_ml_pipeline.py    # Unit tests for training, feature extraction, edge cases
│   ├── test_budget_goals.py   # Unit tests for budget tracking and savings goals
│   └── test_app_smoke.py      # End-to-end smoke verification
├── assets/
│   └── styles.css             # Unified Poster Modernist stylesheet
├── model.pkl                  # Trained scikit-learn model artifact
├── Personal_Finance_Dataset.csv # Baseline historical data
├── requirements.txt           # Clean pinned dependencies
├── PROJECT_AUDIT.md           # This comprehensive document
└── README.md                  # Complete user guide & launch command
```

---

## 4. Machine Learning Implementation Strategy

1. **Dual Classification Support**:
   - **Type Classifier (Income vs Expense)**: Preserved and improved using calibrated Gradient Boosting / Random Forest with cross-validated metrics, proper feature engineering (`Amount`, `Log_Amount`, `Month`, `Day`, `Day_of_Week`, `Is_Weekend`, `Is_Month_End`), and robust error handling.
   - **Category Classifier (Expense Sub-Category)**: High-utility ML predictor for classifying transaction text / amounts into granular budget categories (`Food & Drink`, `Rent`, `Utilities`, `Entertainment`, etc.).
2. **Responsible AI & Uncertainty Disclosure**:
   - Explicitly highlight probability distribution.
   - Explain statistical limitations (e.g., date-based periodicity vs amount-based clustering).
   - Display confidence levels with honest warnings regarding synthetic dataset artifacts.
3. **Artifact Integrity**:
   - Re-train and save with current runtime scikit-learn 1.9+ to eliminate version mismatch warnings.
   - Enforce schema validation on all inputs before inference.

---

## 5. Implementation Roadmap

- [x] Phase 1: Complete Project Reconnaissance & Audit Documentation.
- [ ] Phase 2: Core Data Management & Machine Learning Pipeline Refactoring.
- [ ] Phase 3: Poster Modernist CSS & Component Library Development.
- [ ] Phase 4: Full Multi-View Application Implementation (Dashboard, Predictor, Explorer, Budgets, Goals).
- [ ] Phase 5: Automated Testing Suite & Validation (`pytest`).
- [ ] Phase 6: Final Verification, Documentation & Handoff.
