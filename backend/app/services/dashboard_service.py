from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.models.weather import WeatherData
from app.models.alert import Alert
from app.models.recommendation import Recommendation

from app.schemas.dashboard_schema import DashboardSummary
from app.schemas.weather_schema import WeatherResponse
from app.schemas.alert_schema import AlertResponse
from app.schemas.recommendation_schema import RecommendationResponse


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # GET DASHBOARD
    # ============================================================

    def get_dashboard(self):

        # ========================================================
        # SENSORS
        # ========================================================

        sensors = (
            self.db.query(Sensor)
            .all()
        )

        total_sensors = len(sensors)

        active_sensors = sum(
            1
            for sensor in sensors
            if sensor.status == "ACTIVE"
        )

        inactive_sensors = (
            total_sensors - active_sensors
        )

        # ========================================================
        # ALERTS
        # ========================================================

        alerts = (
            self.db.query(Alert)
            .all()
        )

        total_alerts = len(alerts)

        active_alerts = sum(
            1
            for alert in alerts
            if alert.is_active
        )

        # ========================================================
        # LATEST WEATHER
        # ========================================================
        # IMPORTANT:
        # WeatherData uses recorded_at, NOT timestamp.
        # ========================================================

        latest_weather = (
            self.db.query(WeatherData)
            .order_by(
                WeatherData.recorded_at.desc()
            )
            .first()
        )

        # ========================================================
        # RECOMMENDATIONS
        # ========================================================

        recommendations = (
            self.db.query(Recommendation)
            .order_by(
                Recommendation.created_at.desc()
            )
            .limit(5)
            .all()
        )

        # ========================================================
        # RECENT ALERTS
        # ========================================================

        recent_alerts = (
            self.db.query(Alert)
            .order_by(
                Alert.created_at.desc()
            )
            .limit(5)
            .all()
        )

        # ========================================================
        # RESPONSE
        # ========================================================

        return DashboardSummary(

            total_sensors=total_sensors,

            active_sensors=active_sensors,

            inactive_sensors=inactive_sensors,

            total_alerts=total_alerts,

            active_alerts=active_alerts,

            latest_weather=(
                WeatherResponse.model_validate(
                    latest_weather
                )
                if latest_weather
                else None
            ),

            recommendations=[
                RecommendationResponse.model_validate(
                    recommendation
                )
                for recommendation in recommendations
            ],

            recent_alerts=[
                AlertResponse.model_validate(
                    alert
                )
                for alert in recent_alerts
            ],
        )