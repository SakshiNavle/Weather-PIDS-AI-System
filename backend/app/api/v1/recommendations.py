from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.recommendation_schema import (
    RecommendationCreate,
    RecommendationResponse,
    RecommendationListResponse,
)

from app.services.recommendation_service import (
    RecommendationService,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


# ============================================================
# GET ALL RECOMMENDATIONS
# ============================================================

@router.get(
    "",
    response_model=RecommendationListResponse,
)
def get_recommendations(
    db: Session = Depends(get_db),
):

    service = RecommendationService(db)

    recommendations = (
        service.get_all_recommendations()
    )

    return RecommendationListResponse(
        recommendations=recommendations
    )


# ============================================================
# GET RECOMMENDATIONS BY RISK
# ============================================================

@router.get(
    "/risk/{risk_level}",
    response_model=RecommendationListResponse,
)
def get_recommendations_by_risk(
    risk_level: str,
    db: Session = Depends(get_db),
):

    service = RecommendationService(db)

    recommendations = (
        service.get_by_risk_level(
            risk_level
        )
    )

    return RecommendationListResponse(
        recommendations=recommendations
    )


# ============================================================
# GET RECOMMENDATIONS BY SENSOR
# ============================================================

@router.get(
    "/sensor/{sensor_id}",
    response_model=RecommendationListResponse,
)
def get_recommendations_by_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):

    service = RecommendationService(db)

    recommendations = (
        service.get_by_sensor(
            sensor_id
        )
    )

    return RecommendationListResponse(
        recommendations=recommendations
    )


# ============================================================
# CREATE RECOMMENDATION
# ============================================================

@router.post(
    "",
    response_model=RecommendationResponse,
)
def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db),
):

    service = RecommendationService(db)

    return service.create_recommendation(
        recommendation
    )