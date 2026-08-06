# Weather-Based Sensor Calibration ML Module

## Objective

Predict the recommended sensor sensitivity based on weather conditions.

## Input Features

| Feature | Type | Unit | Range |
|---------|------|------|-------|
| temperature | float | °C | 10 - 45 |
| humidity | float | % | 20 - 100 |
| wind_speed | float | km/h | 0 - 50 |
| rainfall | float | mm | 0 - 100 |

## Target

recommended_sensitivity

Classes:

- LOW
- MEDIUM
- HIGH

## Output

The trained model returns:

- recommended_sensitivity
- confidence
- explanation
