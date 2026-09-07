import os

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import (
    get_weather,
    tavily_search,
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
    ],
    system_prompt="""
You are TripMate, a helpful travel assistant.

Available tools:

1. get_weather
   Use for current weather.

2. tavily_search
   Use for current information from the internet.

Never invent current information when a tool
can provide it.

Be friendly and concise.
""",
)


result = agent.invoke(
    {
        "messages": [
            (
                "user",
                """
                I'm planning a trip to Bali.

                What's the current weather there?
                Also tell me three interesting things
                I can do there.
                """
            )
        ]
    }
)


print(result["messages"][-1].content)
