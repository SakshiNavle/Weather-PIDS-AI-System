from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.models.weather import WeatherData
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation

from app.repositories.prediction_repository import (
    PredictionRepository
)

from app.schemas.prediction_schema import (
    PredictionResponse
)

from app.schemas.alert_schema import AlertCreate

from app.services.ml_service import MLService
from app.services.alert_service import AlertService
from app.services.sensor_simulator import (
    generate_sensor_data
)


class PredictionService:

    def __init__(self, db: Session):

        self.db = db

        self.repository = PredictionRepository(
            db
        )

    # =====================================================
    # RUN SINGLE PREDICTION
    # =====================================================

    def run_prediction(
        self,
        sensor_id: int,
    ):

        # =================================================
        # 1. GET SENSOR
        # =================================================

        sensor = (
            self.db.query(Sensor)
            .filter(
                Sensor.id == sensor_id
            )
            .first()
        )

        if sensor is None:

            raise Exception(
                "Sensor not found."
            )

        # =================================================
        # 2. VALIDATE SENSOR LOCATION
        # =================================================

        if not sensor.location:

            raise Exception(
                "Sensor location is not configured."
            )

        sensor_location = (
            sensor.location.strip()
        )

        # =================================================
        # 3. GET LATEST WEATHER FOR SENSOR LOCATION
        # =================================================
        #
        # IMPORTANT:
        #
        # Do NOT use the globally latest weather.
        #
        # A sensor in Pune should use Pune weather.
        # A sensor in Mumbai should use Mumbai weather.
        #
        # =================================================

        weather = (
            self.db.query(WeatherData)
            .filter(
                WeatherData.site_name
                == sensor_location
            )
            .order_by(
                WeatherData.recorded_at.desc()
            )
            .first()
        )

        # =================================================
        # 4. WEATHER NOT FOUND
        # =================================================

        if weather is None:

            raise Exception(
                f"No weather data available for "
                f"sensor location '{sensor_location}'. "
                f"Run the weather update first."
            )

        # =================================================
        # 5. GENERATE SENSOR-SPECIFIC DATA
        # =================================================

        sensor_data = generate_sensor_data(
            weather,
            sensor
        )

        # =================================================
        # 6. ML PREDICTION
        # =================================================

        result = MLService.predict(
            sensor_data
        )

        recommended_sensitivity = (
            result[
                "recommended_sensitivity"
            ]
        )

        # =================================================
        # 7. UPDATE SENSOR
        # =================================================

        sensor.current_sensitivity = (
            recommended_sensitivity
        )

        sensor.status = "ACTIVE"

        self.db.add(sensor)

        # =================================================
        # 8. SAVE PREDICTION
        # =================================================

        prediction = Prediction(

            sensor_id=sensor.id,

            recommended_sensitivity=(
                recommended_sensitivity
            ),

            confidence_score=(
                result["confidence"]
            ),

            explanation=(
                result["reason"]
            ),
        )

        self.repository.save(
            prediction
        )

        # =================================================
        # 9. SAVE RECOMMENDATION
        # =================================================

        recommendation = Recommendation(

            sensor_id=sensor.id,

            risk_level=(
                weather.weather_risk
            ),

            title=(
                f"{sensor.sensor_name} "
                f"Calibration"
            ),

            description=(
                result["reason"]
            ),

            action=(
                f"Set sensitivity to "
                f"{recommended_sensitivity}"
            ),
        )

        self.db.add(
            recommendation
        )

        # =================================================
        # 10. COMMIT
        # =================================================

        self.db.commit()

        self.db.refresh(sensor)

        self.db.refresh(prediction)

        self.db.refresh(
            recommendation
        )

        # =================================================
        # 11. GENERATE ALERT
        # =================================================

        if weather.weather_risk in [
            "HIGH",
            "SEVERE",
        ]:

            alert_service = AlertService(
                self.db
            )

            alert_service.create_alert(

                AlertCreate(

                    site_name=(
                        sensor.location
                    ),

                    risk_level=(
                        weather.weather_risk
                    ),

                    message=(
                        f"{sensor.sensor_name} "
                        f"at {sensor.location} "
                        f"requires "
                        f"{recommended_sensitivity} "
                        f"sensitivity."
                    ),

                    is_active=True,
                )
            )

        # =================================================
        # 12. RETURN
        # =================================================

        return {

            "prediction": (
                PredictionResponse
                .model_validate(
                    prediction
                )
            ),

            "sensor_data": sensor_data,
        }

    # =====================================================
    # RUN ALL PREDICTIONS
    # =====================================================

    def run_all_predictions(self):

        sensors = (
            self.db.query(Sensor)
            .order_by(
                Sensor.id
            )
            .all()
        )

        if not sensors:

            return {
                "total_sensors": 0,
                "successful_predictions": 0,
                "failed_predictions": 0,
                "results": [],
            }

        results = []

        successful = 0

        failed = 0

        # =================================================
        # PROCESS EACH SENSOR
        # =================================================

        for sensor in sensors:

            try:

                result = (
                    self.run_prediction(
                        sensor.id
                    )
                )

                results.append({

                    "sensor_id": sensor.id,

                    "sensor_name": (
                        sensor.sensor_name
                    ),

                    "location": (
                        sensor.location
                    ),

                    "status": "SUCCESS",

                    "result": result,
                })

                successful += 1

            except Exception as ex:

                self.db.rollback()

                failed += 1

                results.append({

                    "sensor_id": sensor.id,

                    "sensor_name": (
                        sensor.sensor_name
                    ),

                    "location": (
                        sensor.location
                    ),

                    "status": "FAILED",

                    "error": str(ex),
                })

        # =================================================
        # RETURN SUMMARY
        # =================================================

        return {

            "total_sensors": len(
                sensors
            ),

            "successful_predictions": (
                successful
            ),

            "failed_predictions": (
                failed
            ),

            "results": results,
        }

    # =====================================================
    # GET ALL PREDICTIONS
    # =====================================================

    def get_all_predictions(self):

        predictions = (
            self.repository.find_all()
        )

        return [

            PredictionResponse.model_validate(
                prediction
            )

            for prediction in predictions
        ]

    # =====================================================
    # GET SINGLE PREDICTION
    # =====================================================

    def get_prediction(
        self,
        prediction_id: int,
    ):

        prediction = (
            self.repository.find_by_id(
                prediction_id
            )
        )

        if prediction is None:

            return None

        return (
            PredictionResponse
            .model_validate(
                prediction
            )
        )

    # =====================================================
    # GET SENSOR PREDICTIONS
    # =====================================================

    def get_sensor_predictions(
        self,
        sensor_id: int,
    ):

        predictions = (
            self.repository.find_by_sensor(
                sensor_id
            )
        )

        return [

            PredictionResponse.model_validate(
                prediction
            )

            for prediction in predictions
        ]