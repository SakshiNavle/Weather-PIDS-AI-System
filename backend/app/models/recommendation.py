from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Recommendation(Base):

    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    sensor_id = Column(
        Integer,
        ForeignKey("sensors.id"),
        nullable=False
    )

    recommended_sensitivity = Column(
        String(20),
        nullable=False
    )
    # HIGH / MEDIUM / LOW

    confidence_score = Column(
        Float,
        nullable=False
    )

    explanation = Column(
        String(500),
        nullable=False
    )

    recommendation_source = Column(
        String(20),
        default="AI"
    )
    # AI / RULE_ENGINE

    applied = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )