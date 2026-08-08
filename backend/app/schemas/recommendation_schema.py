from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ============================================================
# BASE SCHEMA
# ============================================================

class RecommendationBase(BaseModel):
    sensor_id: int
    risk_level: str
    title: str
    description: str
    action: str


# ============================================================
# CREATE SCHEMA
# ============================================================

class RecommendationCreate(RecommendationBase):
    pass


# ============================================================
# RESPONSE SCHEMA
# ============================================================

class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# LIST RESPONSE SCHEMA
# ============================================================

class RecommendationListResponse(BaseModel):
    recommendations: list[RecommendationResponse]