from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.recommendation_schema import (
    RecommendationCreate,
    RecommendationResponse,
    RecommendationListResponse,
)

from app.services.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
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


# ============================================================
# GET ALL RECOMMENDATIONS
# ============================================================

@router.get(
    "",
    response_model=RecommendationListResponse,
)
def get_all_recommendations(
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)

    return RecommendationListResponse(
        recommendations=
            service.get_all_recommendations()
    )


# ============================================================
# GET RECOMMENDATIONS BY SENSOR
# IMPORTANT: This must come BEFORE /{risk_level}
# ============================================================

@router.get(
    "/sensor/{sensor_id}",
    response_model=list[RecommendationResponse],
)
def get_recommendations_by_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)

    return service.get_by_sensor(
        sensor_id
    )


# ============================================================
# GET RECOMMENDATIONS BY RISK LEVEL
# ============================================================

@router.get(
    "/risk/{risk_level}",
    response_model=list[RecommendationResponse],
)
def get_recommendation_by_risk(
    risk_level: str,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)

    return service.get_by_risk_level(
        risk_level
    )


# ============================================================
# DELETE RECOMMENDATION
# ============================================================

@router.delete(
    "/{recommendation_id}"
)
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)

    success = service.delete_recommendation(
        recommendation_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return {
        "message": "Recommendation deleted successfully"
    }