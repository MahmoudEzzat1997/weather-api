class AppException(Exception):
    status_code = 500
    detail = "Internal server error."

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class WeatherApiKeyMissingError(AppException):
    status_code = 500
    detail = "Weather API key is not configured. Add WEATHER_API_KEY to your .env file."


class WeatherProviderError(AppException):
    status_code = 502
    detail = "Weather provider request failed."
