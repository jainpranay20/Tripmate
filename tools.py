import requests

from langchain.tools import tool
from langchain_tavily import TavilySearch
from database import create_trip, get_trips
from database import setup_database
setup_database()


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

@tool
def save_trip(
    user_id: str,
    destination: str,
    start_date: str,
    end_date: str,
) -> str:
    """Save a confirmed trip to the database."""

    trip_id = create_trip(
        user_id=user_id,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
    )

    return (
        f"Trip #{trip_id} saved successfully. "
        f"Destination: {destination}. "
        f"Dates: {start_date} to {end_date}."
    )

@tool
def get_saved_trips(user_id: str) -> str:
    """Retrieve all saved trips for a user."""

    trips = get_trips(user_id)

    if not trips:
        return "No saved trips found."

    results = []

    for trip in trips:

        trip_id = trip[0]
        destination = trip[1]
        start_date = trip[2]
        end_date = trip[3]
        status = trip[4]

        results.append(
            f"Trip #{trip_id}: "
            f"{destination}, "
            f"{start_date} to {end_date}, "
            f"status={status}"
        )

    return "\n".join(results)


tavily_search = TavilySearch(
    max_results=5,
    topic="general",
)
