from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class WeatherData(Base):

    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True)

    temperature = Column(Float)

    humidity = Column(Float)

    wind_speed = Column(Float)

    rainfall = Column(Float)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())