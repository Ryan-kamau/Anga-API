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
            raise ValueError("City not found")

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

        if response.status_code != 200:
            raise ValueError(f"Weather API failed: {response.text}")

        data = response.json()

        # 🔥 critical check
        if "current" not in data:
            raise ValueError(f"Unexpected API response: {data}")

        return data

      # 🔹 Step 3: Normalize
    def normalize_weather(self, data):
        hourly = data.get("hourly", [])
        current = data.get("current")

        if not current:
            raise ValueError("Missing current weather data")

        sunrise = current.get("sunrise", 0)

        return [
            {
                "time": hour.get("dt"),
                "temp": hour.get("temp"),
                "humidity": hour.get("humidity"),
                "rain": hour.get("rain", {}).get("1h", 0),
                "wind_speed": hour.get("wind_speed"),
                "cloud_cover": hour.get("clouds"),
                "is_day": hour.get("dt", 0) > sunrise
            }
            for hour in hourly[:24]
        ]

    # 🔹 Public method (entry point)
    def get_weather(self, city: str):
        lat, lon = self.get_coordinates(city)
        if lat is None or lon is None:
            raise ValueError("Invalid coordinates")
        
        raw_data = self.fetch_weather(lat, lon)
        if not raw_data:
            raise ValueError("Failed to fetch weather data")
        print("RAW WEATHER RESPONSE:", raw_data)
        return self.normalize_weather(raw_data)



