import requests
from dotenv import load_dotenv
import os

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.weather_url = "https://api.openweathermap.org/data/2.5/onecall"

        if not self.api_key:
            raise ValueError("Missing WEATHER_API_KEY in .env")

    # 🔹 Step 1: Get coordinates
    def get_coordinates(self, city: str):
        params = {
            "q": city,
            "limit": 1,
            "appid": self.api_key
        }

        response = requests.get(self.geo_url, params=params)
        data = response.json()

        if not data:
            raise Exception("City not found")

        return data[0]["lat"], data[0]["lon"]

    # 🔹 Step 2: Fetch weather
    def fetch_weather(self, lat: float, lon: float):
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,daily,alerts",
            "units": "metric",
            "appid": self.api_key
        }

        response = requests.get(self.weather_url, params=params)
        return response.json()

      # 🔹 Step 3: Normalize
    def normalize_weather(self, data):
        hourly = data.get("hourly", [])
        sunrise = data["current"]["sunrise"]
        return [
            {
                "time": hour["dt"],
                "temp": hour["temp"],
                "humidity": hour["humidity"],
                "rain": hour.get("rain", {}).get("1h", 0),
                "wind_speed": hour["wind_speed"],
                "cloud_cover": hour["clouds"],
                "is_day": hour["dt"] > sunrise
            }
            for hour in hourly[:24]
        ]

    # 🔹 Public method (entry point)
    def get_weather(self, city: str):
        lat, lon = self.get_coordinates(city)
        raw_data = self.fetch_weather(lat, lon)
        return self.normalize_weather(raw_data)



