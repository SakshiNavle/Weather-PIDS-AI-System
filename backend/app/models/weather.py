from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from app.core.database import Base


class WeatherData(Base):

    __tablename__ = "weather_data"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    site_name = Column(
        String,
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=False
    )

    humidity = Column(
        Float,
        nullable=False
    )

    wind_speed = Column(
        Float,
        nullable=False
    )

    rainfall = Column(
        Float,
        nullable=False,
        default=0.0
    )

    weather_condition = Column(
        String,
        nullable=True
    )

    weather_description = Column(
        String,
        nullable=True
    )

    storm = Column(
        Boolean,
        default=False
    )

    weather_risk = Column(
        String,
        nullable=False
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )