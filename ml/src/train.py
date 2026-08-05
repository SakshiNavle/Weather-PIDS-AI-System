from pathlib import Path
import joblib
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Paths
# -----------------------------
project_root = Path(__file__).resolve().parent.parent

processed_path = project_root / "data" / "processed"
models_path = project_root / "models"
models_path.mkdir(exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------
X_train = pd.read_csv(processed_path / "X_train.csv")
X_test = pd.read_csv(processed_path / "X_test.csv")

y_train = pd.read_csv(processed_path / "y_train.csv")["target"]
y_test = pd.read_csv(processed_path / "y_test.csv")["target"]

# -----------------------------
# Models
# -----------------------------
models = {
    "Decision Tree": DecisionTreeClassifier(
        random_state=42,
        class_weight="balanced"
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
}

best_model = None
best_accuracy = 0
best_name = ""

print("=" * 60)
print("MODEL TRAINING")
print("=" * 60)

# -----------------------------
# Train Models
# -----------------------------
for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"\n{name}")
    print("-" * 40)
    print(f"Accuracy : {accuracy:.4f}")

    print(classification_report(y_test, predictions))

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_name = name

# -----------------------------
# Save Best Model
# -----------------------------
joblib.dump(
    best_model,
    models_path / "calibration_model.pkl"
)

print("\n" + "=" * 60)
print(f"Best Model : {best_name}")
print(f"Accuracy   : {best_accuracy:.4f}")
print("Model saved successfully!")
print("=" * 60)

print("\nBest Model Parameters:")
print(best_model.get_params())