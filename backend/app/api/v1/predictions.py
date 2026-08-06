from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.prediction_schema import PredictionRunResponse
from app.services.prediction_service import PredictionService

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/run",
    response_model=PredictionRunResponse,
)
def run_prediction(
    sensor_id: int,
    db: Session = Depends(get_db),
):

    service = PredictionService(db)

    result = service.run_prediction(sensor_id)
    return PredictionRunResponse(
        success=True,
        message="Prediction generated successfully.",
        prediction=result["prediction"],
        sensor_data=result["sensor_data"],
    )