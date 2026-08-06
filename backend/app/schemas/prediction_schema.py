from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PredictionResponse(BaseModel):
    id: int
    sensor_id: int
    recommended_sensitivity: str
    confidence_score: float
    explanation: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class SensorDataResponse(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float


class PredictionRunResponse(BaseModel):
    success: bool
    message: str

    prediction: PredictionResponse

    sensor_data: SensorDataResponse