import json
from pathlib import Path


def load_today_events() -> list[dict]:
    file_path = Path("data/calendar.json")

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
