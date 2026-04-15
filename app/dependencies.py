import httpx
from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.http_client import get_http_client
from app.features.getWeather.client import WeatherstackClient
from app.features.getWeather.interfaces import IWeatherClient, IWeatherService
from app.features.getWeather.service import WeatherService


def get_weather_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
    settings: Settings = Depends(get_settings),
) -> IWeatherClient:
    return WeatherstackClient(http_client=http_client, settings=settings)


def get_weather_service(
    weather_client: IWeatherClient = Depends(get_weather_client),
) -> IWeatherService:
    return WeatherService(weather_client=weather_client)
