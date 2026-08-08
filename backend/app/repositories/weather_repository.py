from typing import Optional

from sqlalchemy.orm import Session

from app.models.weather import WeatherData


class WeatherRepository:
    """
    Repository layer for WeatherData database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        weather: WeatherData,
    ) -> WeatherData:
        self.db.add(weather)
        return weather

    def find_latest(
        self,
    ) -> Optional[WeatherData]:
        return (
            self.db.query(WeatherData)
            .order_by(
                WeatherData.timestamp.desc()
            )
            .first()
        )

    def find_history(self, limit: int = 100):
        return (
            self.db.query(WeatherData)
            .order_by(
                WeatherData.recorded_at.desc()
            )
            .limit(limit)
            .all()
        )

    def find_between_dates(
        self,
        start_date,
        end_date,
    ) -> list[WeatherData]:
        return (
            self.db.query(WeatherData)
            .filter(
                WeatherData.timestamp >= start_date,
                WeatherData.timestamp <= end_date,
            )
            .order_by(
                WeatherData.timestamp.asc()
            )
            .all()
        )