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

    # ============================================================
    # CREATE ALERT
    # ============================================================

    def create_alert(
        self,
        alert: AlertCreate,
    ) -> AlertResponse:

        try:

            # ----------------------------------------------------
            # Prevent duplicate active alerts
            # ----------------------------------------------------

            existing_alert = (
                self.repository.find_active_by_site_and_risk(
                    site_name=alert.site_name,
                    risk_level=alert.risk_level,
                )
            )

            if existing_alert is not None:

                return AlertResponse.model_validate(
                    existing_alert
                )

            # ----------------------------------------------------
            # Create new alert
            # ----------------------------------------------------

            new_alert = Alert(
                **alert.model_dump()
            )

            self.repository.save(new_alert)

            self.db.commit()

            self.db.refresh(new_alert)

            return AlertResponse.model_validate(
                new_alert
            )

        except Exception:

            self.db.rollback()

            raise

    # ============================================================
    # GET ALL ALERTS
    # ============================================================

    def get_all_alerts(self):

        alerts = self.repository.find_all()

        return [
            AlertResponse.model_validate(alert)
            for alert in alerts
        ]

    # ============================================================
    # GET ACTIVE ALERTS
    # ============================================================

    def get_active_alerts(self):

        alerts = self.repository.find_active()

        return [
            AlertResponse.model_validate(alert)
            for alert in alerts
        ]

    # ============================================================
    # GET SINGLE ALERT
    # ============================================================

    def get_alert(
        self,
        alert_id: int,
    ):

        alert = self.repository.find_by_id(
            alert_id
        )

        if alert is None:
            return None

        return AlertResponse.model_validate(
            alert
        )

    # ============================================================
    # UPDATE ALERT
    # ============================================================

    def update_alert(
        self,
        alert_id: int,
        data: AlertUpdate,
    ):

        alert = self.repository.find_by_id(
            alert_id
        )

        if alert is None:
            return None

        try:

            updates = data.model_dump(
                exclude_unset=True
            )

            for key, value in updates.items():

                setattr(
                    alert,
                    key,
                    value
                )

            self.db.commit()

            self.db.refresh(alert)

            return AlertResponse.model_validate(
                alert
            )

        except Exception:

            self.db.rollback()

            raise

    # ============================================================
    # RESOLVE ALERT
    # ============================================================

    def resolve_alert(
        self,
        alert_id: int,
    ):

        alert = self.repository.find_by_id(
            alert_id
        )

        if alert is None:
            return None

        try:

            alert.is_active = False

            self.db.commit()

            self.db.refresh(alert)

            return AlertResponse.model_validate(
                alert
            )

        except Exception:

            self.db.rollback()

            raise

    # ============================================================
    # DELETE ALERT
    # ============================================================

    def delete_alert(
        self,
        alert_id: int,
    ):

        alert = self.repository.find_by_id(
            alert_id
        )

        if alert is None:
            return False

        try:

            self.repository.delete(alert)

            self.db.commit()

            return True

        except Exception:

            self.db.rollback()

            raise