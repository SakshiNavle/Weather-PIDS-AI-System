def generate_reason(recommended_sensitivity):
    """
    Returns a human-readable explanation for the prediction.
    """

    reasons = {

        "HIGH":
        "Adverse weather conditions detected. Increase sensor sensitivity.",

        "MEDIUM":
        "Moderate weather conditions require balanced sensor sensitivity.",

        "LOW":
        "Stable weather conditions. Low sensor sensitivity is sufficient."

    }

    return reasons.get(
        recommended_sensitivity,
        "Recommendation unavailable."
    )