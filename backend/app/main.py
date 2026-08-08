from fastapi import FastAPI

from app.core.database import Base, engine

# ============================================================
# MODELS
# ============================================================

from app.models.user import User
from app.models.sensor import Sensor
from app.models.weather import WeatherData
from app.models.recommendation import Recommendation
from app.models.calibration import CalibrationHistory
from app.models.alert import Alert
from app.models.prediction import Prediction


# ============================================================
# API ROUTERS
# ============================================================

from app.api.v1.auth import router as auth_router
from app.api.v1.weather import router as weather_router
from app.api.v1.users import router as user_router
from app.api.v1.sensors import router as sensor_router
from app.api.v1.alerts import router as alert_router
from app.api.v1.recommendations import router as recommendation_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.predictions import router as prediction_router


# ============================================================
# SCHEDULER
# ============================================================

from app.scheduler import start_scheduler


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Weather PIDS AI System",
    version="1.0.0",
    description=(
        "AI Based Weather Predictive Intelligence "
        "& Decision Support System"
    ),
)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():
    start_scheduler()


# ============================================================
# API VERSION 1 ROUTES
# ============================================================

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    weather_router,
    prefix="/api/v1",
)

app.include_router(
    sensor_router,
    prefix="/api/v1",
)

app.include_router(
    user_router,
    prefix="/api/v1",
)

app.include_router(
    alert_router,
    prefix="/api/v1",
)

app.include_router(
    recommendation_router,
    prefix="/api/v1",
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
)

app.include_router(
    prediction_router,
    prefix="/api/v1",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Weather PIDS AI System API Running 🚀",
        "version": "1.0.0",
    }