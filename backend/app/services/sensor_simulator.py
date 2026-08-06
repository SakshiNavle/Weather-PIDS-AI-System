import random

from ml.src.predictor import predict_sensor


def generate_sensor_data(weather):
    """
    Generate realistic sensor readings by adding
    small variations to live weather data.
    """

    temperature = weather.temperature + random.uniform(-0.5, 0.5)
    humidity = weather.humidity + random.uniform(-2, 2)
    wind_speed = weather.wind_speed + random.uniform(-1, 1)
    rainfall = weather.rainfall

    return {
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "wind_speed": round(wind_speed, 2),
        "rainfall": round(rainfall, 2),
    }


def predict_weather(weather):
    """
    Generate simulated sensor readings
    and send them to the trained ML model.
    """

    sensor_data = generate_sensor_data(weather)

    prediction = predict_sensor(
        temperature=sensor_data["temperature"],
        humidity=sensor_data["humidity"],
        wind_speed=sensor_data["wind_speed"],
        rainfall=sensor_data["rainfall"],
    )

    return {
        "sensor_data": sensor_data,
        "prediction": prediction,
    }