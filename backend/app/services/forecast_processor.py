from typing import Any


class ForecastProcessor:

    @staticmethod
    def process_forecast(data: dict[str, Any]) -> dict[str, Any]:
        """
        Convert OpenWeather 3-hour forecast data
        into PIDS-friendly weather metrics.
        """

        forecast_list = data.get("list", [])

        if not forecast_list:
            raise ValueError("No forecast data available")

        # OpenWeather provides forecast every 3 hours.
        # First 8 records = approximately next 24 hours.
        next_24_hours = forecast_list[:8]

        temperatures = []
        humidities = []
        wind_speeds = []
        rainfall = []
        rain_probability = []
        conditions = []

        for item in next_24_hours:

            main = item.get("main", {})
            wind = item.get("wind", {})
            weather = item.get("weather", [{}])[0]

            temperatures.append(main.get("temp", 0))
            humidities.append(main.get("humidity", 0))
            wind_speeds.append(wind.get("speed", 0))

            # Rainfall for this 3-hour period
            rain_data = item.get("rain", {})
            rainfall.append(rain_data.get("3h", 0))

            # Probability of precipitation
            rain_probability.append(item.get("pop", 0))

            conditions.append(weather.get("main", "Unknown"))

        max_rainfall = max(rainfall)
        max_rain_probability = max(rain_probability)
        max_wind_speed = max(wind_speeds)

        # Determine dominant weather condition
        if "Thunderstorm" in conditions:
            weather_condition = "Thunderstorm"
        elif "Rain" in conditions:
            weather_condition = "Rain"
        elif "Drizzle" in conditions:
            weather_condition = "Drizzle"
        elif "Snow" in conditions:
            weather_condition = "Snow"
        elif "Clouds" in conditions:
            weather_condition = "Clouds"
        else:
            weather_condition = conditions[0]

        return {
            "location": data["city"]["name"],
            "next_24_hours": {
                "temperature": round(sum(temperatures) / len(temperatures), 2),
                "max_temperature": round(max(temperatures), 2),
                "min_temperature": round(min(temperatures), 2),

                "humidity": round(
                    sum(humidities) / len(humidities), 2
                ),

                "max_wind_speed": round(max_wind_speed, 2),

                "max_rainfall": round(max_rainfall, 2),

                "max_rain_probability": round(
                    max_rain_probability * 100, 2
                ),

                "weather_condition": weather_condition,
            }
        }