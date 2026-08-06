from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.models.alert import Alert

from app.services.weather_service import WeatherService
from app.services.recommendation_service import RecommendationService


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self):

        total_sensors = self.db.query(Sensor).count()

        active_sensors = (
            self.db.query(Sensor)
            .filter(Sensor.status == "ACTIVE")
            .count()
        )

        inactive_sensors = total_sensors - active_sensors

        total_alerts = self.db.query(Alert).count()

        active_alerts = (
            self.db.query(Alert)
            .filter(Alert.is_active == True)
            .count()
        )

        weather = WeatherService(self.db).get_latest_weather()

        recommendations = (
            RecommendationService(self.db)
            .get_all_recommendations()
        )

        recent_alerts = [
            alert
            for alert in (
                self.db.query(Alert)
                .order_by(Alert.created_at.desc())
                .limit(5)
                .all()
            )
        ]

        return {
            "total_sensors": total_sensors,
            "active_sensors": active_sensors,
            "inactive_sensors": inactive_sensors,
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "latest_weather": weather,
            "recommendations": recommendations,
            "recent_alerts": recent_alerts,
        }