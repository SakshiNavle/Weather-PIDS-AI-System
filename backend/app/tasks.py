import logging

from app.core.database import SessionLocal
from app.models.sensor import Sensor
from app.services.weather_service import WeatherService


logger = logging.getLogger(__name__)


# ============================================================
# UPDATE WEATHER FOR ALL SENSOR LOCATIONS
# ============================================================

def update_weather():
    """
    Fetch and store weather for every unique sensor location.

    Locations are discovered dynamically from the Sensor table.

    Example:

        Sensor 1 -> Mumbai
        Sensor 2 -> Mumbai
        Sensor 3 -> Pune

    Weather API calls:

        Mumbai -> once
        Pune   -> once

    Duplicate locations are automatically removed.
    """

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Get unique sensor locations
        # ----------------------------------------------------

        locations = (
            db.query(Sensor.location)
            .filter(
                Sensor.location.isnot(None)
            )
            .distinct()
            .all()
        )

        if not locations:

            logger.warning(
                "No sensor locations found. "
                "Skipping weather update."
            )

            return

        weather_service = WeatherService(db)

        # ----------------------------------------------------
        # Fetch weather for every location
        # ----------------------------------------------------

        for (location,) in locations:

            location = location.strip()

            if not location:
                continue

            try:

                logger.info(
                    f"Fetching weather for {location}"
                )

                weather_service.fetch_and_store_weather(
                    location
                )

                logger.info(
                    f"Weather updated successfully "
                    f"for {location}"
                )

            except Exception as ex:

                logger.error(
                    f"Failed to update weather "
                    f"for {location}: {ex}",
                    exc_info=True,
                )

    except Exception as ex:

        logger.error(
            f"Weather scheduler failed: {ex}",
            exc_info=True,
        )

    finally:

        db.close()