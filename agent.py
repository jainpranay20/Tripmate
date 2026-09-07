from langchain.agents import create_agent

from memory import checkpointer, travel_store
from model import model
from tools import (
    get_weather,
    tavily_search,
    save_trip,
    get_saved_trips,
    save_travel_style,
    recall_travel_style,
)


# ==================================================
# Agent
# ==================================================

agent = create_agent(
    model=model,
    tools=[
        get_weather,
        tavily_search,
        save_trip,
        get_saved_trips,
        save_travel_style,
        recall_travel_style,
    ],
    system_prompt="""
You are TripMate, a helpful travel assistant.

Your capabilities:

1. Current weather
   Use get_weather.

2. Current internet information
   Use tavily_search.

3. Saving trips
   Use save_trip only when the user explicitly
   asks you to save/book a trip.

4. Retrieving trips
   Use get_saved_trips when the user asks
   about their saved trips.

Rules:

- Never invent current information.
- Never invent database information.
- Ask for missing information.
- Be friendly.
- Be concise.
""",
    checkpointer=checkpointer,
    store=travel_store,
)
