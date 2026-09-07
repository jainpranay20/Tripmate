# ---------------------------------------------------------
# main.py
#
# FIRST OPENROUTER TEST
#
# Goal:
#
# Python
#   ↓
# .env
#   ↓
# OpenRouter
#   ↓
# GPT-5 mini
#   ↓
# Response
#
# We are NOT creating an agent yet.
# We are only checking that our OpenRouter connection works.
# ---------------------------------------------------------


# ---------------------------------------------------------
# 1. Import Python libraries
# ---------------------------------------------------------

# os allows Python to read environment variables.
import os

# load_dotenv() loads values from our .env file.
from dotenv import load_dotenv

# ChatOpenAI is LangChain's OpenAI-compatible chat model.
# Even though the class is called ChatOpenAI, we are going
# to configure it to send requests to OpenRouter.
from langchain_openai import ChatOpenAI


# ---------------------------------------------------------
# 2. Load environment variables
# ---------------------------------------------------------

# This reads the .env file.
#
# For example:
#
# OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx
#
# After this, Python can access the key using:
#
# os.environ["OPENROUTER_API_KEY"]
#
load_dotenv()


# ---------------------------------------------------------
# 3. Create our LLM
# ---------------------------------------------------------

model = ChatOpenAI(

    # The model we are asking OpenRouter to use.
    model="openai/gpt-5-mini",

    # Get the API key from our .env file.
    api_key=os.environ["OPENROUTER_API_KEY"],

    # IMPORTANT:
    # Normally ChatOpenAI would communicate with OpenAI.
    #
    # By changing base_url, we tell it:
    #
    # "Send this request to OpenRouter."
    base_url="https://openrouter.ai/api/v1",

    # IMPORTANT:
    # Limit the maximum number of tokens the model can generate.
    #
    # We only need a small response for this test.
    #
    # This prevents OpenRouter from trying to reserve
    # a very large token budget.
    max_tokens=1024,
)


# ---------------------------------------------------------
# 4. Send a test message
# ---------------------------------------------------------

response = model.invoke(
    "Explain what an AI agent is in three simple sentences."
)


# ---------------------------------------------------------
# 5. Print the response
# ---------------------------------------------------------

print(response.content)
