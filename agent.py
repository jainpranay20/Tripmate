from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from memory import checkpointer
from model import model
from schemas import TripRequest
from tools import (
    get_weather,
    tavily_search,
    save_trip,
    get_saved_trips,
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
- Always provide a concise assistant_message for the user.
- Be friendly.
- Be concise.
""",
    response_format=ToolStrategy(TripRequest),
    checkpointer=checkpointer,
)
