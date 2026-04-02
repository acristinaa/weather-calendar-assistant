# Weather + Calendar Assistant

My second AI agent project, built with FastAPI and LangChain.

This assistant checks what I'm doing today, looks at the weather, and gives practical suggestions like what to wear or whether outdoor plans should be rescheduled.

---

## What it does

- Reads today's events from a local calendar JSON file
- Fetches real-time weather data from an API
- Detects indoor vs outdoor activities
- Suggests what to wear based on conditions
- Warns about weather risks (rain, cold, etc.)
- Returns a structured JSON response

---

## Tech stack

- Python
- FastAPI
- LangChain (`langchain_classic`)
- OpenAI (`gpt-4o-mini`)
- Pydantic
- Requests
- Open-Meteo API

---

## Project structure

```
weather-calendar-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── config.py
│   ├── schemas.py
│   ├── tools.py
│   └── services/
│       ├── __init__.py
│       ├── calendar_service.py
│       └── weather_service.py
│
├── data/
│   └── calendar.json
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd weather-calendar-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
LATITUDE=52.52
LONGITUDE=13.41
```

---

## Run the project

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

## How to test

1. Open your browser and go to: `http://127.0.0.1:8000/docs`
2. Find the endpoint: **POST** `/assistant/today`
3. Click **Try it out**
4. Paste this request:

```json
{
  "query": "What am I doing today? What should I wear? Should I reschedule outdoor plans?"
}
```

5. Click **Execute**

---

## Example response

```json
{
  "date": "2026-04-02",
  "weather_summary": "Partly cloudy, 11°C, possible rain later",
  "events": [
    {
      "title": "Morning walk",
      "time": "08:30",
      "location": "Park",
      "is_outdoor": true
    }
  ],
  "outfit_advice": ["Wear a light jacket or layers"],
  "schedule_advice": ["Consider moving outdoor plans indoors if rain starts"],
  "warnings": ["Rain may affect outdoor activities"]
}
```

---

## Notes

- Weather data is fetched from the Open-Meteo API
- Calendar data is fetched from Google Calendar using the Google Calendar API
- Google Calendar authentication currently uses a local desktop OAuth flow for development
- This setup is intended for local testing and can be upgraded later for production deployment

---

## Future improvements

- Integrate Google Calendar API
- Match weather conditions to specific event times
- Add user preferences (e.g., transport, clothing style)
- Suggest commute adjustments
- Build a frontend interface
- Deploy the API online

---

## What I learned

- How to build a tool-using AI agent
- Connecting LLMs to real-world APIs
- Structuring a backend project with FastAPI
- Using Pydantic for clean, reliable outputs
- Designing systems that combine data + reasoning

---

## Author

**Cristina**  
Computer Science student & aspiring AI engineer
