from pathlib import Path
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================================
# Paths
# ==========================================================

project_root = Path(__file__).resolve().parent.parent

processed_path = project_root / "data" / "processed"
models_path = project_root / "models"

# ==========================================================
# Load Model
# ==========================================================

model = joblib.load(
    models_path / "calibration_model.pkl"
)

# ==========================================================
# Load Test Data
# ==========================================================

X_test = pd.read_csv(
    processed_path / "X_test.csv"
)

y_test = pd.read_csv(
    processed_path / "y_test.csv"
)["target"]

# ==========================================================
# Prediction
# ==========================================================

predictions = model.predict(X_test)

# ==========================================================
# Evaluation
# ==========================================================

accuracy = accuracy_score(
    y_test,
    predictions
)

print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(f"\nAccuracy : {accuracy:.4f}\n")

print("Classification Report")
print("-" * 60)

print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix")
print("-" * 60)

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print("\nEvaluation Completed Successfully.")