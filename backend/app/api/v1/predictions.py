from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.prediction_service import PredictionService


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


# =====================================================
# RUN PREDICTION FOR ONE SENSOR
# =====================================================

@router.post("/run")
def run_prediction(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    service = PredictionService(db)

    try:
        return service.run_prediction(sensor_id)

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )


# =====================================================
# RUN PREDICTION FOR ALL ACTIVE SENSORS
# =====================================================

@router.post("/run-all")
def run_all_predictions(
    db: Session = Depends(get_db),
):
    service = PredictionService(db)

    try:
        return service.run_all_predictions()

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# =====================================================
# GET ALL PREDICTIONS
# =====================================================

@router.get("")
def get_all_predictions(
    db: Session = Depends(get_db),
):
    service = PredictionService(db)

    return service.get_all_predictions()


# =====================================================
# GET PREDICTIONS FOR A SPECIFIC SENSOR
# IMPORTANT: Keep this BEFORE /{prediction_id}
# =====================================================

@router.get("/sensor/{sensor_id}")
def get_sensor_predictions(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    service = PredictionService(db)

    return service.get_sensor_predictions(sensor_id)


# =====================================================
# GET PREDICTION BY ID
# =====================================================

@router.get("/{prediction_id}")
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    service = PredictionService(db)

    prediction = service.get_prediction(
        prediction_id
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    return prediction