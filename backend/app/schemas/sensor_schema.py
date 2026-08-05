from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    sensor_name: str
    sensor_type: str
    location: str
    current_sensitivity: str
    status: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(SensorBase):
    pass


class SensorResponse(SensorBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )