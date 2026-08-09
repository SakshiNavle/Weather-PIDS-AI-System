from sqlalchemy.orm import Session

from app.core.logger import setup_logger

from app.models.weather import WeatherData
from app.models.alert import Alert
from app.models.recommendation import Recommendation

from app.repositories.weather_repository import WeatherRepository

from app.schemas.weather_schema import WeatherResponse

from app.services.openweather_client import OpenWeatherClient


logger = setup_logger(__name__)


class WeatherService:
    """
    Business logic for live weather operations.

    Flow:
        OpenWeather
             ↓
        WeatherData
             ↓
        Risk calculation
             ↓
        HIGH/SEVERE → Alert
             ↓
        HIGH/SEVERE → Recommendation
    """

    def __init__(self, db: Session):

        self.db = db
        self.repository = WeatherRepository(db)
        self.client = OpenWeatherClient()

    # =========================================================
    # RAINFALL
    # =========================================================

    def _extract_rainfall(self, weather: dict) -> float:

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

        return condition, description

    # =========================================================
    # STORM
    # =========================================================

    def _is_storm(self, weather: dict) -> bool:

        condition, _ = (
            self._extract_weather_condition(weather)
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

        rainfall = self._extract_rainfall(weather)

        wind_speed = float(
            (weather.get("wind") or {}).get(
                "speed",
                0
            )
        )

        humidity = float(
            (weather.get("main") or {}).get(
                "humidity",
                0
            )
        )

        condition, description = (
            self._extract_weather_condition(weather)
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

        main_data = weather.get("main") or {}
        wind_data = weather.get("wind") or {}

        rainfall = self._extract_rainfall(weather)

        condition, description = (
            self._extract_weather_condition(weather)
        )

        risk_level = self._get_weather_risk(weather)

        storm = self._is_storm(weather)

        return WeatherData(

            site_name=city,

            temperature=float(
                main_data.get("temp", 0)
            ),

            humidity=float(
                main_data.get("humidity", 0)
            ),

            wind_speed=float(
                wind_data.get("speed", 0)
            ),

            rainfall=rainfall,

            weather_condition=condition,

            weather_description=description,

            storm=storm,

            weather_risk=risk_level
        )

    # =========================================================
    # CREATE ALERT
    # =========================================================

    def _create_weather_alert(
        self,
        weather_data: WeatherData
    ):

        risk = weather_data.weather_risk

        if risk not in {
            "HIGH",
            "SEVERE"
        }:
            return

        # Prevent duplicate active alerts for same
        # site and risk level.

        existing = (
            self.db.query(Alert)
            .filter(
                Alert.site_name
                == weather_data.site_name,

                Alert.risk_level
                == risk,

                Alert.is_active
                == True
            )
            .first()
        )

        if existing:
            return

        message = (
            f"{risk} weather detected at "
            f"{weather_data.site_name}. "
            f"Sensor calibration recommended. "
            f"Condition: "
            f"{weather_data.weather_condition}, "
            f"temperature: "
            f"{weather_data.temperature:.1f}°C, "
            f"humidity: "
            f"{weather_data.humidity:.0f}%, "
            f"wind: "
            f"{weather_data.wind_speed:.1f} m/s, "
            f"rainfall: "
            f"{weather_data.rainfall:.2f} mm."
        )

        alert = Alert(

            site_name=weather_data.site_name,

            risk_level=risk,

            message=message,

            is_active=True
        )

        self.db.add(alert)

    # =========================================================
    # CREATE RECOMMENDATION
    # =========================================================

    def _create_weather_recommendation(
        self,
        weather_data: WeatherData
    ):

        risk = weather_data.weather_risk

        # Recommendations are meaningful for
        # MEDIUM, HIGH and SEVERE conditions.

        if risk not in {
            "MEDIUM",
            "HIGH",
            "SEVERE"
        }:
            return

        # -----------------------------------------------------
        # Find an available sensor.
        # -----------------------------------------------------

        try:

            from app.models.sensor import Sensor

            sensor = (
                self.db.query(Sensor)
                .filter(
                    Sensor.location
                    == weather_data.site_name
                )
                .first()
            )

            # If no sensor exists for the city,
            # we cannot create a sensor-specific recommendation.

            if sensor is None:
                logger.warning(
                    "No sensor found for location %s",
                    weather_data.site_name
                )
                return

            # -------------------------------------------------
            # Decide recommended sensitivity.
            # -------------------------------------------------

            if risk == "SEVERE":

                recommended_sensitivity = "HIGH"

                action = (
                    "Increase sensor sensitivity to HIGH "
                    "and monitor environmental conditions "
                    "continuously."
                )

            elif risk == "HIGH":

                recommended_sensitivity = "HIGH"

                action = (
                    "Increase sensor sensitivity to HIGH "
                    "to improve detection during elevated "
                    "weather risk."
                )

            else:

                recommended_sensitivity = "MEDIUM"

                action = (
                    "Set sensor sensitivity to MEDIUM "
                    "and continue monitoring weather conditions."
                )

            # -------------------------------------------------
            # Prevent excessive duplicate recommendations.
            # -------------------------------------------------

            existing = (
                self.db.query(Recommendation)
                .filter(
                    Recommendation.sensor_id
                    == sensor.id,

                    Recommendation.risk_level
                    == risk
                )
                .first()
            )

            if existing:
                return

            description = (
                f"Weather conditions at "
                f"{weather_data.site_name} indicate "
                f"{risk} environmental risk. "
                f"Temperature="
                f"{weather_data.temperature:.2f}°C, "
                f"humidity="
                f"{weather_data.humidity:.0f}%, "
                f"wind speed="
                f"{weather_data.wind_speed:.2f} m/s, "
                f"rainfall="
                f"{weather_data.rainfall:.2f} mm."
            )

            recommendation = Recommendation(

                sensor_id=sensor.id,

                risk_level=risk,

                title=(
                    f"{risk} Weather Calibration Recommendation"
                ),

                description=description,

                action=action
            )

            self.db.add(recommendation)

            logger.info(
                "Recommendation created for sensor %s",
                sensor.id
            )

        except Exception:

            logger.exception(
                "Failed to create weather recommendation"
            )

            # Do not destroy the weather transaction
            # if recommendation generation fails.

    # =========================================================
    # FETCH + STORE WEATHER
    # =========================================================

    def fetch_and_store_weather(
        self,
        city: str
    ) -> WeatherResponse:

        try:

            # -------------------------------------------------
            # Fetch live OpenWeather data
            # -------------------------------------------------

            weather = (
                self.client.get_current_weather(city)
            )

            # -------------------------------------------------
            # Build WeatherData
            # -------------------------------------------------

            weather_data = (
                self._build_weather_data(
                    city,
                    weather
                )
            )

            logger.info(
                "Weather fetched: city=%s risk=%s",
                city,
                weather_data.weather_risk
            )

            # -------------------------------------------------
            # Save weather
            # -------------------------------------------------

            self.repository.save(
                weather_data
            )

            # -------------------------------------------------
            # Alert
            # -------------------------------------------------

            self._create_weather_alert(
                weather_data
            )

            # -------------------------------------------------
            # Recommendation
            # -------------------------------------------------

            self._create_weather_recommendation(
                weather_data
            )

            # -------------------------------------------------
            # Commit everything
            # -------------------------------------------------

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
            WeatherResponse.model_validate(record)
            for record in records
        ]