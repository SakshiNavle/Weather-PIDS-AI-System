from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.models.weather import WeatherData
from app.repositories.weather_repository import WeatherRepository
from app.schemas.weather_schema import WeatherResponse
from app.services.openweather_client import OpenWeatherClient


logger = setup_logger(__name__)


class WeatherService:
    """
    Business logic for weather operations.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = WeatherRepository(db)
        self.client = OpenWeatherClient()

    def _extract_rainfall(self, weather: dict) -> float:
        rainfall = weather.get("rain") or {}
        return float(rainfall.get("1h", 0.0) or 0.0)

    def _is_stormy(self, weather: dict) -> bool:
        weather_conditions = weather.get("weather") or []
        if not weather_conditions:
            return False

        condition = (weather_conditions[0].get("main") or "").upper()
        return condition in {"THUNDERSTORM", "TORNADO", "HAIL", "RAIN"}

    def _get_weather_risk(self, weather: dict) -> str:
        if self._is_stormy(weather):
            return "HIGH"

        rainfall = self._extract_rainfall(weather)
        wind_speed = float((weather.get("wind") or {}).get("speed", 0.0) or 0.0)

        if rainfall >= 10.0 or wind_speed >= 20.0:
            return "MEDIUM"

        return "LOW"

    def _build_weather_data(self, city: str, weather: dict) -> WeatherData:
        rainfall = self._extract_rainfall(weather)
        storm = self._is_stormy(weather)
        risk_level = self._get_weather_risk(weather)

        return WeatherData(
            site_name=city,
            temperature=float(weather["main"]["temp"]),
            humidity=int(weather["main"]["humidity"]),
            wind_speed=float((weather.get("wind") or {}).get("speed", 0.0) or 0.0),
            rainfall=rainfall,
            storm=storm,
            weather_risk=risk_level,
        )

    def fetch_and_store_weather(
        self,
        city: str,
    ) -> WeatherResponse:
        """
        Fetch weather from OpenWeather,
        save it to the database,
        and return the saved record.
        """

        try:

            weather = self.client.get_current_weather(city)
            weather_data = self._build_weather_data(city, weather)

            self.repository.save(weather_data)

            self.db.commit()

            self.db.refresh(weather_data)

            logger.info(
                "Weather saved successfully for %s",
                city
            )

            return WeatherResponse.model_validate(weather_data)

        except Exception as ex:

            self.db.rollback()

            logger.exception(
                "Failed to fetch weather for %s",
                city
            )

            raise ex

        finally:
            self.client.close()

    def get_latest_weather(self):

        weather = self.repository.find_latest()

        if weather is None:
            return None

        return WeatherResponse.model_validate(weather)

    def get_weather_history(
        self,
        limit: int = 100,
    ):

        records = self.repository.find_history(limit)

        return [
            WeatherResponse.model_validate(record)
            for record in records
        ]