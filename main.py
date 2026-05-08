from routers import weather_api, activity_api
from fastapi import FastAPI

app = FastAPI(title="Anga API", 
            description="Weather-based activity recommendation service",
            version="1.0.0",)

app.include_router(weather_api.router, prefix="/anga", tags=["Weather"])
app.include_router(activity_api.router, prefix="/anga", tags=["Activity"])

