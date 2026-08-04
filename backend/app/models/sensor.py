from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Sensor(Base):

    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)

    sensor_name = Column(String(100), nullable=False)

    sensor_type = Column(String(50))

    location = Column(String(150))

    current_sensitivity = Column(String(20))

    status = Column(String(20))