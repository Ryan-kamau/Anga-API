# routers/activity_api.py

from fastapi import APIRouter, HTTPException, Query
from services.weather_service import WeatherService
from schema.activity import ActivityResponse
from services.activity_service import get_best_times
from core.activity_config import ACTIVITY_RULES

router = APIRouter()
weather_service = WeatherService()   # shared instance, same pattern as weather_api.py


@router.get("/activity/best-time", response_model=ActivityResponse)
def best_time(
    activity: str = Query(..., description="Activity name, e.g. 'running'"),
    city:     str = Query(..., description="City name, e.g. 'Nairobi'"),
    top_n:    int = Query(5,   description="How many recommendations to return", ge=1, le=24),
):
    """
    Return the top N best time windows for a given activity in a city.

    Flow:
        1. Validate activity exists in config (fast-fail before any HTTP call)
        2. Fetch + normalise weather via WeatherService
        3. Score, rank, and explain each hourly slot via activity_service
        4. Return structured response
    """

    # ── 1. Validate activity early ──────────────────────────────────────────
    if activity not in ACTIVITY_RULES:
        raise HTTPException(
            status_code=422,
            detail={
                "error":     f"Unknown activity '{activity}'",
                "available": list(ACTIVITY_RULES.keys()),
            },
        )

    # ── 2. Fetch weather ─────────────────────────────────────────────────────
    try:
        weather_data = weather_service.get_weather(city)

    except ValueError as e:
        # city not found, bad coordinates, upstream API error
        raise HTTPException(status_code=404, detail=str(e))

    except Exception:
        raise HTTPException(status_code=502, detail="Weather service unavailable")

    # ── 3. Score and rank ────────────────────────────────────────────────────
    try:
        recommendations = get_best_times(activity, weather_data, top_n=top_n)

    except ValueError as e:
        # activity not found (double-check, shouldn't hit after step 1)
        raise HTTPException(status_code=422, detail=str(e))

    # ── 4. Return ────────────────────────────────────────────────────────────
    return {
        "activity":        activity,
        "city":            city,
        "evaluated_hours": len(weather_data),
        "recommendations": recommendations,   # [{time, score, rating, reason}]
    }