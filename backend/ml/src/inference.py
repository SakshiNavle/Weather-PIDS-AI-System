from pathlib import Path
import joblib
import pandas as pd

# ==========================================================
# Load Model (only once)
# ==========================================================
# ==========================================================
# Load Model (only once)
# ==========================================================

MODEL_PATH = (
    Path(__file__).resolve()
    .parent.parent
    / "models"
    / "calibration_model.pkl"
)

model = joblib.load(MODEL_PATH)

# ==========================================================
# Feature Engineering
# ==========================================================

def create_features(
    temperature,
    humidity,
    wind_speed,
    rainfall
):
    """
    Create the same engineered features that were used
    during model training.
    """

    weather_severity_score = (
        0.10 * temperature +
        0.30 * humidity +
        0.20 * wind_speed +
        0.40 * rainfall
    )

    heavy_rain = 1 if rainfall >= 50 else 0

    high_humidity = 1 if humidity >= 80 else 0

    return pd.DataFrame([{
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rainfall": rainfall,
        "weather_severity_score": weather_severity_score,
        "heavy_rain": heavy_rain,
        "high_humidity": high_humidity
    }])


# ==========================================================
# Prediction Function
# ==========================================================

def predict(
    temperature,
    humidity,
    wind_speed,
    rainfall
):
    """
    Predict recommended sensor sensitivity.

    Returns:
        dict
    """

    features = create_features(
        temperature,
        humidity,
        wind_speed,
        rainfall
    )

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    confidence = float(round(max(probabilities), 4))

    label_map = {
        0: "HIGH",
        1: "LOW",
        2: "MEDIUM"
    }

    recommendation = label_map[int(prediction)]

    reason_map = {
        "HIGH":
            "Adverse weather conditions detected. Increase sensor sensitivity.",

        "MEDIUM":
            "Moderate weather conditions require balanced sensor sensitivity.",

        "LOW":
            "Stable weather conditions. Low sensor sensitivity is sufficient."
    }

    return {
        "recommended_sensitivity": recommendation,
        "confidence": confidence,
        "reason": reason_map[recommendation]
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    result = predict(
        temperature=32,
        humidity=85,
        wind_speed=20,
        rainfall=45
    )

    print("=" * 60)
    print("MODEL INFERENCE")
    print("=" * 60)
    print(result)