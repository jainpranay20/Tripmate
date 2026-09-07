import requests

from langchain.tools import tool
from langchain_tavily import TavilySearch


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return f"Could not find the city '{city}'."

    location = geo_data["results"][0]

    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    current = weather_data["current"]

    return (
        f"Current weather in {location['name']}: "
        f"{current['temperature_2m']}°C, "
        f"wind speed {current['wind_speed_10m']} km/h."
    )


tavily_search = TavilySearch(
    max_results=5,
    topic="general",
)
