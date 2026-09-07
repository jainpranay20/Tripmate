import uuid

from database import setup_database
from agent import agent


def main():

    # Create database tables
    setup_database()

    # One conversation/thread
    config = {
        "configurable": {
            "thread_id": f"user-session-{uuid.uuid4()}"
        }
    }

    print("🌍 TripMate")
    print("Your AI travel assistant.")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in {
            "exit",
            "quit",
        }:
            print("Goodbye!")
            break

        result = agent.invoke(
            {
                "messages": [
                    ("user", user_input)
                ]
            },
            config=config,
        )

        structured = result.get("structured_response")

        if structured is not None:
            print(f"\nTripMate: {structured.assistant_message}\n")
            print(f"Request details: {structured.model_dump(exclude_none=True)}\n")
        else:
            print(f"\nTripMate: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()
