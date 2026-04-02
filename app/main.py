from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agent import agent_executor, parser
from app.schemas import AssistantQuery, DailyAssistantResponse

app = FastAPI(
    title="Weather + Calendar Assistant",
    version="1.0.0",
    description="An assistant that checks today's events, weather, and gives outfit/schedule advice.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Weather + Calendar Assistant is running"}


@app.post("/assistant/today", response_model=DailyAssistantResponse)
async def assistant_today(body: AssistantQuery):
    try:
        raw_response = agent_executor.invoke({"query": body.query})
        output = raw_response.get("output")

        if output is None:
            raise ValueError("Agent returned no output.")

        if not isinstance(output, str):
            raise ValueError(f"Unexpected output type: {type(output)}")

        structured_response = parser.parse(output)
        return structured_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant failed: {str(e)}")
