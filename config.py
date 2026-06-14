import os


def sanitize_url(url: str) -> str:
    """Strip non-printable ASCII characters (ord < 32 or ord > 126) from a URL string."""
    return ''.join(c for c in url if 32 <= ord(c) <= 126)


BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
WEATHERBIT_API_KEY: str = os.getenv("WEATHERBIT_API_KEY", "")
WEBHOOK_URL: str = sanitize_url(os.getenv("WEBHOOK_URL", ""))
PORT: int = int(os.getenv("PORT", "8443"))
TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Moscow")
BEER_HOUR: int = int(os.getenv("BEER_HOUR", "16"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Copy .env.example to .env and fill in your token.")
if not WEATHERBIT_API_KEY:
    raise RuntimeError("WEATHERBIT_API_KEY is not set. Copy .env.example to .env and fill in your Weatherbit API key.")
