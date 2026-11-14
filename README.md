# Personal Finance Predictor

A minimalist, high-performance personal finance analytics and machine learning application built with Streamlit, Plotly, and scikit-learn.

---

## Overview

- **Financial Analytics**: Inflows, outflows, net surplus/deficit, and savings rate tracking.
- **Calibrated ML Predictor**: Gradient Boosting classifier (`CalibratedClassifierCV`) with calibrated probabilistic certainty and statistical caveat disclosures.
- **Ledger Explorer**: Search, filter, manual journal entries, and batch CSV import/export.
- **Budget Surveillance**: Category-level expenditure caps, variance tracking, and utilization rates.
- **Capital Targets**: Long-term savings goals with milestone projections.
- **Streamlit Cloud Ready**: Optimized caching (`@st.cache_data`, `@st.cache_resource`) and resource governance for zero-latency free-tier deployment.

---

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

### Run Automated Tests

```bash
pytest -v
```

### Retrain ML Pipeline

```bash
python3 train_model.py
```

---

## Tech Stack

- **Frontend & App Framework**: Streamlit
- **Data & Computations**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (Gradient Boosting, Sigmoid Calibration)
- **Visualizations**: Plotly
- **Testing**: Pytest

---

## License

MIT License
