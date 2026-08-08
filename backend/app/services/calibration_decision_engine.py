from typing import Any


class CalibrationDecisionEngine:

    @staticmethod
    def generate_recommendation(
        weather: dict[str, Any],
        risk: dict[str, Any],
    ) -> dict[str, Any]:

        risk_level = risk["risk"]
        score = risk["score"]
        reasons = risk["reasons"]

        if risk_level == "HIGH":
            action = "CALIBRATE"
            priority = "HIGH"
            frequency = "INCREASED"
            message = (
                "High weather risk detected. "
                "Sensor calibration is recommended."
            )

        elif risk_level == "MEDIUM":
            action = "MONITOR"
            priority = "MEDIUM"
            frequency = "NORMAL"
            message = (
                "Moderate weather risk detected. "
                "Monitor sensor conditions and prepare for calibration."
            )

        else:
            action = "NORMAL_OPERATION"
            priority = "LOW"
            frequency = "NORMAL"
            message = (
                "Weather conditions are stable. "
                "Continue normal sensor operation."
            )

        return {
            "action": action,
            "priority": priority,
            "calibration_frequency": frequency,
            "weather_risk": risk_level,
            "risk_score": score,
            "message": message,
            "reasons": reasons,
        }