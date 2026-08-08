import random


# ============================================================
# SENSOR-SPECIFIC CHARACTERISTICS
# ============================================================

SENSOR_PROFILES = {
    1: {
        "temperature_offset": 0.10,
        "humidity_offset": 1.0,
        "wind_offset": 0.20,
        "temperature_noise": 0.10,
        "humidity_noise": 1.0,
        "wind_noise": 0.40,
    },

    2: {
        "temperature_offset": -0.20,
        "humidity_offset": -1.5,
        "wind_offset": -0.30,
        "temperature_noise": 0.15,
        "humidity_noise": 1.2,
        "wind_noise": 0.50,
    },

    3: {
        "temperature_offset": 0.30,
        "humidity_offset": 2.0,
        "wind_offset": 0.40,
        "temperature_noise": 0.15,
        "humidity_noise": 1.5,
        "wind_noise": 0.60,
    },

    4: {
        "temperature_offset": -0.10,
        "humidity_offset": -1.0,
        "wind_offset": -0.20,
        "temperature_noise": 0.12,
        "humidity_noise": 1.2,
        "wind_noise": 0.50,
    },

    5: {
        "temperature_offset": 0.20,
        "humidity_offset": 1.5,
        "wind_offset": 0.30,
        "temperature_noise": 0.18,
        "humidity_noise": 1.5,
        "wind_noise": 0.60,
    },

    6: {
        "temperature_offset": -0.30,
        "humidity_offset": -2.0,
        "wind_offset": -0.40,
        "temperature_noise": 0.15,
        "humidity_noise": 1.3,
        "wind_noise": 0.55,
    },
}


# ============================================================
# GENERATE SENSOR DATA
# ============================================================

def generate_sensor_data(weather, sensor):
    """
    Generate realistic sensor-specific readings.

    Live weather acts as the environmental baseline.
    Each sensor has its own measurement characteristics
    and small random measurement noise.
    """

    profile = SENSOR_PROFILES.get(
        sensor.id,
        {
            "temperature_offset": 0.0,
            "humidity_offset": 0.0,
            "wind_offset": 0.0,
            "temperature_noise": 0.15,
            "humidity_noise": 1.0,
            "wind_noise": 0.50,
        }
    )

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    temperature = (
        weather.temperature
        + profile["temperature_offset"]
        + random.uniform(
            -profile["temperature_noise"],
            profile["temperature_noise"]
        )
    )

    # --------------------------------------------------------
    # Humidity
    # --------------------------------------------------------

    humidity = (
        weather.humidity
        + profile["humidity_offset"]
        + random.uniform(
            -profile["humidity_noise"],
            profile["humidity_noise"]
        )
    )

    # --------------------------------------------------------
    # Wind
    # --------------------------------------------------------

    wind_speed = (
        weather.wind_speed
        + profile["wind_offset"]
        + random.uniform(
            -profile["wind_noise"],
            profile["wind_noise"]
        )
    )

    # --------------------------------------------------------
    # Rainfall
    # --------------------------------------------------------

    rainfall = weather.rainfall

    # --------------------------------------------------------
    # Physical limits
    # --------------------------------------------------------

    humidity = max(
        0.0,
        min(100.0, humidity)
    )

    wind_speed = max(
        0.0,
        wind_speed
    )

    rainfall = max(
        0.0,
        rainfall
    )

    # --------------------------------------------------------
    # Sensor-type-specific behavior
    # --------------------------------------------------------

    if sensor.sensor_type == "Temperature":

        # Temperature sensor has slightly more
        # precise temperature measurement.

        temperature += random.uniform(
            -0.05,
            0.05
        )

    elif sensor.sensor_type == "Perimeter Fence":

        # Fence sensors are more exposed to wind.

        wind_speed += random.uniform(
            -0.30,
            0.30
        )

    # --------------------------------------------------------
    # Return sensor reading
    # --------------------------------------------------------

    return {
        "sensor_id": sensor.id,
        "sensor_name": sensor.sensor_name,
        "sensor_type": sensor.sensor_type,
        "location": sensor.location,

        "temperature": round(
            temperature,
            2
        ),

        "humidity": round(
            humidity,
            2
        ),

        "wind_speed": round(
            wind_speed,
            2
        ),

        "rainfall": round(
            rainfall,
            2
        ),

        "storm": bool(
            weather.storm
        ),

        "weather_risk": weather.weather_risk,
    }