from pydantic import BaseModel

from app.schemas.weather_schema import WeatherResponse
from app.schemas.alert_schema import AlertResponse
from app.schemas.recommendation_schema import RecommendationResponse


class DashboardSummary(BaseModel):
    total_sensors: int
    active_sensors: int
    inactive_sensors: int

    total_alerts: int
    active_alerts: int

    latest_weather: WeatherResponse | None

    recommendations: list[RecommendationResponse]

    recent_alerts: list[AlertResponse]