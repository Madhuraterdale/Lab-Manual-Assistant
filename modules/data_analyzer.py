import math


def calculate_mean(values):
    if not values:
        return None

    return sum(values) / len(values)


def calculate_percentage_error(experimental, theoretical):
    if theoretical == 0:
        return None

    return abs((experimental - theoretical) / theoretical) * 100


def calculate_percentage(values):
    if not values:
        return []

    total = sum(values)

    if total == 0:
        return [0 for _ in values]

    return [(value / total) * 100 for value in values]


def analyze_data(values, theoretical_value=None):
    result = {}

    if not values:
        return result

    mean = calculate_mean(values)

    result["Number of observations"] = len(values)
    result["Mean"] = mean
    result["Minimum"] = min(values)
    result["Maximum"] = max(values)

    if theoretical_value is not None:
        error = calculate_percentage_error(
            mean,
            theoretical_value
        )

        result["Percentage Error"] = error

    return result