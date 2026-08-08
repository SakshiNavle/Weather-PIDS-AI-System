from typing import Any


class WeatherRiskEngine:

    @staticmethod
    def calculate_risk(
        weather: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Calculate weather risk for the next 24 hours.

        Risk is based on:
        - Rain probability
        - Rainfall
        - Wind speed
        - Humidity
        - Weather condition
        """

        rain_probability = weather.get("max_rain_probability", 0)
        rainfall = weather.get("max_rainfall", 0)
        wind_speed = weather.get("max_wind_speed", 0)
        humidity = weather.get("humidity", 0)
        condition = weather.get("weather_condition", "")

        score = 0
        reasons = []

        # --------------------------------------------------
        # RAIN PROBABILITY
        # --------------------------------------------------

        if rain_probability >= 80:
            score += 3
            reasons.append(
                "Very high probability of precipitation"
            )

        elif rain_probability >= 50:
            score += 2
            reasons.append(
                "Moderate probability of precipitation"
            )

        elif rain_probability >= 30:
            score += 1

        # --------------------------------------------------
        # RAINFALL
        # --------------------------------------------------

        if rainfall >= 4:
            score += 3
            reasons.append(
                "Heavy rainfall expected"
            )

        elif rainfall >= 2:
            score += 2
            reasons.append(
                "Moderate rainfall expected"
            )

        elif rainfall >= 0.5:
            score += 1
            reasons.append(
                "Rainfall expected"
            )

        # --------------------------------------------------
        # WIND
        # --------------------------------------------------

        if wind_speed >= 12:
            score += 3
            reasons.append(
                "High wind speed expected"
            )

        elif wind_speed >= 8:
            score += 2
            reasons.append(
                "Elevated wind speed expected"
            )

        elif wind_speed >= 5:
            score += 1

        # --------------------------------------------------
        # HUMIDITY
        # --------------------------------------------------

        if humidity >= 85:
            score += 2
            reasons.append(
                "Very high humidity"
            )

        elif humidity >= 75:
            score += 1
            reasons.append(
                "High humidity"
            )

        # --------------------------------------------------
        # WEATHER CONDITION
        # --------------------------------------------------

        if condition == "Thunderstorm":
            score += 3
            reasons.append(
                "Thunderstorm conditions expected"
            )

        elif condition == "Rain":
            score += 1

        elif condition == "Drizzle":
            score += 1

        # --------------------------------------------------
        # FINAL RISK
        # --------------------------------------------------

        if score >= 7:
            risk = "HIGH"

        elif score >= 4:
            risk = "MEDIUM"

        else:
            risk = "LOW"

        return {
            "risk": risk,
            "score": score,
            "reasons": reasons,
        }