# core/activity_config.py

"""
Activity weather thresholds.

Each activity defines ideal weather ranges:
[min, max] inclusive

The scoring engine uses these thresholds
to determine how suitable weather conditions are
for a given activity.

This acts as the core "knowledge layer"
for the recommendation engine.
"""

ACTIVITY_RULES: dict[str, dict[str, list[int]]] = {

    # ─────────────────────────────────────────────
    # 🏃 Fitness / Outdoor Sports
    # ─────────────────────────────────────────────

    "running": {
        "temp":        [15, 25],
        "humidity":    [0, 70],
        "wind_speed":  [0, 10],
        "rain":        [0, 0],
        "cloud_cover": [0, 50],
    },

    "cycling": {
        "temp":        [12, 28],
        "humidity":    [0, 70],
        "wind_speed":  [0, 8],
        "rain":        [0, 0],
        "cloud_cover": [0, 60],
    },

    "hiking": {
        "temp":        [10, 30],
        "humidity":    [0, 80],
        "wind_speed":  [0, 15],
        "rain":        [0, 2],
        "cloud_cover": [0, 70],
    },

    "football": {
        "temp":        [16, 28],
        "humidity":    [0, 75],
        "wind_speed":  [0, 12],
        "rain":        [0, 3],
        "cloud_cover": [0, 80],
    },

    "basketball": {
        "temp":        [18, 30],
        "humidity":    [0, 70],
        "wind_speed":  [0, 8],
        "rain":        [0, 0],
        "cloud_cover": [0, 60],
    },

    "swimming": {
        "temp":        [24, 35],
        "humidity":    [0, 85],
        "wind_speed":  [0, 10],
        "rain":        [0, 1],
        "cloud_cover": [0, 40],
    },

    "outdoor_yoga": {
        "temp":        [18, 30],
        "humidity":    [0, 65],
        "wind_speed":  [0, 5],
        "rain":        [0, 0],
        "cloud_cover": [10, 50],
    },

    # ─────────────────────────────────────────────
    # 🧺 Daily Lifestyle Activities
    # ─────────────────────────────────────────────

    "washing_laundry": {
        "temp":        [20, 35],
        "humidity":    [0, 60],
        "wind_speed":  [1, 10],
        "rain":        [0, 0],
        "cloud_cover": [0, 40],
    },

    "house_cleaning": {
        "temp":        [18, 30],
        "humidity":    [0, 75],
        "wind_speed":  [0, 15],
        "rain":        [0, 10],
        "cloud_cover": [0, 100],
    },

    "grocery_shopping": {
        "temp":        [18, 30],
        "humidity":    [0, 80],
        "wind_speed":  [0, 15],
        "rain":        [0, 2],
        "cloud_cover": [0, 100],
    },

    "motorbike_riding": {
        "temp":        [18, 28],
        "humidity":    [0, 75],
        "wind_speed":  [0, 12],
        "rain":        [0, 1],
        "cloud_cover": [0, 70],
    },

    "gardening": {
        "temp":        [12, 30],
        "humidity":    [0, 80],
        "wind_speed":  [0, 15],
        "rain":        [0, 2],
        "cloud_cover": [0, 90],
    },

    "farming": {
        "temp":        [15, 30],
        "humidity":    [20, 80],
        "wind_speed":  [0, 12],
        "rain":        [0, 5],
        "cloud_cover": [0, 80],
    },

    "construction_work": {
        "temp":        [15, 28],
        "humidity":    [0, 70],
        "wind_speed":  [0, 10],
        "rain":        [0, 1],
        "cloud_cover": [0, 60],
    },

    # ─────────────────────────────────────────────
    # ❤️ Social / Leisure
    # ─────────────────────────────────────────────

    "going_on_dates": {
        "temp":        [18, 27],
        "humidity":    [0, 75],
        "wind_speed":  [0, 10],
        "rain":        [0, 1],
        "cloud_cover": [0, 60],
    },

    "bbq": {
        "temp":        [20, 32],
        "humidity":    [0, 70],
        "wind_speed":  [0, 10],
        "rain":        [0, 0],
        "cloud_cover": [0, 50],
    },

    "picnic": {
        "temp":        [20, 30],
        "humidity":    [0, 70],
        "wind_speed":  [0, 8],
        "rain":        [0, 0],
        "cloud_cover": [0, 50],
    },

    "watching_sunset": {
        "temp":        [18, 28],
        "humidity":    [0, 75],
        "wind_speed":  [0, 8],
        "rain":        [0, 0],
        "cloud_cover": [0, 40],
    },

    "outdoor_reading": {
        "temp":        [18, 28],
        "humidity":    [0, 70],
        "wind_speed":  [0, 6],
        "rain":        [0, 0],
        "cloud_cover": [10, 60],
    },

    "photography": {
        "temp":        [5, 35],
        "humidity":    [0, 85],
        "wind_speed":  [0, 20],
        "rain":        [0, 0],
        "cloud_cover": [20, 60],
    },
}