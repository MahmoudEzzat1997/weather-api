from typing import Any, Callable

from fastapi import APIRouter, Depends, Request, Response

from app.features.getWeather.interfaces import IWeatherService
from app.features.getWeather.schemas import WeatherResponseDTO
from app.dependencies import get_weather_service
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/weather", tags=["Weather"])


def weather_cache_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Request | None = None,
    response: Response | None = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    city = ""
    if request is not None:
        city = request.path_params.get("city", "")
    if not city:
        city = kwargs.get("city", "")

    normalized_city = str(city).strip().lower()
    return f"{namespace}:{func.__module__}.{func.__name__}:city={normalized_city}"


@router.get("/{city}", response_model=WeatherResponseDTO)
@cache(expire=1800, key_builder=weather_cache_key_builder)
async def get_weather(
    city: str,
    service: IWeatherService = Depends(get_weather_service)
) -> WeatherResponseDTO:
    return await service.get_weather(city)
