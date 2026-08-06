from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    sensor_id = Column(Integer, nullable=False)

    recommended_sensitivity = Column(String(20), nullable=False)

    confidence_score = Column(Float, nullable=False)

    explanation = Column(String(500), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )