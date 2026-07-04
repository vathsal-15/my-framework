from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent
from packages.core.core.tools import calculator_tool

session = Session()

math_agent = Agent(
    name="math_agent",
    system_prompt="You are a math assistant. Use the calculator tool for any arithmetic instead of computing it yourself.",
    tools=[calculator_tool]
)

event = math_agent.generate("What is 347 * 29?", session)

print("--- Tool use demo ---")
print(f"[{event.agent_name}] {event.content}")
print(f"Event type: {event.event_type}")