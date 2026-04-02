import json
from langchain.tools import tool

from app.services.google_calendar_service import get_today_events_from_google_calendar
from app.services.weather_service import get_weather_data, summarize_weather


@tool
def get_today_events() -> str:
    """Return today's Google Calendar events as JSON."""
    events = get_today_events_from_google_calendar()
    return json.dumps(events, ensure_ascii=False)


@tool
def get_today_weather() -> str:
    """Return today's weather summary and raw weather values as JSON."""
    weather = get_weather_data()
    summary = summarize_weather(weather)

    result = {
        "summary": summary,
        "details": weather,
    }
    return json.dumps(result, ensure_ascii=False)
