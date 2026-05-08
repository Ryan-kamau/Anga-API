# schemas/activity.py
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Literal


# Exhaustive set — mirrors label_score() in activity_service.py exactly.
RatingLiteral = Literal["Excellent", "Very Good", "Good", "Fair", "Poor", "Very Poor"]


class Recommendation(BaseModel):
    """
    A single scored and explained time slot for an activity.
    """

    time:   str           = Field(..., description="Localized East Africa Time (EAT) timestamp converted from Unix dt")
    score:  int           = Field(..., description="Raw suitability score (higher = better)")
    rating: RatingLiteral = Field(..., description="Human-readable band derived from score")
    reason: str           = Field(..., description="Comma-separated explanation of contributing factors")

    @field_validator("time", mode="before")
    @classmethod
    def unix_to_iso(cls, v):
        """Same conversion as WeatherSlot — keeps output consistent."""
        if isinstance(v, int):
            formatted = datetime.fromtimestamp(v, tz=ZoneInfo("Africa/Nairobi")).strftime("%Y-%m-%d Time-%H:%M:%S%z")
            return formatted[:-2] + ":" + formatted[-2:]
        return v


class ActivityResponse(BaseModel):
    """
    Top-level envelope returned by GET /activity/best-time.
    """

    activity:        str                  = Field(..., description="Activity that was evaluated")
    city:            str                  = Field(..., description="City used for the forecast")
    evaluated_hours: int                  = Field(..., description="Total hourly slots that were scored")
    recommendations: list[Recommendation] = Field(..., description="Top N slots, ranked best-first")


class ErrorDetail(BaseModel):
    """
    Structured error body for 422 (unknown activity) responses.
    Gives consumers the list of valid values so they can self-correct.
    """

    error:     str       = Field(..., description="Human-readable error message")
    available: list[str] = Field(..., description="Valid activity names")