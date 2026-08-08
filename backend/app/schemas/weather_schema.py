from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class WeatherBase(BaseModel):

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
        description="Rainfall in millimeters during the last hour"
    )

    weather_condition: str = Field(
        default="Clear"
    )

    weather_description: str = Field(
        default=""
    )


class WeatherCreate(WeatherBase):
    pass


class WeatherResponse(WeatherBase):

    id: int

    site_name: str

    storm: bool

    weather_risk: str

    timestamp: datetime = Field(
        validation_alias=AliasChoices(
            "timestamp",
            "recorded_at"
        )
    )

    model_config = ConfigDict(
        from_attributes=True
    )


class WeatherCurrentResponse(BaseModel):

    location: str

    weather: WeatherResponse


class WeatherHistoryResponse(BaseModel):

    records: list[WeatherResponse]


class WeatherRefreshResponse(BaseModel):

    success: bool

    message: str

    weather: WeatherResponse