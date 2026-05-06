from routers import weather_api
from fastapi import FastAPI

app = FastAPI(title="Anga API")

app.include_router(weather_api.router, prefix="/anga", tags=["Weather"])

