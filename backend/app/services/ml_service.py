from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ============================================================
# MODEL PATHS
# ============================================================

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "models"
    / "calibration_model.pkl"
)

ENCODER_PATH = (
    BASE_DIR
    / "ml"
    / "models"
    / "label_encoder.pkl"
)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


# ============================================================
# VERIFY MODEL FEATURES
# ============================================================

EXPECTED_FEATURES = [
    "temperature",
    "humidity",
    "wind_speed",
    "rainfall",
    "weather_severity_score",
    "heavy_rain",
    "high_humidity",
]


if hasattr(model, "feature_names_in_"):

    actual_features = list(model.feature_names_in_)

    if actual_features != EXPECTED_FEATURES:
        raise RuntimeError(
            "ML model feature mismatch.\n"
            f"Expected: {EXPECTED_FEATURES}\n"
            f"Model has: {actual_features}"
        )


# ============================================================
# ML SERVICE
# ============================================================

class MLService:

    @staticmethod
    def predict(weather):
        """
        Run the trained calibration model.

        Supports:
            - SQLAlchemy WeatherData object
            - sensor reading dictionary

        Required raw inputs:
            temperature
            humidity
            wind_speed
            rainfall
        """

        # ====================================================
        # EXTRACT WEATHER VALUES
        # ====================================================

        if isinstance(weather, dict):

            temperature = float(
                weather["temperature"]
            )

            humidity = float(
                weather["humidity"]
            )

            wind_speed = float(
                weather["wind_speed"]
            )

            rainfall = float(
                weather["rainfall"]
            )

        else:

            temperature = float(
                weather.temperature
            )

            humidity = float(
                weather.humidity
            )

            wind_speed = float(
                weather.wind_speed
            )

            rainfall = float(
                weather.rainfall
            )


        # ====================================================
        # FEATURE ENGINEERING
        # ====================================================

        weather_severity_score = (
            rainfall * 2.0
            + wind_speed * 1.5
            + humidity * 0.5
        )

        heavy_rain = int(
            rainfall >= 5
        )

        high_humidity = int(
            humidity >= 90
        )


        # ====================================================
        # CREATE FEATURE DATAFRAME
        # ====================================================

        feature_data = {

            "temperature": temperature,

            "humidity": humidity,

            "wind_speed": wind_speed,

            "rainfall": rainfall,

            "weather_severity_score":
                weather_severity_score,

            "heavy_rain":
                heavy_rain,

            "high_humidity":
                high_humidity,
        }


        # Explicitly follow the trained model's
        # feature order.

        features = pd.DataFrame(
            [[
                feature_data[name]
                for name in EXPECTED_FEATURES
            ]],
            columns=EXPECTED_FEATURES
        )


        # ====================================================
        # MODEL PREDICTION
        # ====================================================

        prediction = model.predict(
            features
        )[0]


        # ====================================================
        # DECODE LABEL
        # ====================================================

        sensitivity = label_encoder.inverse_transform(
            [prediction]
        )[0]

        sensitivity = str(
            sensitivity
        )


        # ====================================================
        # CONFIDENCE
        # ====================================================

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                features
            )[0]

            confidence = float(
                np.max(probabilities)
            )

        else:

            confidence = 1.0


        # ====================================================
        # EXPLANATION
        # ====================================================

        reason = (
            f"ML model recommends "
            f"{sensitivity} sensitivity "
            f"based on "
            f"temperature={temperature:.2f}°C, "
            f"humidity={humidity:.0f}%, "
            f"wind speed={wind_speed:.2f} m/s, "
            f"rainfall={rainfall:.2f} mm."
        )


        # ====================================================
        # RETURN
        # ====================================================

        return {

            "recommended_sensitivity":
                sensitivity,

            "confidence":
                round(confidence, 4),

            "reason":
                reason,

            # Useful for debugging/dashboard
            "features":
                feature_data,
        }