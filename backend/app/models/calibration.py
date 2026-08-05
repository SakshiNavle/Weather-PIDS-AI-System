from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class CalibrationHistory(Base):

    __tablename__ = "calibration_history"

    id = Column(Integer, primary_key=True, index=True)

    sensor_id = Column(
        Integer,
        ForeignKey("sensors.id"),
        nullable=False
    )

    old_sensitivity = Column(
        String(20),
        nullable=False
    )

    new_sensitivity = Column(
        String(20),
        nullable=False
    )

    changed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    source = Column(
        String(20),
        default="AI"
    )
    # AI / MANUAL / RULE_ENGINE

    remarks = Column(
        String(255)
    )

    changed_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )