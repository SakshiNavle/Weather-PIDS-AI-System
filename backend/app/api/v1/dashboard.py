from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dashboard_schema import DashboardSummary
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardSummary,
)
def get_dashboard(
    db: Session = Depends(get_db),
):

    service = DashboardService(db)

    return service.get_dashboard()