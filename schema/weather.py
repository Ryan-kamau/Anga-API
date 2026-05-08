# schemas/weather.py
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator
from schema.weather import WeatherResponse
from datetime import datetime, timezone


class WeatherSlot(BaseModel):
    """
    A single normalised hourly weather slot as returned by WeatherService.
    The raw OpenWeather 'dt' (Unix UTC int) is converted to an ISO-8601
    string so API consumers get a human-readable timestamp.
    """

    time:        str   = Field(..., description="Localized East Africa Time (EAT) timestamp converted from Unix dt")
    temp:        float = Field(..., description="Temperature in °C")
    humidity:    int   = Field(..., description="Relative humidity in %")
    rain:        float = Field(..., description="Rainfall in mm (3-hour window)")
    wind_speed:  float = Field(..., description="Wind speed in m/s")
    cloud_cover: int   = Field(..., description="Cloud cover in %")
    is_day:      bool  = Field(..., description="True if the slot falls after sunrise")

    @field_validator("time", mode="before")
    @classmethod
    def unix_to_iso(cls, v):
        """Accept either a Unix int or an existing ISO string."""
        if isinstance(v, int):
            formatted = datetime.fromtimestamp(v, tz=ZoneInfo("Africa/Nairobi")).strftime("%Y-%m-%d Time-%H:%M:%S%z")
            return formatted[:-2] + ":" + formatted[-2:]
        return v   # already a string (e.g. from tests / mocks)


class WeatherResponse(BaseModel):
    """Top-level wrapper returned by GET /weather/details."""

    city:    str              = Field(..., description="City queried")
    count:   int              = Field(..., description="Number of hourly slots returned")
    forecast: list[WeatherSlot] = Field(..., description="Ordered hourly forecast slots")