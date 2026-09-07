import os

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

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
    max_tokens=1024,
)


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

        You can:

        - Check current weather.
        - Search the web.
        - Save trips.
        - Retrieve saved trips.

        Rules:

        1. Use the weather tool for current weather.
        2. Use web search for current internet information.
        3. Only save a trip when the user explicitly asks you to save it.
        4. Never invent database information.
        5. Ask for missing information when necessary.
        6. Be friendly and concise.
        """,
)


result = agent.invoke(
    {
        "messages": [
            (
                "user",
                """
                My user ID is rohan_01.

                Save my trip to Bali from
                2026-10-10 to 2026-10-15.
                """
            )
        ]
    }
)

print(result["messages"][-1].content)
