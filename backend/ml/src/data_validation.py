from pathlib import Path

import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
project_root = Path(__file__).resolve().parent.parent
dataset_path = project_root / "data" / "synthetic_weather.csv"

df = pd.read_csv(dataset_path)

print("=" * 60)
print("DATASET VALIDATION REPORT")
print("=" * 60)

# Shape
print(f"\nDataset Shape: {df.shape}")

# Data Types
print("\nData Types:")
print(df.dtypes)

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicate Rows
print("\nDuplicate Rows:", df.duplicated().sum())

# Class Distribution
print("\nClass Distribution:")
print(df["recommended_sensitivity"].value_counts())

# Statistical Summary
print("\nStatistical Summary:")
print(df.describe())

print("\nFirst Five Rows:")
print(df.head())

print("\nValidation Completed Successfully!")