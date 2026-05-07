# test_scoring.py  — run with: python test_scoring.py
# Simulates what WeatherService.normalize_weather() would return
# so you can test scoring logic without hitting the OpenWeather API.

from core.activity_config import ACTIVITY_RULES
from services.activity_service import score_weather, label_score, explain_score, get_best_times

# ── Fake weather data (matches your normalize_weather schema exactly) ─────────
mock_weather = [
    # Great conditions for running
    {"time": "2026-05-07T06:00:00", "temp": 18, "humidity": 55, "rain": 0,   "wind_speed": 6,  "cloud_cover": 20, "is_day": True},
    # Too hot, humid
    {"time": "2026-05-07T12:00:00", "temp": 32, "humidity": 85, "rain": 0,   "wind_speed": 3,  "cloud_cover": 10, "is_day": True},
    # Raining
    {"time": "2026-05-07T15:00:00", "temp": 20, "humidity": 70, "rain": 4,   "wind_speed": 5,  "cloud_cover": 90, "is_day": True},
    # Good evening window
    {"time": "2026-05-07T18:00:00", "temp": 22, "humidity": 60, "rain": 0,   "wind_speed": 8,  "cloud_cover": 30, "is_day": True},
    # Cold night
    {"time": "2026-05-07T21:00:00", "temp": 11, "humidity": 65, "rain": 0,   "wind_speed": 4,  "cloud_cover": 15, "is_day": False},
]

print("=" * 55)
print("  INDIVIDUAL SLOT SCORES — running")
print("=" * 55)

rules = ACTIVITY_RULES["running"]

for hour in mock_weather:
    s = score_weather(hour, rules)
    print(f"  {hour['time']}  score={s}/10  [{label_score(s)}]")
    print(f"    → {explain_score(hour, rules)}")
    print()

print("=" * 55)
print("  TOP RECOMMENDATIONS — running")
print("=" * 55)

best = get_best_times("running", mock_weather, top_n=3)
for rec in best:
    print(f"  {rec['time']}")
    print(f"    Score : {rec['score']}/10  ({rec['rating']})")
    print(f"    Reason: {rec['reason']}")
    print()