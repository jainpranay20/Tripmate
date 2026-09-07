import os

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from tools import (
    get_weather,
    tavily_search,
    save_trip,
    get_saved_trips,
)

model = ChatOpenAI(
    model="openai/gpt-5-mini",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    max_tokens=512,
)


# ==================================================
# Conversation memory
# ==================================================

checkpointer = InMemorySaver()


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
- Be friendly.
- Be concise.
""",
    checkpointer=checkpointer,
)
