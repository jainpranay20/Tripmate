import requests

from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    # ------------------------------------------------
    # 1. Convert city name -> latitude/longitude
    # ------------------------------------------------

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

    latitude = location["latitude"]
    longitude = location["longitude"]

    # ------------------------------------------------
    # 2. Get current weather
    # ------------------------------------------------

    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    current = weather_data["current"]

    temperature = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]

    return (
        f"Current weather in {location['name']}: "
        f"{temperature}°C, "
        f"wind speed {wind_speed} km/h."
    )
if __name__ == "__main__":
    print(
        get_weather.invoke(
            {"city": "Bengaluru"}
        )
    )
