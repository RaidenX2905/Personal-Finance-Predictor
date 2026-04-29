# 💸 Personal Finance Predictor

A sleek, intelligent web application built with **Streamlit** and **Machine Learning** to classify financial transactions. This project uses a **Random Forest Classifier** to predict whether a transaction is an **Income** or an **Expense** based on the amount and date.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

## ✨ Features

- **Intelligent Classification**: Leverages a Random Forest model to accurately predict transaction types.
- **Clean UI/UX**: A professional, light-themed interface designed for simplicity and clarity.
- **Interactive Dashboard**: Real-time data visualization of your financial history.
- **Instant Insights**: Side-by-side comparison of transaction amounts and categories.

**Live Link:** https://personal-finance-predictor-by-jsh.streamlit.app/

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RaidenX2905/Personal-Finance-Predictor.git
   cd Personal-Finance-Predictor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model (Optional if model.pkl exists):**
   ```bash
   python train_model.py
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📊 How it Works

The application processes raw transaction data through a pipeline that extracts temporal features (Month, Day) and applies logarithmic scaling to transaction amounts. The preprocessed data is then fed into a Random Forest ensemble model to determine the classification.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly Express
- **Data Handling**: Pandas & NumPy
- **Machine Learning**: Scikit-Learn

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ by [Raiden X](https://github.com/RaidenX2905)
