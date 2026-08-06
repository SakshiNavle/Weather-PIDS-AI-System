from ml.src.inference import predict


def predict_sensor(
    temperature,
    humidity,
    wind_speed,
    rainfall
):
    """
    Wrapper function used by the backend.

    Returns:
        Prediction dictionary.
    """

    return predict(
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        rainfall=rainfall
    )