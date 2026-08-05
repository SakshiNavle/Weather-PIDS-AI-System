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

            rainfall = 0.0

            if "rain" in weather:
                rainfall = weather["rain"].get("1h", 0.0)

            weather_data = WeatherData(
                temperature=weather["main"]["temp"],
                humidity=weather["main"]["humidity"],
                wind_speed=weather["wind"]["speed"],
                rainfall=rainfall,
            )

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