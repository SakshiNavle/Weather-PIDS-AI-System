from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor_schema import (
    SensorCreate,
    SensorUpdate,
)


class SensorService:

    def __init__(self, db: Session):
        self.repository = SensorRepository(db)

    def create_sensor(self, sensor: SensorCreate):

        db_sensor = Sensor(**sensor.model_dump())

        return self.repository.create(db_sensor)

    def get_all_sensors(self):

        return self.repository.get_all()

    def get_sensor(self, sensor_id: int):

        sensor = self.repository.get_by_id(sensor_id)

        if sensor is None:
            raise HTTPException(
                status_code=404,
                detail="Sensor not found"
            )

        return sensor

    def update_sensor(
        self,
        sensor_id: int,
        sensor_update: SensorUpdate,
    ):

        sensor = self.get_sensor(sensor_id)

        for key, value in sensor_update.model_dump().items():
            setattr(sensor, key, value)

        return self.repository.update(sensor)

    def delete_sensor(
        self,
        sensor_id: int,
    ):

        sensor = self.get_sensor(sensor_id)

        self.repository.delete(sensor)

        return {
            "message": "Sensor deleted successfully"
        }