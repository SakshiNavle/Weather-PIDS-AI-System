from pathlib import Path

import pandas as pd

# -----------------------------
# Paths
# -----------------------------
project_root = Path(__file__).resolve().parent.parent

processed_path = project_root / "data" / "processed"

# -----------------------------
# Load Processed Data
# -----------------------------
X_train = pd.read_csv(processed_path / "X_train.csv")
X_test = pd.read_csv(processed_path / "X_test.csv")

# -----------------------------
# Feature Engineering Function
# -----------------------------
def add_engineered_features(df):
    df = df.copy()

    # Weather Severity Score (0–100+)
    df["weather_severity_score"] = (
        0.4 * df["rainfall"] +
        0.3 * df["humidity"] +
        0.2 * df["wind_speed"] +
        0.1 * df["temperature"]
    )

    # Heavy Rain Indicator
    df["heavy_rain"] = (df["rainfall"] >= 50).astype(int)

    # High Humidity Indicator
    df["high_humidity"] = (df["humidity"] >= 85).astype(int)

    return df

# -----------------------------
# Apply Feature Engineering
# -----------------------------
X_train = add_engineered_features(X_train)
X_test = add_engineered_features(X_test)

# -----------------------------
# Save Updated Data
# -----------------------------
X_train.to_csv(processed_path / "X_train.csv", index=False)
X_test.to_csv(processed_path / "X_test.csv", index=False)

print("=" * 60)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 60)

print("\nNew Features Added:")
print("- weather_severity_score")
print("- heavy_rain")
print("- high_humidity")

print("\nTraining Columns:")
print(list(X_train.columns))