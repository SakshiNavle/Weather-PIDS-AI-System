from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.weather_schema import (
    WeatherCurrentResponse,
    WeatherHistoryResponse,
    WeatherRefreshResponse,
)
from app.services.weather_service import WeatherService

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


@router.get(
    "/current",
    response_model=WeatherCurrentResponse,
)
def get_current_weather(
    city: str = Query(..., description="City name"),
    db: Session = Depends(get_db),
):

    service = WeatherService(db)

    weather = service.fetch_and_store_weather(city)

    return WeatherCurrentResponse(
        location=city,
        weather=weather,
    )


@router.get(
    "/history",
    response_model=WeatherHistoryResponse,
)
def get_weather_history(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):

    service = WeatherService(db)

    records = service.get_weather_history(limit)

    return WeatherHistoryResponse(
        records=records
    )


@router.post(
    "/refresh",
    response_model=WeatherRefreshResponse,
)
def refresh_weather(
    city: str,
    db: Session = Depends(get_db),
):

    service = WeatherService(db)

    weather = service.fetch_and_store_weather(city)

    return WeatherRefreshResponse(
        success=True,
        message="Weather updated successfully.",
        weather=weather,
    )