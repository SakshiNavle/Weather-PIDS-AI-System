from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.sensor_schema import (
    SensorCreate,
    SensorUpdate,
    SensorResponse,
)
from app.services.sensor_service import SensorService

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"],
)


@router.post(
    "",
    response_model=SensorResponse,
    status_code=201,
)
def create_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db),
):
    service = SensorService(db)
    return service.create_sensor(sensor)


@router.get(
    "",
    response_model=list[SensorResponse],
)
def get_all_sensors(
    db: Session = Depends(get_db),
):
    service = SensorService(db)
    return service.get_all_sensors()


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    service = SensorService(db)
    return service.get_sensor(sensor_id)


@router.put(
    "/{sensor_id}",
    response_model=SensorResponse,
)
def update_sensor(
    sensor_id: int,
    sensor: SensorUpdate,
    db: Session = Depends(get_db),
):
    service = SensorService(db)
    return service.update_sensor(sensor_id, sensor)


@router.delete(
    "/{sensor_id}",
)
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    service = SensorService(db)
    return service.delete_sensor(sensor_id)