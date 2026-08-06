from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.models.sensor import Sensor
from app.models.weather import WeatherData

from app.repositories.prediction_repository import PredictionRepository
from app.schemas.prediction_schema import PredictionResponse

from app.services.sensor_simulator import predict_weather


class PredictionService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = PredictionRepository(db)

    def run_prediction(self, sensor_id: int):

        # ==========================================
        # Get Sensor
        # ==========================================

        sensor = (
            self.db.query(Sensor)
            .filter(Sensor.id == sensor_id)
            .first()
        )

        if sensor is None:
            raise Exception("Sensor not found.")

        # ==========================================
        # Get Latest Weather
        # ==========================================

        weather = (
            self.db.query(WeatherData)
            .order_by(WeatherData.timestamp.desc())
            .first()
        )

        if weather is None:
            raise Exception("No weather data found.")

        # ==========================================
        # Generate simulated sensor data
        # and run ML prediction
        # ==========================================

        simulation = predict_weather(weather)

        sensor_data = simulation["sensor_data"]

        result = simulation["prediction"]

        # Debug (remove later)
        print("=" * 50)
        print(result)
        print(type(result))
        print("=" * 50)

        # ==========================================
        # Save Prediction
        # ==========================================

        prediction = Prediction(
            sensor_id=sensor.id,
            recommended_sensitivity=result["recommended_sensitivity"],
            confidence_score=result["confidence"],
            explanation=result["reason"],
        )

        self.repository.save(prediction)

        self.db.commit()

        self.db.refresh(prediction)

        # ==========================================
        # Response
        # ==========================================

        return {
            "prediction": PredictionResponse.model_validate(prediction),
            "sensor_data": sensor_data,
        }