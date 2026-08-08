from sqlalchemy.orm import Session

from app.models.prediction import Prediction


class PredictionRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, prediction: Prediction):
        """
        Save a prediction to the database.
        Commit is handled by the service layer.
        """
        self.db.add(prediction)

    def find_all(self):
        """
        Return all predictions (latest first).
        """
        return (
            self.db.query(Prediction)
            .order_by(Prediction.created_at.desc())
            .all()
        )

    def find_by_id(self, prediction_id: int):
        """
        Return a single prediction by ID.
        """
        return (
            self.db.query(Prediction)
            .filter(Prediction.id == prediction_id)
            .first()
        )

    def find_by_sensor(self, sensor_id: int):
        """
        Return prediction history for a sensor.
        """
        return (
            self.db.query(Prediction)
            .filter(Prediction.sensor_id == sensor_id)
            .order_by(Prediction.created_at.desc())
            .all()
        )

    def delete(self, prediction: Prediction):
        """
        Delete a prediction.
        Commit is handled by the service layer.
        """
        self.db.delete(prediction)
    def find_all(self):
        """
        Return all predictions (latest first).
        """
        return (
            self.db.query(Prediction)
            .order_by(Prediction.created_at.desc())
            .all()
        )

    def find_by_id(self, prediction_id: int):
        """
        Return a single prediction by ID.
        """
        return (
            self.db.query(Prediction)
            .filter(Prediction.id == prediction_id)
            .first()
        )

    def find_by_sensor(self, sensor_id: int):
        """
        Return prediction history for a sensor.
        """
        return (
            self.db.query(Prediction)
            .filter(Prediction.sensor_id == sensor_id)
            .order_by(Prediction.created_at.desc())
            .all()
        )