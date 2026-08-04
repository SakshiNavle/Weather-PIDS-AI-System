from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class CalibrationHistory(Base):

    __tablename__ = "calibration_history"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer)

    old_sensitivity = Column(String(20))

    new_sensitivity = Column(String(20))

    changed_by = Column(String(100))

    changed_at = Column(DateTime(timezone=True), server_default=func.now())