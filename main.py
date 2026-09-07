import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import get_weather


load_dotenv()


# -----------------------------------------
# OpenRouter model
# -----------------------------------------

model = ChatOpenAI(
    model="openai/gpt-5-mini",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    max_tokens=1024,
)



# -----------------------------------------
# Create agent
# -----------------------------------------

agent = create_agent(
    model=model,
    tools=[
        get_weather,
    ],
    system_prompt="""
    You are TripMate, a helpful travel assistant.

    When the user asks for current weather,
    always use the get_weather tool.

    Never guess current weather.

    Be friendly and concise.
""",
)


# -----------------------------------------
# Ask the agent
# -----------------------------------------

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What's the weather in Bengaluru right now?"
        }
    ]
})


print(result["messages"][-1].content)
