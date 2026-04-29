import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def main():
    print("Loading dataset...")
    # Assuming dataset is in the same directory
    csv_path = "Personal_Finance_Dataset.csv"
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # Strip column names just in case
    df.columns = df.columns.str.strip()

    print("Preprocessing data...")
    # Convert to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Extract Month and Day
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    
    # Convert Amount to numeric and apply log1p
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Amount'] = np.log1p(df['Amount'])
    
    # Map Type (Income vs Expense)
    df['Type'] = df['Type'].map({'Income': 1, 'Expense': 0})
    
    # Drop rows with NaN values
    df = df.dropna()
    
    # Features and Target
    X = df[['Amount', 'Month', 'Day']]
    y = df['Type'].astype(int)
    
    print(f"Training RandomForestClassifier on {len(X)} samples...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    print("Saving model to model.pkl...")
    with open("model.pkl", "wb") as f:
        pickle.dump(rf, f)
        
    print("Model training and saving completed successfully!")

if __name__ == "__main__":
    main()
