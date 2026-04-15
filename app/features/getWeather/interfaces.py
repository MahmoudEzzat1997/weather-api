from abc import ABC, abstractmethod

from app.features.getWeather.schemas import WeatherResponseDTO, WeatherstackResponseDTO


class IWeatherClient(ABC):

    @abstractmethod
    async def fetch_weather(self, city: str) -> WeatherstackResponseDTO:
        pass


class IWeatherService(ABC):

    @abstractmethod
    async def get_weather(self, city: str) -> WeatherResponseDTO:
        pass
