from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.alert_schema import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)
from app.services.alert_service import AlertService

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=AlertResponse,
    status_code=201,
)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
):
    service = AlertService(db)
    return service.create_alert(alert)


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_all_alerts(
    db: Session = Depends(get_db),
):
    service = AlertService(db)
    return service.get_all_alerts()


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    service = AlertService(db)

    alert = service.get_alert(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


@router.put(
    "/{alert_id}",
    response_model=AlertResponse,
)
def update_alert(
    alert_id: int,
    data: AlertUpdate,
    db: Session = Depends(get_db),
):
    service = AlertService(db)

    alert = service.update_alert(
        alert_id,
        data,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


@router.delete(
    "/{alert_id}",
)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    service = AlertService(db)

    deleted = service.delete_alert(alert_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return {
        "message": "Alert deleted successfully"
    }