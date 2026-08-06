from sqlalchemy.orm import Session

from app.models.prediction import Prediction


class PredictionRepository:

    def __init__(self, db: Session):
        self.db = db


    def save(self, prediction):
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)

        return prediction


    def get_all(self):
        return self.db.query(Prediction).all()


    def get_by_id(self, prediction_id: int):
        return (
            self.db.query(Prediction)
            .filter(Prediction.id == prediction_id)
            .first()
        )