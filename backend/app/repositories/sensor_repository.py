from sqlalchemy.orm import Session

from app.models.sensor import Sensor


class SensorRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, sensor: Sensor):
        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)

        print("DEBUG SENSOR:", sensor)
        print("DEBUG SENSOR ID:", sensor.id)

        return sensor

    def get_all(self):
        return (
            self.db.query(Sensor)
            .order_by(Sensor.id.asc())
            .all()
        )

    def get_by_id(self, sensor_id: int):
        return (
            self.db.query(Sensor)
            .filter(Sensor.id == sensor_id)
            .first()
        )

    def update(self, sensor: Sensor):
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def delete(self, sensor: Sensor):
        self.db.delete(sensor)
        self.db.commit()