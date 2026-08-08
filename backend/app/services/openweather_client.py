from typing import Any

import httpx

from app.core.config import settings


class OpenWeatherClient:
    """
    Client responsible for communicating with the
    OpenWeather API.

    Responsibilities:
    - Build API requests
    - Handle timeouts
    - Parse responses
    - Raise errors

    Does NOT:
    - Save data
    - Perform business logic
    - Access the database
    """

    CURRENT_WEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    FORECAST_URL = (
        "https://api.openweathermap.org/data/2.5/forecast"
    )

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY

        self.client = httpx.Client(
            timeout=10.0
        )

    # ============================================================
    # CURRENT WEATHER
    # ============================================================

    def get_current_weather(
        self,
        city: str,
    ) -> dict[str, Any]:
        """
        Fetch current weather for a city.
        """

        response = self.client.get(
            self.CURRENT_WEATHER_URL,
            params={
                "q": city,
                "appid": self.api_key,
                "units": "metric",
            },
        )

        response.raise_for_status()

        return response.json()

    # ============================================================
    # WEATHER FORECAST
    # ============================================================

    def get_weather_forecast(
        self,
        city: str,
    ) -> dict[str, Any]:
        """
        Fetch short-term weather forecast for a city.

        OpenWeather provides forecast data at approximately
        3-hour intervals.
        """

        response = self.client.get(
            self.FORECAST_URL,
            params={
                "q": city,
                "appid": self.api_key,
                "units": "metric",
            },
        )

        response.raise_for_status()

        return response.json()

    # ============================================================
    # CLOSE CLIENT
    # ============================================================

    def close(self):
        """
        Close underlying HTTP client.
        """

        self.client.close()