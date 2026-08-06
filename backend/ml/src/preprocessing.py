from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# Paths
# -----------------------------
project_root = Path(__file__).resolve().parent.parent

data_path = project_root / "data" / "synthetic_weather.csv"

processed_path = project_root / "data" / "processed"
processed_path.mkdir(exist_ok=True)

models_path = project_root / "models"
models_path.mkdir(exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(data_path)

# -----------------------------
# Features & Target
# -----------------------------
X = df[[
    "temperature",
    "humidity",
    "wind_speed",
    "rainfall"
]]

y = df["recommended_sensitivity"]

# -----------------------------
# Encode Labels
# -----------------------------
label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

joblib.dump(
    label_encoder,
    models_path / "label_encoder.pkl"
)

# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

# -----------------------------
# Save Processed Files
# -----------------------------
X_train.to_csv(processed_path / "X_train.csv", index=False)
X_test.to_csv(processed_path / "X_test.csv", index=False)

pd.DataFrame({"target": y_train}).to_csv(
    processed_path / "y_train.csv",
    index=False
)

pd.DataFrame({"target": y_test}).to_csv(
    processed_path / "y_test.csv",
    index=False
)

print("=" * 60)
print("PREPROCESSING COMPLETED")
print("=" * 60)

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

print("\nClasses:")

for i, label in enumerate(label_encoder.classes_):
    print(f"{i} -> {label}")

print("\nProcessed files saved successfully.")