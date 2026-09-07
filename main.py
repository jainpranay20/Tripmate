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

        response = result["messages"][-1].content

        print(f"\nTripMate: {response}\n")


if __name__ == "__main__":
    main()
