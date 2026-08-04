from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.user import User
from app.models.sensor import Sensor
from app.models.weather import WeatherData
from app.models.recommendation import Recommendation
from app.models.calibration import CalibrationHistory
from app.models.alert import Alert

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather-Based Sensor Calibration System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Backend Running Successfully 🚀"
    }