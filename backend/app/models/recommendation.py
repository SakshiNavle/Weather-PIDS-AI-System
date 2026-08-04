from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Recommendation(Base):

    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer)

    recommended_sensitivity = Column(String(20))

    confidence = Column(Float)

    explanation = Column(String(300))

    created_at = Column(DateTime(timezone=True), server_default=func.now())