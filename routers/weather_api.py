from fastapi import APIRouter, HTTPException
from services.weather_service import WeatherService
from fastapi import HTTPException
from schema.weather import WeatherResponse

router = APIRouter()
weather_service = WeatherService()  # single instance

@router.get("/weather/details", response_model=WeatherResponse)
def get_weather_details(city: str):
    try:
        return weather_service.get_weather(city)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")