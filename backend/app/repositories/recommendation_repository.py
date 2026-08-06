from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation


class RecommendationRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, recommendation: Recommendation):
        self.db.add(recommendation)

    def find_all(self):
        return (
            self.db.query(Recommendation)
            .order_by(Recommendation.created_at.desc())
            .all()
        )

    def find_by_id(self, recommendation_id: int):
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.id == recommendation_id)
            .first()
        )

    def find_by_risk(self, risk_level: str):
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.risk_level == risk_level)
            .all()
        )

    def delete(self, recommendation: Recommendation):
        self.db.delete(recommendation)