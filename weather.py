import httpx

import config

WEATHERBIT_BASE = "https://api.weatherbit.io/v2.0/current"


async def get_weather(city: str) -> tuple[dict | None, str | None]:
    """
    Fetch current weather from Weatherbit API.

    Returns (data, None) on success or (None, error_message) on failure.
    Never raises — all errors are surfaced as the second tuple element.
    """
    params = {
        "city": city,
        "key": config.WEATHERBIT_API_KEY,
        "units": "M",
        "lang": "en",
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(WEATHERBIT_BASE, params=params, timeout=10)

        if r.status_code == 204 or (r.status_code == 200 and r.json().get("count", 0) == 0):
            return None, f'City "{city}" not found. Check the spelling and try again.'
        if r.status_code == 403:
            return None, "Invalid API key. Check WEATHERBIT_API_KEY in your .env file."
        if r.status_code == 429:
            return None, "Weatherbit rate limit reached. Try again in a minute."

        r.raise_for_status()

        data_list = r.json().get("data", [])
        if not data_list:
            return None, f'City "{city}" not found. Check the spelling and try again.'

        return data_list[0], None

    except httpx.HTTPStatusError as e:
        return None, f"Weather service returned error {e.response.status_code}. Try again later."
    except httpx.TimeoutException:
        return None, "Request timed out. The weather service is slow — try again in a moment."
    except httpx.RequestError:
        return None, "Could not reach the weather service. Check your internet connection."


def format_weather(data: dict) -> str:
    """Format a raw Weatherbit response dict into a human-readable string."""
    city = data.get("city_name", "Unknown")
    country = data.get("country_code", "")
    temp = data.get("temp", 0)
    feels = data.get("app_temp", 0)
    humidity = data.get("rh", 0)
    description = data.get("weather", {}).get("description", "").capitalize()
    wind_speed = data.get("wind_spd", 0)
    visibility_km = data.get("vis", 0)
    pressure_mb = data.get("pres", 0)

    return (
        f"Weather in {city}, {country}\n"
        f"{description}\n"
        f"Пора идти домой, работа подождет!\n\n"
        f"Temperature: {temp:.1f}°C (feels like {feels:.1f}°C)\n"
        f"Humidity:    {humidity}%\n"
        f"Wind:        {wind_speed:.1f} m/s\n"
        f"Pressure:    {pressure_mb:.0f} hPa\n"
        f"Visibility:  {visibility_km:.1f} km"
    )
