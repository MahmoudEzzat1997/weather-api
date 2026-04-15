import httpx
from app.core.config import get_settings

# single shared async client for the whole app
_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        settings = get_settings()
        _client = httpx.AsyncClient(
            base_url=settings.weather_base_url,
            timeout=httpx.Timeout(10.0),
            trust_env=False,
        )
    return _client


async def close_http_client() -> None:
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
