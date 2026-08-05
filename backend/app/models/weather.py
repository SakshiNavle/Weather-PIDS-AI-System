from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)

    site_name = Column(String(100), nullable=False)
    # Example: North Plant

    temperature = Column(Float, nullable=False)

    humidity = Column(Float, nullable=False)

    wind_speed = Column(Float, nullable=False)

    rainfall = Column(Float, nullable=False)

    storm = Column(Boolean, default=False)

    weather_risk = Column(String(20), default="LOW")
    # LOW / MEDIUM / HIGH / SEVERE

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )