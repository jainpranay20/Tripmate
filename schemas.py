from typing import Literal

from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    """Structured representation of a user's travel request."""

    assistant_message: str = Field(
        description="A concise, friendly message to show the user. Ask for missing information when needed."
    )

    intent: Literal[
        "new_trip",
        "modify_trip",
        "cancel_trip",
        "view_trips",
        "weather",
        "search",
        "general",
    ] = Field(
        description="What the user wants to do."
    )

    user_id: str | None = Field(
        default=None,
        description="The user's ID if provided."
    )

    destination: str | None = Field(
        default=None,
        description="Trip destination."
    )

    start_date: str | None = Field(
        default=None,
        description="Trip start date in YYYY-MM-DD format."
    )

    end_date: str | None = Field(
        default=None,
        description="Trip end date in YYYY-MM-DD format."
    )

    trip_id: int | None = Field(
        default=None,
        description="Trip ID when modifying or cancelling a trip."
    )
