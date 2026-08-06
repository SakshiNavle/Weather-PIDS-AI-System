from sqlalchemy.orm import Session

from app.models.alert import Alert


class AlertRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, alert: Alert):
        self.db.add(alert)

    def find_all(self):
        return (
            self.db.query(Alert)
            .order_by(Alert.created_at.desc())
            .all()
        )

    def find_by_id(self, alert_id: int):
        return (
            self.db.query(Alert)
            .filter(Alert.id == alert_id)
            .first()
        )

    def delete(self, alert: Alert):
        self.db.delete(alert)