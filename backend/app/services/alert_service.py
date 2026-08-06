from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert_schema import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)


class AlertService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = AlertRepository(db)

    def create_alert(
        self,
        alert: AlertCreate,
    ) -> AlertResponse:

        new_alert = Alert(**alert.model_dump())

        self.repository.save(new_alert)

        self.db.commit()

        self.db.refresh(new_alert)

        return AlertResponse.model_validate(new_alert)

    def get_all_alerts(self):

        alerts = self.repository.find_all()

        return [
            AlertResponse.model_validate(alert)
            for alert in alerts
        ]

    def get_alert(
        self,
        alert_id: int,
    ):

        alert = self.repository.find_by_id(alert_id)

        if alert is None:
            return None

        return AlertResponse.model_validate(alert)

    def update_alert(
        self,
        alert_id: int,
        data: AlertUpdate,
    ):

        alert = self.repository.find_by_id(alert_id)

        if alert is None:
            return None

        updates = data.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(alert, key, value)

        self.db.commit()

        self.db.refresh(alert)

        return AlertResponse.model_validate(alert)

    def delete_alert(
        self,
        alert_id: int,
    ):

        alert = self.repository.find_by_id(alert_id)

        if alert is None:
            return False

        self.repository.delete(alert)

        self.db.commit()

        return True