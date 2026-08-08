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
        String(100),
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
        default=0.0,
        nullable=False
    )

    weather_condition = Column(
        String(50),
        default="Clear",
        nullable=False
    )

    weather_description = Column(
        String(150),
        default="",
        nullable=False
    )

    storm = Column(
        Boolean,
        default=False,
        nullable=False
    )

    weather_risk = Column(
        String(20),
        default="LOW",
        nullable=False
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )