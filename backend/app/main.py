from fastapi import FastAPI

from app.core.database import Base, engine

# Import all models BEFORE create_all
from app.models.user import User
from app.models.sensor import Sensor
from app.models.weather import WeatherData
from app.models.recommendation import Recommendation
from app.models.calibration import CalibrationHistory
from app.models.alert import Alert

from app.auth.auth_router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather PIDS AI System",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Weather PIDS AI System API Running 🚀"}