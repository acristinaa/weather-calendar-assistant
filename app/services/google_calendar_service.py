from __future__ import annotations

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TOKEN_PATH = Path("token.json")
CREDENTIALS_PATH = Path("credentials.json")


def get_google_calendar_credentials() -> Credentials:
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    "credentials.json not found. Download your OAuth client file from Google Cloud Console."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH),
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    return creds


def get_calendar_service():
    creds = get_google_calendar_credentials()
    return build("calendar", "v3", credentials=creds)


def get_today_events_from_google_calendar(
    timezone_str: str = "Europe/Berlin",
    calendar_id: str = "primary",
) -> list[dict]:
    service = get_calendar_service()

    tz = ZoneInfo(timezone_str)
    now = datetime.now(tz)

    start_of_day = datetime.combine(now.date(), time.min, tzinfo=tz)
    end_of_day = start_of_day + timedelta(days=1)

    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    parsed_events = []

    for event in events:
        start = event.get("start", {})
        location = event.get("location", "No location")

        start_value = start.get("dateTime") or start.get("date") or "Unknown"
        title = event.get("summary", "Untitled event")

        is_outdoor = infer_is_outdoor(title=title, location=location)

        parsed_events.append(
            {
                "title": title,
                "time": format_event_time(start_value, timezone_str),
                "location": location,
                "is_outdoor": is_outdoor,
            }
        )

    return parsed_events


def format_event_time(start_value: str, timezone_str: str) -> str:
    try:
        if "T" in start_value:
            dt = datetime.fromisoformat(start_value.replace("Z", "+00:00"))
            return dt.astimezone(ZoneInfo(timezone_str)).strftime("%H:%M")
        return "All day"
    except Exception:
        return start_value


def infer_is_outdoor(title: str, location: str) -> bool:
    outdoor_keywords = [
        "park",
        "walk",
        "run",
        "picnic",
        "outdoor",
        "terrace",
        "beach",
        "hike",
        "football",
        "garden",
    ]

    text = f"{title} {location}".lower()
    return any(keyword in text for keyword in outdoor_keywords)
