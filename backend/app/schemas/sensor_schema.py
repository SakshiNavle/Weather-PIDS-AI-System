from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    sensor_name: str
    sensor_type: str
    location: str
    current_sensitivity: str
    status: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    sensor_name: str | None = None
    sensor_type: str | None = None
    location: str | None = None
    current_sensitivity: str | None = None
    status: str | None = None


class SensorResponse(SensorBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )