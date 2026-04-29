import streamlit as st
import pandas as pd
import numpy as np
import pickle
import datetime
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Configuration ---
st.set_page_config(page_title="Personal Finance AI", page_icon="💳", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .metric-container {
        background-color: #1e1e2f;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        text-align: center;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #a0a0b0;
        margin-bottom: 8px;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
    }
    .val-positive { color: #10b981; }
    .val-negative { color: #ef4444; }
    .val-neutral { color: #3b82f6; }
    
    /* Predictor Cards */
    .pred-card {
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    .pred-income { 
        background: linear-gradient(145deg, rgba(16,185,129,0.1) 0%, rgba(16,185,129,0.05) 100%);
        border: 2px solid rgba(16, 185, 129, 0.4); 
    }
    .pred-expense { 
        background: linear-gradient(145deg, rgba(239,68,68,0.1) 0%, rgba(239,68,68,0.05) 100%);
        border: 2px solid rgba(239, 68, 68, 0.4); 
    }
    .pred-title { 
        font-size: 1.2rem; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        color: #a0a0b0;
        margin-bottom: 10px;
    }
    .pred-result { 
        font-size: 4rem; 
        font-weight: 800; 
        margin: 10px 0; 
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .pred-conf { 
        font-size: 1.2rem; 
        opacity: 0.9; 
    }
    
    /* Tweak tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Data & Model Loading Functions ---
@st.cache_resource
def load_model():
    model_path = "model.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None

@st.cache_data
def load_data():
    csv_path = "Personal_Finance_Dataset.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna()
        # Create Month-Year format for grouping, sorting chronologically
        df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
        df = df.sort_values('Date', ascending=False)
        return df
    return None

# --- Main App ---
def main():
    model = load_model()
    df = load_data()

    # --- Sidebar Navigation ---
    with st.sidebar:
        st.title("💳 Finance AI")
        st.markdown("Intelligent finance tracking, visualization, and prediction.")
        st.divider()
        
        nav = st.radio("Navigation", [
            "📊 Dashboard Overview", 
            "🤖 Transaction Predictor", 
            "🔍 Data Explorer"
        ])
        
        st.divider()
        if df is not None:
            st.caption(f"Data Loaded: {len(df)} records")
        st.caption("© 2026 Personal Finance AI")

    # --- Route to specific pages ---
    if nav == "📊 Dashboard Overview":
        render_dashboard(df)
    elif nav == "🤖 Transaction Predictor":
        render_predictor(model)
    elif nav == "🔍 Data Explorer":
        render_data_explorer(df)


# --- Page: Dashboard ---
def render_dashboard(df):
    st.title("📊 Financial Dashboard")
    st.markdown("Get a bird's-eye view of your finances, tracking income versus expenses and analyzing your spending habits.")
    
    if df is None or df.empty:
        st.warning("No dataset found. Please ensure `Personal_Finance_Dataset.csv` is in the directory.")
        return
        
    # Calculate KPIs
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    net_balance = total_income - total_expense
    
    # KPIs Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
            <div class="metric-container">
                <div class="metric-label">Net Balance</div>
                <div class="metric-val {"val-positive" if net_balance >= 0 else "val-negative"}">${net_balance:,.2f}</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="metric-container">
                <div class="metric-label">Total Income</div>
                <div class="metric-val val-positive">${total_income:,.2f}</div>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="metric-container">
                <div class="metric-label">Total Expenses</div>
                <div class="metric-val val-negative">${total_expense:,.2f}</div>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
            <div class="metric-container">
                <div class="metric-label">Total Transactions</div>
                <div class="metric-val val-neutral">{len(df):,}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    st.write("") # Spacing
    
    # Charts Row 1
    c1, c2 = st.columns([2, 1.2])
    
    with c1:
        st.subheader("📈 Income vs Expense Trend")
        # Group by Month_Year and Type
        trend_df = df.groupby(['Month_Year', 'Type'])['Amount'].sum().reset_index()
        # Sort values properly
        trend_df = trend_df.sort_values('Month_Year')
        
        fig_trend = px.bar(
            trend_df, x='Month_Year', y='Amount', color='Type', barmode='group',
            color_discrete_map={'Income': '#10b981', 'Expense': '#ef4444'},
            labels={'Month_Year': 'Month', 'Amount': 'Amount ($)'},
            template='plotly_dark'
        )
        fig_trend.update_layout(
            xaxis_tickangle=-45, 
            margin=dict(t=20, b=0, l=0, r=0), 
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2:
        st.subheader("🛒 Expenses by Category")
        exp_df = df[df['Type'] == 'Expense']
        if not exp_df.empty:
            cat_df = exp_df.groupby('Category')['Amount'].sum().reset_index()
            fig_pie = px.pie(
                cat_df, values='Amount', names='Category', hole=0.5,
                color_discrete_sequence=px.colors.sequential.Tealgrn,
                template='plotly_dark'
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
            fig_pie.update_layout(
                margin=dict(t=20, b=0, l=0, r=0), 
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data available for categorization.")

    st.divider()

    # Recent Transactions Section
    st.subheader("📝 Recent Transactions")
    # Display the 10 most recent transactions beautifully
    display_df = df[['Date', 'Transaction Description', 'Category', 'Amount', 'Type']].copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(
        display_df.head(10), 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
        }
    )


# --- Page: AI Predictor ---
def render_predictor(model):
    st.title("🤖 AI Transaction Predictor")
    st.markdown("Leverage our trained Random Forest model to instantly classify transactions as **Income** or **Expense** based on the amount and date properties.")
    
    if model is None:
        st.error("Model not found! Please run `train_model.py` first to generate the `model.pkl` file.")
        return

    col_input, col_result = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.subheader("Transaction Details")
        with st.form("prediction_form", border=True):
            amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=150.00, step=10.0, format="%.2f")
            date_input = st.date_input("Transaction Date", value=datetime.date.today())
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🧠 Classify Transaction", use_container_width=True, type="primary")
            
    with col_result:
        st.subheader("Prediction Result")
        if submitted:
            # Preprocess features according to train_model.py
            log_amount = np.log1p(amount)
            month = date_input.month
            day = date_input.day
            
            features = [[log_amount, month, day]]
            prediction = model.predict(features)[0]
            
            # Extract probability/confidence
            try:
                proba = model.predict_proba(features)[0]
                confidence = max(proba) * 100
                conf_text = f"Confidence: {confidence:.1f}%"
            except:
                conf_text = "Confidence: N/A"

            # Render styled prediction card
            if prediction == 1:
                st.markdown(f"""
                <div class="pred-card pred-income">
                    <div class="pred-title">Classification</div>
                    <div class="pred-result val-positive">INCOME</div>
                    <div class="pred-conf val-positive">{conf_text}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pred-card pred-expense">
                    <div class="pred-title">Classification</div>
                    <div class="pred-result val-negative">EXPENSE</div>
                    <div class="pred-conf val-negative">{conf_text}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Enter the transaction details on the left and click the button to see the AI classification.")
            st.image("https://cdn-icons-png.flaticon.com/512/2015/2015041.png", width=150) # simple placeholder


# --- Page: Data Explorer ---
def render_data_explorer(df):
    st.title("🔍 Interactive Data Explorer")
    st.markdown("Deep dive into your raw transaction data. Filter, search, and export your records.")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return

    # Create filter controls
    with st.container():
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            type_filter = st.selectbox("Type", ["All"] + sorted(list(df['Type'].unique())))
        with f2:
            cat_filter = st.selectbox("Category", ["All"] + sorted(list(df['Category'].unique())))
        with f3:
            min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
            date_filter = st.date_input("Date Range", [min_date, max_date])
        with f4:
            search_query = st.text_input("Search Description", placeholder="e.g. 'grocery'...")

    # Apply filters
    filtered_df = df.copy()
    
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['Type'] == type_filter]
        
    if cat_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == cat_filter]
        
    if len(date_filter) == 2:
        start_date, end_date = date_filter
        filtered_df = filtered_df[(filtered_df['Date'].dt.date >= start_date) & (filtered_df['Date'].dt.date <= end_date)]
        
    if search_query:
        filtered_df = filtered_df[filtered_df['Transaction Description'].str.contains(search_query, case=False, na=False)]

    st.write("") # Spacing
    
    # Display info & download button
    col_info, col_btn = st.columns([4, 1])
    with col_info:
        st.markdown(f"**Showing {len(filtered_df):,} out of {len(df):,} transactions**")
    with col_btn:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="filtered_transactions.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Render interactive dataframe
    display_df = filtered_df[['Date', 'Transaction Description', 'Category', 'Amount', 'Type']].copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
        },
        height=600
    )

if __name__ == "__main__":
    main()
