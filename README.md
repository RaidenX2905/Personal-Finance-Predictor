# PERSONAL FINANCE PREDICTOR
### POSTER MODERNIST FINANCIAL INTELLIGENCE PLATFORM

A refined, high-performance personal finance analytics and machine learning application crafted with strict **Poster Modernist** architectural and visual standards.

---

## 1. Quick Start & Execution

### System Requirements
- Python 3.10+ (Tested through Python 3.14)
- Virtual environment recommended

### Installation

```bash
# Clone or navigate to the repository
cd Personal-Finance-Predictor-main

# Install pinned dependencies
pip install -r requirements.txt
```

### Launch Application

Execute the following exact command:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## 2. Running Automated Tests

Run the full automated test suite covering data management, ML pipeline, budget allocations, savings goals, and visual charts:

```bash
pytest -v
```

---

## 3. Retraining the ML Pipeline

To re-run cross-validation, calibrate probabilities, and re-serialize the model artifact:

```bash
python3 train_model.py
```

- **Algorithm**: `CalibratedClassifierCV(GradientBoostingClassifier)` (120 Estimators, Sigmoid calibration).
- **Features**: `[Amount, Log_Amount, Month, Day, DayOfWeek, IsWeekend, IsMonthEnd]`.
- **Holdout ROC-AUC**: `0.8861`.
- **5-Fold Cross-Validation Accuracy**: `93.27%`.
- **Artifacts Generated**: `model.pkl` and `data/model_metrics.json`.

---

## 4. Design System & Palette

Crafted according to the **Poster Modernist** visual aesthetic:

- **Background**: `#E3E2DE` (Raw canvas / archival bond)
- **Primary Cobalt**: `#1351AA` (Strategic focal points & primary actions)
- **Primary Text**: `#141414` (Near-black editorial ink)
- **Secondary Text**: `#444343` (Charcoal body typography)
- **Muted Labels**: `#7A7A7A` (Monospace / uppercase category taxonomy)
- **Hairline Borders**: `#C7C7C7` (1px solid rules)
- **Zero Radius**: Flat surfaces, no rounded SaaS card corners (`border-radius: 0px`).
- **Zero Gradients & Shadows**: Clean flat color blocks and crisp high-contrast layout.

---

## 5. Application Features & Architecture

```
Personal-Finance-Predictor-main/
├── app.py                 # Streamlit entrypoint and route dispatcher
├── core/
│   ├── config.py          # Design tokens, color palette, categories
│   ├── data_manager.py    # Persistent user records, baseline isolation, CSV I/O
│   ├── budget_service.py  # Monthly budget caps & variance calculation
│   ├── goals_service.py   # Savings goals & progress milestones
│   └── ml_pipeline.py     # Feature engineering, calibrated model training & inference
├── components/
│   ├── layout.py          # Poster Modernist headers, rules, grid rows
│   ├── charts.py          # Restrained Plotly charts with custom palette
│   └── cards.py           # Sharp zero-radius metric blocks & editorial callouts
├── views/
│   ├── dashboard.py       # Portfolio surveillance, KPIs, and monthly trends
│   ├── predictor.py       # Calibrated transaction classifier & confidence bounds
│   ├── explorer.py        # Dense ledger query, search, add, delete, CSV import/export
│   ├── budgets.py         # Category expenditure limits & utilization rates
│   └── goals.py           # Capital target tracking & milestone updates
├── data/                  # Persistent JSON storage for user transactions & budgets
├── tests/                 # Full pytest suite
├── assets/styles.css      # Centralized Poster Modernist CSS
├── model.pkl              # Calibrated serialized ML model
├── Personal_Finance_Dataset.csv # Historical baseline corpus
├── requirements.txt       # Pinned dependencies
├── PROJECT_AUDIT.md       # Full engineering audit and architectural report
└── README.md
```

### Highlights
- **Persistent Transactions**: User-created records are safely stored in `data/user_transactions.json` without modifying the original baseline dataset.
- **Data Provenance**: Every entry clearly indicates its integrity tier (`User` vs `Baseline`).
- **Calibrated AI Predictions**: Transparent confidence levels with honest disclosure regarding synthetic training data clustering.
- **Budget Surveillance**: Real-time category cap comparison, monthly burn variance, and utilization progress.
- **Capital Accumulation Targets**: Goal tracking with target dates, milestones, and funding progress.
- **CSV Import / Export**: Complete import parser with row-level validation and RFC 4180 export.

---

## 6. Known Limitations & Responsible AI Notice
- The historical dataset (`Personal_Finance_Dataset.csv`) contains synthetic label assignments (e.g., small salary payments categorized as expenses). The calibrated ML model explicitly discloses these limitations and clarifies that semantic vendor/receipt verification is required for enterprise bookkeeping.
