from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WeatherBase(BaseModel):
    """
    Base schema for weather information.
    """

    temperature: float = Field(
        ...,
        description="Temperature in Celsius"
    )

    humidity: float = Field(
        ...,
        ge=0,
        le=100,
        description="Relative humidity percentage"
    )

    wind_speed: float = Field(
        ...,
        ge=0,
        description="Wind speed in meters per second"
    )

    rainfall: float = Field(
        default=0.0,
        ge=0,
        description="Rainfall in millimeters"
    )


class WeatherCreate(WeatherBase):
    """
    Schema used when creating weather records.
    """
    pass


class WeatherResponse(WeatherBase):
    """
    Schema returned to API clients.
    """

    id: int
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class WeatherCurrentResponse(BaseModel):
    """
    Current weather response from the Weather API.
    """

    location: str

    weather: WeatherResponse


class WeatherHistoryResponse(BaseModel):
    """
    Historical weather records.
    """

    records: list[WeatherResponse]


class WeatherRefreshResponse(BaseModel):
    """
    Response after refreshing weather data.
    """

    success: bool

    message: str

    weather: WeatherResponse