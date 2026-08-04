from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer)

    message = Column(String(300))

    severity = Column(String(20))

    created_at = Column(DateTime(timezone=True), server_default=func.now())