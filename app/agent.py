from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.config import settings
from app.tools import get_today_events, get_today_weather


class EventItemOutput(BaseModel):
    title: str
    time: str
    location: str
    is_outdoor: bool


class DailyAssistantOutput(BaseModel):
    date: str
    weather_summary: str
    events: list[EventItemOutput]
    outfit_advice: list[str]
    schedule_advice: list[str]
    warnings: list[str]


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.openai_api_key,
    temperature=0.2,
)

parser = PydanticOutputParser(pydantic_object=DailyAssistantOutput)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Weather + Calendar Assistant.

You must:
1. Use the calendar tool
2. Use the weather tool
3. Decide what the user is doing today
4. Suggest what to wear
5. Warn the user if outdoor plans may be affected
6. Suggest rescheduling only if weather makes outdoor activities uncomfortable or risky

Important rules:
- Be practical
- Be specific
- Do not invent events
- If an event is outdoors and rain chance is high, mention it in warnings or schedule_advice
- If temperature is low, suggest layers or a jacket
- If weather is fine, say outdoor plans look okay

Return ONLY valid structured output in this format:
{format_instructions}
            """.strip(),
        ),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [get_today_events, get_today_weather]

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
