from app.common.exceptions import WeatherProviderError
from app.features.getWeather.interfaces import IWeatherClient, IWeatherService
from app.features.getWeather.schemas import (
    WeatherAirQualityDTO,
    WeatherAtmosphereDTO,
    WeatherConditionsDTO,
    WeatherLocationDTO,
    WeatherResponseDTO,
    WeatherWindDTO,
)


class WeatherService(IWeatherService):

    def __init__(self, weather_client: IWeatherClient) -> None:
        self._weather_client = weather_client

    async def get_weather(self, city: str) -> WeatherResponseDTO:
        data = await self._weather_client.fetch_weather(city)

        try:
            return WeatherResponseDTO(
                location=WeatherLocationDTO(
                    city=data.location.name,
                    country=data.location.country,
                    region=data.location.region,
                    localtime=data.location.localtime,
                ),
                conditions=WeatherConditionsDTO(
                    temperature=data.current.temperature,
                    feels_like=data.current.feelslike,
                    description=data.current.weather_descriptions[0].strip(),
                    icon_url=(
                        data.current.weather_icons[0]
                        if data.current.weather_icons
                        else None
                    ),
                    is_day=data.current.is_day.lower() == "yes",
                ),
                wind=WeatherWindDTO(
                    speed=data.current.wind_speed,
                    direction=data.current.wind_dir,
                    degree=data.current.wind_degree,
                ),
                atmosphere=WeatherAtmosphereDTO(
                    humidity=data.current.humidity,
                    pressure=data.current.pressure,
                    precipitation=data.current.precip,
                    cloud_cover=data.current.cloudcover,
                    uv_index=data.current.uv_index,
                    visibility=data.current.visibility,
                ),
                air_quality=WeatherAirQualityDTO(
                    us_epa_index=data.current.air_quality.us_epa_index,
                    gb_defra_index=data.current.air_quality.gb_defra_index,
                ),
            )
        except IndexError as exc:
            raise WeatherProviderError("Weather provider returned an unexpected response.") from exc
