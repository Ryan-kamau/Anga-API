# services/activity_service.py
from core.activity_config import ACTIVITY_RULES
 
def score_weather(weather: dict, rules: dict) -> int:
    """
    Intelligent weather scoring system.

    Positive = suitable
    Negative = unsuitable

    Final score range roughly:
        -15 → terrible
         0  → neutral
        +15 → excellent
    """

    score = 0

    # ─────────────────────────────────────────────
    # 🌡️ Temperature
    # ─────────────────────────────────────────────
    low, high = rules["temp"]
    temp = weather["temp"]

    if low <= temp <= high:
        score += 3

    elif temp < low:
        diff = low - temp

        if diff <= 3:
            score += 1
        elif diff <= 7:
            score -= 2
        else:
            score -= 4

    else:  # temp > high
        diff = temp - high

        if diff <= 3:
            score += 1
        elif diff <= 7:
            score -= 2
        else:
            score -= 4

    # ─────────────────────────────────────────────
    # 💧 Humidity
    # ─────────────────────────────────────────────
    humidity_max = rules["humidity"][1]
    humidity = weather["humidity"]

    if humidity <= humidity_max:
        score += 2

    elif humidity <= humidity_max + 10:
        score += 0

    elif humidity <= humidity_max + 20:
        score -= 2

    else:
        score -= 4

    # ─────────────────────────────────────────────
    # 🌧️ Rain
    # ─────────────────────────────────────────────
    rain_max = rules["rain"][1]
    rain = weather["rain"]

    if rain <= rain_max:
        score += 3

    elif rain <= rain_max + 1:
        score += 0

    elif rain <= rain_max + 3:
        score -= 4

    else:
        score -= 6

    # ─────────────────────────────────────────────
    # 🌬️ Wind Speed
    # ─────────────────────────────────────────────
    wind_max = rules["wind_speed"][1]
    wind = weather["wind_speed"]

    if wind <= wind_max:
        score += 2

    elif wind <= wind_max + 5:
        score -= 1

    else:
        score -= 3

    # ─────────────────────────────────────────────
    # ☁️ Cloud Cover
    # ─────────────────────────────────────────────
    cloud_min, cloud_max = rules["cloud_cover"]
    clouds = weather["cloud_cover"]

    if cloud_min <= clouds <= cloud_max:
        score += 1

    elif clouds <= cloud_max + 20:
        score += 0

    else:
        score -= 2

    return score

def label_score(score: int) -> str:
    """
    Convert numeric score into human-readable rating.
    Updated for negative scoring system.
    """

    if score >= 10:
        return "Excellent"

    elif score >= 6:
        return "Very Good"

    elif score >= 2:
        return "Good"

    elif score >= -2:
        return "Fair"

    elif score >= -6:
        return "Poor"

    else:
        return "Very Poor"


def explain_score(weather: dict, rules: dict) -> str:
    """
    Generate explanation based on BOTH positive and negative conditions.
    """

    reasons = []

    # ─────────────────────────────────────────────
    # 🌡️ Temperature
    # ─────────────────────────────────────────────
    low, high = rules["temp"]
    temp = weather["temp"]

    if low <= temp <= high:
        reasons.append(f"Temperature ({temp}°C) is ideal")

    elif temp < low:
        reasons.append(f"Too cold ({temp}°C)")

    else:
        reasons.append(f"Too hot ({temp}°C)")

    # ─────────────────────────────────────────────
    # 💧 Humidity
    # ─────────────────────────────────────────────
    humidity = weather["humidity"]
    humidity_max = rules["humidity"][1]

    if humidity <= humidity_max:
        reasons.append(f"Humidity ({humidity}%) is comfortable")

    else:
        reasons.append(f"High humidity ({humidity}%) may feel uncomfortable")

    # ─────────────────────────────────────────────
    # 🌧️ Rain
    # ─────────────────────────────────────────────
    rain = weather["rain"]
    rain_max = rules["rain"][1]

    if rain <= rain_max:
        reasons.append("Rain conditions are acceptable")

    elif rain <= rain_max + 2:
        reasons.append("Light rain expected")

    else:
        reasons.append("Heavy rain may affect activity")

    # ─────────────────────────────────────────────
    # 🌬️ Wind
    # ─────────────────────────────────────────────
    wind = weather["wind_speed"]
    wind_max = rules["wind_speed"][1]

    if wind <= wind_max:
        reasons.append(f"Wind speed ({wind} m/s) is manageable")

    else:
        reasons.append(f"Strong wind ({wind} m/s) may interfere")

    # ─────────────────────────────────────────────
    # ☁️ Cloud Cover
    # ─────────────────────────────────────────────
    cloud_min, cloud_max = rules["cloud_cover"]
    clouds = weather["cloud_cover"]

    if cloud_min <= clouds <= cloud_max:
        reasons.append("Cloud conditions are favorable")

    elif clouds > cloud_max:
        reasons.append("Too cloudy")

    else:
        reasons.append("Very clear skies")

    return ", ".join(reasons)


def get_best_times(activity: str, weather_data: list, top_n: int = 5) -> list:
    """
    Rank best time slots for an activity.
    """

    if activity not in ACTIVITY_RULES:
        raise ValueError(
            f"Unknown activity '{activity}'. "
            f"Available: {list(ACTIVITY_RULES.keys())}"
        )

    rules = ACTIVITY_RULES[activity]

    scored = []

    for hour in weather_data:

        score = score_weather(hour, rules)

        scored.append({
            "time": hour["time"],
            "score": score,
            "rating": label_score(score),
            "reason": explain_score(hour, rules),
        })

    # Highest score first
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    return ranked[:top_n]