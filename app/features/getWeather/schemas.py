from pydantic import BaseModel, ConfigDict, Field


class WeatherstackLocationDTO(BaseModel):
    name: str
    country: str
    region: str
    localtime: str


class WeatherstackAirQualityDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    us_epa_index: int = Field(alias="us-epa-index")
    gb_defra_index: int = Field(alias="gb-defra-index")


class WeatherstackCurrentDTO(BaseModel):
    temperature: float
    weather_icons: list[str]
    weather_descriptions: list[str]
    air_quality: WeatherstackAirQualityDTO
    wind_speed: float
    wind_degree: int
    wind_dir: str
    pressure: float
    precip: float
    humidity: int
    cloudcover: int
    feelslike: float
    uv_index: float
    visibility: float
    is_day: str


class WeatherstackResponseDTO(BaseModel):
    location: WeatherstackLocationDTO
    current: WeatherstackCurrentDTO


class WeatherLocationDTO(BaseModel):
    city: str
    country: str
    region: str
    localtime: str


class WeatherConditionsDTO(BaseModel):
    temperature: float
    feels_like: float
    description: str
    icon_url: str | None
    is_day: bool


class WeatherWindDTO(BaseModel):
    speed: float
    direction: str
    degree: int


class WeatherAtmosphereDTO(BaseModel):
    humidity: int
    pressure: float
    precipitation: float
    cloud_cover: int
    uv_index: float
    visibility: float


class WeatherAirQualityDTO(BaseModel):
    us_epa_index: int
    gb_defra_index: int


class WeatherResponseDTO(BaseModel):
    location: WeatherLocationDTO
    conditions: WeatherConditionsDTO
    wind: WeatherWindDTO
    atmosphere: WeatherAtmosphereDTO
    air_quality: WeatherAirQualityDTO
