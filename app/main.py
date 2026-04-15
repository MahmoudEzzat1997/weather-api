from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.common.middleware import register_exception_handlers
from app.core.http_client import close_http_client
from app.features.getWeather.router import router as get_weather_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_http_client()

app = FastAPI(
    title="Weather API",
    version="0.1.0",
    lifespan=lifespan,
)

# Initialize the cache once globally with in-memory backend
in_memory_backend = InMemoryBackend()
FastAPICache.init(in_memory_backend, prefix="weather-cache")
register_exception_handlers(app)
app.include_router(get_weather_router)
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Weather API! Visit /docs for API documentation."}

@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

