# ☁️ Anga API

A FastAPI service that fetches real-time weather forecasts and recommends the best time windows for outdoor activities — with scores, ratings, and plain-English explanations.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Running the Server](#running-the-server)
- [API Reference](#api-reference)
  - [GET /anga/weather/details](#get-angaweatherdetails)
  - [GET /anga/activity/best-time](#get-angaactivitybest-time)
- [Response Schemas](#response-schemas)
- [Supported Activities](#supported-activities)
- [Scoring System](#scoring-system)
- [Architecture](#architecture)
- [Adding a New Activity](#adding-a-new-activity)
- [Error Handling](#error-handling)

---

## Overview

Anga ("sky" in Swahili) answers one question: **when is the best time today to do X outside?**

Given a city and an activity, the API:
1. Fetches a 24-hour hourly forecast from OpenWeather
2. Scores each time slot across five weather parameters
3. Returns the top results, ranked best-first, with a human-readable reason for each

---

## Project Structure

```
.
├── main.py                        # FastAPI app entry point
│
├── routers/
│   ├── weather_api.py             # GET /anga/weather/details
│   └── activity_api.py            # GET /anga/activity/best-time
│
├── services/
│   ├── weather_service.py         # OpenWeather fetch + normalisation
│   └── activity_service.py        # Scoring, rating, explanation logic
│
├── core/
│   └── activity_config.py         # Activity weather threshold rules
│
├── schemas/
│   ├── weather.py                 # WeatherSlot, WeatherResponse (Pydantic)
│   └── activity.py                # Recommendation, ActivityResponse (Pydantic)
│
├── .env                           # API keys (not committed)
├── .gitignore
└── requirements.txt
```

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/anga-api.git
cd anga-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

**requirements.txt**

```
fastapi
uvicorn
requests
python-dotenv
pydantic
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_openweathermap_api_key_here
```

Get a free API key at [openweathermap.org](https://openweathermap.org/api).  
The free tier covers the forecast endpoint used by this service.

---

## Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`  
Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

---

## API Reference

### `GET /anga/weather/details`

Returns a normalised 24-hour hourly forecast for a city.

**Query Parameters**

| Parameter | Type   | Required | Description          |
|-----------|--------|----------|----------------------|
| `city`    | string | ✅       | City name, e.g. `Nairobi` |

**Example Request**

```
GET /anga/weather/details?city=Nairobi
```

**Example Response**

```json
{
  "city": "Nairobi",
  "count": 8,
  "forecast": [
    {
      "time": "2026-05-07T06:00:00+00:00",
      "temp": 19.4,
      "humidity": 61,
      "rain": 0.0,
      "wind_speed": 3.2,
      "cloud_cover": 28,
      "is_day": true
    }
  ]
}
```

> **Note:** `time` is always returned as ISO 8601 UTC. OpenWeather's raw Unix timestamp is converted automatically by the schema layer.

---

### `GET /anga/activity/best-time`

Scores and ranks every hourly forecast slot for a given activity. Returns the top N slots with scores, ratings, and explanations.

**Query Parameters**

| Parameter | Type   | Required | Default | Description                          |
|-----------|--------|----------|---------|--------------------------------------|
| `activity`| string | ✅       | —       | Activity name (see Supported Activities) |
| `city`    | string | ✅       | —       | City name, e.g. `Nairobi`            |
| `top_n`   | int    | ❌       | `5`     | Number of results to return (1–24)   |

**Example Request**

```
GET /anga/activity/best-time?activity=running&city=Nairobi
```

**Example Response**

```json
{
  "activity": "running",
  "city": "Nairobi",
  "evaluated_hours": 8,
  "recommendations": [
    {
      "time": "2026-05-07T06:00:00+00:00",
      "score": 11,
      "rating": "Excellent",
      "reason": "Temperature (20°C) is ideal, Humidity (55%) is comfortable, Rain conditions are acceptable, Wind speed (4 m/s) is manageable, Cloud conditions are favorable"
    },
    {
      "time": "2026-05-07T18:00:00+00:00",
      "score": 8,
      "rating": "Very Good",
      "reason": "Temperature (22°C) is ideal, Humidity (60%) is comfortable, Rain conditions are acceptable, Wind speed (5 m/s) is manageable, Cloud conditions are favorable"
    }
  ]
}
```

---

## Response Schemas

### `WeatherResponse`

| Field      | Type               | Description                        |
|------------|--------------------|------------------------------------|
| `city`     | string             | City queried                       |
| `count`    | int                | Number of forecast slots returned  |
| `forecast` | `WeatherSlot[]`    | Ordered hourly forecast            |

### `WeatherSlot`

| Field         | Type   | Description                             |
|---------------|--------|-----------------------------------------|
| `time`        | string | UTC timestamp in ISO 8601 format        |
| `temp`        | float  | Temperature in °C                       |
| `humidity`    | int    | Relative humidity in %                  |
| `rain`        | float  | Rainfall in mm (3-hour accumulation)    |
| `wind_speed`  | float  | Wind speed in m/s                       |
| `cloud_cover` | int    | Cloud cover in %                        |
| `is_day`      | bool   | True if slot falls after local sunrise  |

### `ActivityResponse`

| Field             | Type                 | Description                           |
|-------------------|----------------------|---------------------------------------|
| `activity`        | string               | Activity evaluated                    |
| `city`            | string               | City used for the forecast            |
| `evaluated_hours` | int                  | Total slots that were scored          |
| `recommendations` | `Recommendation[]`   | Top N slots, ranked best-first        |

### `Recommendation`

| Field    | Type   | Description                                       |
|----------|--------|---------------------------------------------------|
| `time`   | string | UTC timestamp in ISO 8601 format                  |
| `score`  | int    | Raw suitability score (higher = better)           |
| `rating` | string | Human-readable band (see Scoring System below)    |
| `reason` | string | Comma-separated explanation of all factors        |

---

## Supported Activities

| Activity        | Key              |
|-----------------|------------------|
| Running         | `running`        |
| Cycling         | `cycling`        |
| Hiking          | `hiking`         |
| Football        | `football`       |
| Outdoor Yoga    | `outdoor_yoga`   |
| Gardening       | `gardening`      |
| Photography     | `photography`    |

Passing an unknown activity returns a `422` error with the full list of valid options.

---

## Scoring System

Each hourly slot is scored across five weather parameters. Scores are additive and can be negative for poor conditions.

| Parameter    | Max points | Penalty trigger                          |
|--------------|-----------|------------------------------------------|
| Temperature  | +3        | Outside ideal range → up to −4          |
| Humidity     | +2        | Over max → up to −4                     |
| Rain         | +3        | Any rain above threshold → up to −6     |
| Wind speed   | +2        | Over max → up to −3                     |
| Cloud cover  | +1        | Far outside range → −2                  |

**Rating bands**

| Score  | Rating     |
|--------|------------|
| ≥ 10   | Excellent  |
| ≥ 6    | Very Good  |
| ≥ 2    | Good       |
| ≥ −2   | Fair       |
| ≥ −6   | Poor       |
| < −6   | Very Poor  |

---

## Architecture

```
Request
  │
  ▼
Router (routers/)
  │  validates query params
  │  catches + maps exceptions to HTTP codes
  │
  ▼
WeatherService (services/weather_service.py)
  │  geocode city → coordinates
  │  fetch 5-day/3-hour forecast from OpenWeather
  │  normalise into internal WeatherSlot format
  │
  ▼
ActivityService (services/activity_service.py)
  │  look up rules from ACTIVITY_RULES
  │  score each slot (score_weather)
  │  label each slot (label_score)
  │  explain each slot (explain_score)
  │  rank and slice top N
  │
  ▼
Pydantic Schema (schemas/)
  │  validates output types
  │  converts Unix timestamps → ISO 8601
  │
  ▼
JSON Response
```

---

## Adding a New Activity

No logic changes required. Open `core/activity_config.py` and add an entry:

```python
"swimming": {
    "temp":        [24, 35],   # °C — warm enough to swim
    "humidity":    [0,  90],   # % — humidity matters less outdoors
    "wind_speed":  [0,  20],   # m/s — wind affects open water
    "rain":        [0,   2],   # mm — light rain is acceptable
    "cloud_cover": [0, 100],   # % — clouds irrelevant for swimming
}
```

The activity is immediately available at `/anga/activity/best-time?activity=swimming&city=...`

---

## Error Handling

| Status | Cause                                           |
|--------|-------------------------------------------------|
| `404`  | City not found or coordinates could not be resolved |
| `422`  | Unknown activity — response includes valid options  |
| `502`  | OpenWeather API is unreachable or returned an error |
| `500`  | Unexpected internal server error                |

**Example 422 response**

```json
{
  "detail": {
    "error": "Unknown activity 'badminton'",
    "available": ["running", "cycling", "hiking", "football", "outdoor_yoga", "gardening", "photography"]
  }
}
```
