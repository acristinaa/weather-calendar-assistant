import requests
from app.config import settings


def get_weather_data() -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={settings.latitude}"
        f"&longitude={settings.longitude}"
        "&current=temperature_2m,weather_code,wind_speed_10m"
        "&hourly=temperature_2m,precipitation_probability,weather_code"
        "&forecast_days=1"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    hourly = data.get("hourly", {})

    precipitation_probs = hourly.get("precipitation_probability", [])
    max_precipitation = max(precipitation_probs) if precipitation_probs else 0

    return {
        "temperature": current.get("temperature_2m"),
        "weather_code": current.get("weather_code"),
        "wind_speed": current.get("wind_speed_10m"),
        "max_precipitation_probability": max_precipitation,
    }


def weather_code_to_text(code: int | None) -> str:
    if code is None:
        return "Unknown weather"

    mapping = {
        0: "Clear sky",
        1: "Mostly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Snow",
        80: "Rain showers",
        95: "Thunderstorm",
    }

    return mapping.get(code, "Unrecognized weather")


def summarize_weather(weather: dict) -> str:
    condition = weather_code_to_text(weather.get("weather_code"))
    temp = weather.get("temperature")
    wind = weather.get("wind_speed")
    rain_prob = weather.get("max_precipitation_probability")

    return (
        f"{condition}. Temperature around {temp}°C, "
        f"wind {wind} km/h, "
        f"max rain chance today {rain_prob}%."
    )