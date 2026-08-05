from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.sensor import Sensor


class SensorRepository:
    """
    Handles only database operations
    """


    def __init__(self, db: Session):
        self.db = db


    def get_all(self) -> List[Sensor]:

        return self.db.query(Sensor).all()


    def get_by_id(
        self,
        sensor_id: int
    ) -> Optional[Sensor]:

        return (
            self.db.query(Sensor)
            .filter(
                Sensor.id == sensor_id
            )
            .first()
        )


    def create(
        self,
        sensor: Sensor
    ) -> Sensor:

        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)

        return sensor


    def update(
        self,
        sensor: Sensor
    ) -> Sensor:

        self.db.commit()
        self.db.refresh(sensor)

        return sensor


    def delete(
        self,
        sensor: Sensor
    ):

        self.db.delete(sensor)
        self.db.commit()