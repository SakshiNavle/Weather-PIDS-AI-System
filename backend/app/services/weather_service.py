from sqlalchemy.orm import Session

from app.core.logger import setup_logger

from app.models.weather import WeatherData
from app.models.alert import Alert

from app.repositories.weather_repository import WeatherRepository

from app.schemas.weather_schema import WeatherResponse

from app.services.openweather_client import OpenWeatherClient


logger = setup_logger(__name__)


class WeatherService:
    """
    Business logic for live weather operations.
    """

    def __init__(self, db: Session):

        self.db = db

        self.repository = WeatherRepository(db)

        self.client = OpenWeatherClient()

    # =========================================================
    # RAINFALL
    # =========================================================

    def _extract_rainfall(
        self,
        weather: dict
    ) -> float:
        """
        Extract rainfall from OpenWeather response.

        OpenWeather normally provides:

            rain -> 1h

        However, the rain object may be absent.
        Therefore we safely handle all cases.
        """

        rain_data = weather.get("rain") or {}

        rainfall_1h = rain_data.get("1h")

        if rainfall_1h is not None:

            try:
                return max(
                    0.0,
                    float(rainfall_1h)
                )

            except (TypeError, ValueError):

                return 0.0

        return 0.0

    # =========================================================
    # WEATHER CONDITION
    # =========================================================

    def _extract_weather_condition(
        self,
        weather: dict
    ) -> tuple[str, str]:
        """
        Extract weather condition and description.

        Example:

        main        = Rain
        description = light rain
        """

        weather_list = weather.get("weather") or []

        if not weather_list:

            return "Clear", ""

        current_condition = weather_list[0]

        condition = (
            current_condition.get(
                "main",
                "Clear"
            )
            or "Clear"
        )

        description = (
            current_condition.get(
                "description",
                ""
            )
            or ""
        )

        return (
            condition,
            description
        )

    # =========================================================
    # STORM DETECTION
    # =========================================================

    def _is_storm(
        self,
        weather: dict
    ) -> bool:

        condition, _ = (
            self._extract_weather_condition(
                weather
            )
        )

        return condition.upper() in {
            "THUNDERSTORM",
            "TORNADO"
        }

    # =========================================================
    # WEATHER RISK
    # =========================================================

    def _get_weather_risk(
        self,
        weather: dict
    ) -> str:

        rainfall = self._extract_rainfall(
            weather
        )

        wind_speed = float(
            (
                weather.get("wind") or {}
            ).get(
                "speed",
                0
            )
        )

        humidity = float(
            (
                weather.get("main") or {}
            ).get(
                "humidity",
                0
            )
        )

        condition, description = (
            self._extract_weather_condition(
                weather
            )
        )

        condition = condition.upper()

        description = description.lower()

        # =====================================================
        # SEVERE
        # =====================================================

        if condition in {
            "THUNDERSTORM",
            "TORNADO"
        }:

            return "SEVERE"

        # =====================================================
        # HIGH
        # =====================================================

        if rainfall >= 20:

            return "HIGH"

        if wind_speed >= 15:

            return "HIGH"

        # Heavy rain indicated by weather description
        if (
            "heavy rain" in description
            or "heavy intensity rain" in description
        ):

            return "HIGH"

        # =====================================================
        # MEDIUM
        # =====================================================

        if rainfall >= 5:

            return "MEDIUM"

        if wind_speed >= 10:

            return "MEDIUM"

        if humidity >= 90:

            return "MEDIUM"

        # Rain/drizzle should not automatically
        # become LOW simply because rainfall amount
        # is unavailable.

        if condition in {
            "RAIN",
            "DRIZZLE"
        }:

            return "MEDIUM"

        # =====================================================
        # LOW
        # =====================================================

        return "LOW"

    # =========================================================
    # BUILD WEATHER OBJECT
    # =========================================================

    def _build_weather_data(
        self,
        city: str,
        weather: dict
    ) -> WeatherData:

        main_data = (
            weather.get("main") or {}
        )

        wind_data = (
            weather.get("wind") or {}
        )

        rainfall = self._extract_rainfall(
            weather
        )

        condition, description = (
            self._extract_weather_condition(
                weather
            )
        )

        risk_level = self._get_weather_risk(
            weather
        )

        storm = self._is_storm(
            weather
        )

        return WeatherData(

            site_name=city,

            temperature=float(
                main_data.get(
                    "temp",
                    0
                )
            ),

            humidity=float(
                main_data.get(
                    "humidity",
                    0
                )
            ),

            wind_speed=float(
                wind_data.get(
                    "speed",
                    0
                )
            ),

            rainfall=rainfall,

            weather_condition=condition,

            weather_description=description,

            storm=storm,

            weather_risk=risk_level
        )

    # =========================================================
    # WEATHER ALERT
    # =========================================================

    def _create_weather_alert(
        self,
        weather_data: WeatherData
    ):

        if weather_data.weather_risk not in {
            "HIGH",
            "SEVERE"
        }:

            return

        alert = Alert(

            site_name=weather_data.site_name,

            risk_level=weather_data.weather_risk,

            message=(
                f"{weather_data.weather_risk} weather "
                f"detected at "
                f"{weather_data.site_name}. "
                f"Sensor calibration recommended."
            ),

            is_active=True
        )

        self.db.add(alert)

    # =========================================================
    # FETCH + STORE
    # =========================================================

    def fetch_and_store_weather(
        self,
        city: str
    ) -> WeatherResponse:

        try:

            # -------------------------------------------------
            # Fetch live weather
            # -------------------------------------------------

            weather = (
                self.client.get_current_weather(
                    city
                )
            )

            # -------------------------------------------------
            # Build database object
            # -------------------------------------------------

            weather_data = (
                self._build_weather_data(
                    city,
                    weather
                )
            )

            # =================================================
            # DEBUG
            # =================================================

            print("\n")
            print("=" * 70)

            print("LIVE OPENWEATHER DATA")

            print("=" * 70)

            print(
                f"City             : {city}"
            )

            print(
                f"Temperature      : "
                f"{weather_data.temperature} °C"
            )

            print(
                f"Humidity         : "
                f"{weather_data.humidity} %"
            )

            print(
                f"Wind Speed       : "
                f"{weather_data.wind_speed} m/s"
            )

            print(
                f"Rainfall (1h)    : "
                f"{weather_data.rainfall} mm"
            )

            print(
                f"Condition        : "
                f"{weather_data.weather_condition}"
            )

            print(
                f"Description      : "
                f"{weather_data.weather_description}"
            )

            print(
                f"Storm            : "
                f"{weather_data.storm}"
            )

            print(
                f"Risk             : "
                f"{weather_data.weather_risk}"
            )

            print("=" * 70)

            # =================================================
            # SAVE
            # =================================================

            self.repository.save(
                weather_data
            )

            # =================================================
            # ALERT
            # =================================================

            self._create_weather_alert(
                weather_data
            )

            # =================================================
            # COMMIT
            # =================================================

            self.db.commit()

            self.db.refresh(
                weather_data
            )

            logger.info(
                "Weather saved successfully for %s",
                city
            )

            return WeatherResponse.model_validate(
                weather_data
            )

        except Exception as ex:

            self.db.rollback()

            logger.exception(
                "Failed to fetch weather for %s",
                city
            )

            raise ex

        finally:

            self.client.close()

    # =========================================================
    # LATEST WEATHER
    # =========================================================

    def get_latest_weather(self):

        weather = (
            self.repository.find_latest()
        )

        if weather is None:

            return None

        return WeatherResponse.model_validate(
            weather
        )

    # =========================================================
    # HISTORY
    # =========================================================

    def get_weather_history(
        self,
        limit: int = 100
    ):

        records = (
            self.repository.find_history(
                limit
            )
        )

        return [
            WeatherResponse.model_validate(
                record
            )
            for record in records
        ]