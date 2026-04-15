import httpx
from pydantic import ValidationError

from app.common.exceptions import WeatherApiKeyMissingError, WeatherProviderError
from app.core.config import Settings
from app.features.getWeather.interfaces import IWeatherClient
from app.features.getWeather.schemas import WeatherstackResponseDTO


class WeatherstackClient(IWeatherClient):

    def __init__(self, http_client: httpx.AsyncClient, settings: Settings) -> None:
        self._http_client = http_client
        self._settings = settings

    async def fetch_weather(self, city: str) -> WeatherstackResponseDTO:
        if not self._settings.weather_api_key:
            raise WeatherApiKeyMissingError()

        try:
            response = await self._http_client.get(
                "/current",
                params={
                    "access_key": self._settings.weather_api_key,
                    "query": city,
                },
            )
        except httpx.HTTPError as exc:
            raise WeatherProviderError() from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise WeatherProviderError() from exc

        if data.get("success") is False:
            error = data.get("error", {})
            raise WeatherProviderError(error.get("info", "Weather provider returned an error."))

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise WeatherProviderError() from exc

        try:
            return WeatherstackResponseDTO.model_validate(data)
        except ValidationError as exc:
            raise WeatherProviderError("Weather provider returned an unexpected response.") from exc
