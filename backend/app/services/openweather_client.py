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

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY

        self.client = httpx.Client(
            timeout=10.0
        )

    def get_current_weather(
        self,
        city: str,
    ) -> dict[str, Any]:
        """
        Fetch current weather for a city.
        """

        response = self.client.get(
            self.BASE_URL,
            params={
                "q": city,
                "appid": self.api_key,
                "units": "metric",
            },
        )

        response.raise_for_status()

        return response.json()

    def close(self):
        """
        Close underlying HTTP client.
        """
        self.client.close()