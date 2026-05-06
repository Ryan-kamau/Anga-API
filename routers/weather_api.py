from fastapi import APIRouter
from services.weather_service import WeatherService

router = APIRouter()
weather_service = WeatherService()  # single instance

@router.get("/weather/{city}")
def get_weather(city: str):
    return weather_service.get_weather(city)