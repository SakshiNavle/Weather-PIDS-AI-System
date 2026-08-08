from sqlalchemy.orm import Session

from app.models.alert import Alert


class AlertRepository:

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def save(self, alert: Alert):
        self.db.add(alert)
        return alert

    # ============================================================
    # GET ALL
    # ============================================================

    def find_all(self):
        return (
            self.db.query(Alert)
            .order_by(Alert.created_at.desc())
            .all()
        )

    # ============================================================
    # GET BY ID
    # ============================================================

    def find_by_id(self, alert_id: int):

        return (
            self.db.query(Alert)
            .filter(Alert.id == alert_id)
            .first()
        )

    # ============================================================
    # GET ACTIVE ALERTS
    # ============================================================

    def find_active(self):

        return (
            self.db.query(Alert)
            .filter(Alert.is_active.is_(True))
            .order_by(Alert.created_at.desc())
            .all()
        )

    # ============================================================
    # CHECK DUPLICATE ACTIVE ALERT
    # ============================================================

    def find_active_by_site_and_risk(
        self,
        site_name: str,
        risk_level: str,
    ):

        return (
            self.db.query(Alert)
            .filter(
                Alert.site_name == site_name,
                Alert.risk_level == risk_level,
                Alert.is_active.is_(True),
            )
            .first()
        )

    # ============================================================
    # DELETE
    # ============================================================

    def delete(self, alert: Alert):

        self.db.delete(alert)