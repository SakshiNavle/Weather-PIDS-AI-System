from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.recommendation_schema import (
    RecommendationCreate,
    RecommendationResponse,
)


class RecommendationService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = RecommendationRepository(db)

    def create_recommendation(
        self,
        recommendation: RecommendationCreate,
    ) -> RecommendationResponse:

        db_recommendation = Recommendation(
            risk_level=recommendation.risk_level,
            title=recommendation.title,
            description=recommendation.description,
            action=recommendation.action,
        )

        self.repository.save(db_recommendation)

        self.db.commit()

        self.db.refresh(db_recommendation)

        return RecommendationResponse.model_validate(db_recommendation)

    def get_all_recommendations(self):

        recommendations = self.repository.find_all()

        return [
            RecommendationResponse.model_validate(r)
            for r in recommendations
        ]

    def get_by_risk_level(
        self,
        risk_level: str,
    ):

        recommendations = self.repository.find_by_risk(risk_level)

        return [
            RecommendationResponse.model_validate(r)
            for r in recommendations
        ]

    def delete_recommendation(
        self,
        recommendation_id: int,
    ):

        recommendation = self.repository.find_by_id(recommendation_id)

        if recommendation is None:
            return False

        self.repository.delete(recommendation)

        self.db.commit()

        return True