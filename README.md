# Weather API

A FastAPI service that integrates with WeatherAPI.com to provide current weather data by city.

---

## Features

- Real-time weather data by city name
- In-memory caching to reduce external API calls and improve latency
- Dependency injection via FastAPI's `Depends`
- Vertical slice architecture for rapid development
- Dockerized for easy deployment

---

## Architecture

This project uses **Vertical Slice Architecture**, 
organizing code by feature rather than layer. 
This was chosen over Clean Architecture to minimize boilerplate
and speed up development.

```
app/
├── common/          # Shared exceptions and middleware
├── core/            # Configuration and HTTP client
├── features/
│   └── getWeather/  # All weather feature logic (client, service, router, schemas)
├── dependencies.py  # DI bindings
└── main.py          # App entrypoint
```

---

## Caching Strategy

- **Settings** — cached with `@lru_cache` since settings never change and always return the same result
- **Weather endpoint** — cached with an in-memory cache (30min TTL) to reduce calls to WeatherAPI.com and lower latency
GET /weather/Cairo => hits cache
GET /weather/cairo => hits same cache entry
GET /weather/London => gets its own cache entry
---


## Production Environment 
1. Distributed Cache (Redis). The current in-memory cache is just for light traffic and doesn't support scaling, so it breaks with multiple workers or containers. Redis would be shared across all instances.
2. Structured Logging to Replace plain print/default logs with structlog or loguru to get JSON logs with request IDs, timestamps, and context — essential for debugging in production.
3. Rate Limiting to prevent API abuse and securing the limited quota
Add per-IP rate limiting (e.g. slowapi) to prevent abuse and protect the upstream WeatherAPI.com quota.
4. Proper CI/CD pipeline for streamlined development process
5. Move away from a plain .env file toward a proper secrets manager like Azure Key Vault
## Getting Started

### Prerequisites

- Docker & Docker Compose

### Environment Variables
No .env file exists in the dockerized version or the source code for 
security reasons (.env contains the API Key)
Create a `.env` file in the project root:
```env
WEATHER_API_KEY=your_weatherapi_key
WEATHER_BASE_URL=http://api.weatherapi.com
```

### Run with Docker

```powershell
# Build and start
docker compose up --build

# Stop
docker compose down
```

---

## Usage

### Get Weather by City

- **Endpoint:** `GET /weather/{city}`
- **Example:**

```powershell
curl.exe http://127.0.0.1:8000/weather/Cairo
```

**Response:**

```json
{
  "location": {
    "city": "Cairo",
    "country": "Egypt",
    "region": "Al Qahirah",
    "localtime": "2026-04-15 15:19"
  },
  "conditions": {
    "temperature": 31.0,
    "feels_like": 29.0,
    "description": "Sunny",
    "icon_url": "https://example.com/sunny.png",
    "is_day": true
  },
  "wind": {
    "speed": 9.0,
    "direction": "NE"
  },
  "atmosphere": {
    "humidity": 27,
    "pressure": 1009.0,
    "precipitation": 0.0,
    "cloud_cover": 0,
    "uv_index": 4.0,
    "visibility": 10.0
  },
  "air_quality": {
    "us_epa_index": 2,
    "gb_defra_index": 2
  }
}
```

### Other Endpoints

- `GET /` — Welcome message
- `GET /health` — Health check
- `GET /docs` — Swagger UI

---

## Running Tests

```powershell
pytest tests/
--No tests Yet just the Package as a placeholder--
```
