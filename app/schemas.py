from pydantic import BaseModel, Field


class AssistantQuery(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=300,
        description="What the user wants the assistant to do",
        examples=["What am I doing today? What should I wear?"],
    )


class EventItem(BaseModel):
    title: str
    time: str
    location: str
    is_outdoor: bool


class DailyAssistantResponse(BaseModel):
    date: str
    weather_summary: str
    events: list[EventItem]
    outfit_advice: list[str]
    schedule_advice: list[str]
    warnings: list[str]