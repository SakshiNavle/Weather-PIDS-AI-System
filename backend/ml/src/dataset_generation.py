import random
from pathlib import Path

import pandas as pd

# ==========================================================
# Configuration
# ==========================================================
NUM_SAMPLES = 10000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

# ==========================================================
# Weather Scenarios
# ==========================================================

WEATHER_SCENARIOS = {
    "Sunny": {
        "temperature": (30, 45),
        "humidity": (20, 45),
        "wind_speed": (5, 18),
        "rainfall": (0, 5)
    },

    "Cloudy": {
        "temperature": (22, 32),
        "humidity": (45, 70),
        "wind_speed": (10, 25),
        "rainfall": (5, 20)
    },

    "Rainy": {
        "temperature": (18, 30),
        "humidity": (70, 95),
        "wind_speed": (15, 35),
        "rainfall": (20, 70)
    },

    "Storm": {
        "temperature": (15, 28),
        "humidity": (80, 100),
        "wind_speed": (30, 50),
        "rainfall": (60, 100)
    }
}

# Scenario probabilities (must total 1.0)
SCENARIO_WEIGHTS = [0.30, 0.25, 0.30, 0.15]

# ==========================================================
# Generate one weather sample
# ==========================================================

def generate_weather():

    scenario = random.choices(
        list(WEATHER_SCENARIOS.keys()),
        weights=SCENARIO_WEIGHTS,
        k=1
    )[0]

    ranges = WEATHER_SCENARIOS[scenario]

    temperature = round(
        random.uniform(*ranges["temperature"]),
        1
    )

    humidity = round(
        random.uniform(*ranges["humidity"]),
        1
    )

    wind_speed = round(
        random.uniform(*ranges["wind_speed"]),
        1
    )

    rainfall = round(
        random.uniform(*ranges["rainfall"]),
        1
    )

    return (
        temperature,
        humidity,
        wind_speed,
        rainfall,
        scenario
    )

# ==========================================================
# Recommendation Logic
# ==========================================================

# ==========================================================
# Recommendation Logic
# ==========================================================

def get_recommendation(
    temperature,
    humidity,
    wind_speed,
    rainfall
):
    """
    Generate sensor sensitivity recommendation based on
    weather severity with realistic uncertainty near
    decision boundaries.
    """

    # -----------------------------
    # Normalize Features (0 to 1)
    # -----------------------------
    temp_norm = (temperature - 15) / (45 - 15)
    humidity_norm = (humidity - 20) / (100 - 20)
    wind_norm = (wind_speed - 5) / (50 - 5)
    rain_norm = rainfall / 100

    # -----------------------------
    # Calculate Weather Severity
    # -----------------------------
    severity = (
        0.10 * temp_norm +
        0.30 * humidity_norm +
        0.20 * wind_norm +
        0.40 * rain_norm
    ) * 100

    # Simulate slight sensor/environment uncertainty
    severity += random.uniform(-5, 5)

    # -----------------------------
    # Recommendation Logic
    # -----------------------------

    # Very Safe Weather
    if severity < 25:
        recommendation = "LOW"

    # Boundary (LOW ↔ MEDIUM)
    elif severity < 40:
        if random.random() < 0.80:
            recommendation = "LOW"
        else:
            recommendation = "MEDIUM"

    # Clearly Moderate
    elif severity < 55:
        recommendation = "MEDIUM"

    # Boundary (MEDIUM ↔ HIGH)
    elif severity < 70:
        if random.random() < 0.80:
            recommendation = "HIGH"
        else:
            recommendation = "MEDIUM"

    # Severe Weather
    else:
        recommendation = "HIGH"

    # -----------------------------
    # Explanation
    # -----------------------------
    if recommendation == "LOW":
        explanation = (
            "Stable weather conditions. "
            "Low sensor sensitivity is sufficient."
        )

    elif recommendation == "MEDIUM":
        explanation = (
            "Moderate weather conditions require "
            "balanced sensor sensitivity."
        )

    else:
        explanation = (
            "Adverse weather conditions detected. "
            "Increase sensor sensitivity."
        )

    return recommendation, explanation
# ==========================================================
# Dataset Generation
# ==========================================================

records = []

for _ in range(NUM_SAMPLES):

    (
        temperature,
        humidity,
        wind_speed,
        rainfall,
        scenario
    ) = generate_weather()

    recommendation, explanation = get_recommendation(
        temperature,
        humidity,
        wind_speed,
        rainfall
    )

    records.append({

        "temperature": temperature,

        "humidity": humidity,

        "wind_speed": wind_speed,

        "rainfall": rainfall,

        "recommended_sensitivity": recommendation,

        "explanation": explanation

    })

# ==========================================================
# Save Dataset
# ==========================================================

df = pd.DataFrame(records)

project_root = Path(__file__).resolve().parent.parent

output_path = project_root / "data" / "synthetic_weather.csv"

df.to_csv(output_path, index=False)

# ==========================================================
# Summary
# ==========================================================

print("=" * 60)
print("Synthetic Dataset Generated Successfully")
print("=" * 60)

print(f"Location : {output_path}")
print(f"Samples  : {len(df)}")

print("\nClass Distribution:")

print(df["recommended_sensitivity"].value_counts())

print("=" * 60)