from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationBase(BaseModel):
    risk_level: str
    title: str
    description: str
    action: str


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class RecommendationListResponse(BaseModel):
    recommendations: list[RecommendationResponse]