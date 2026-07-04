from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent
from packages.core.core.tools import calculator_tool, datetime_tool

session = Session()

assistant = Agent(
    name="assistant",
    system_prompt="You are a helpful assistant. Use tools when appropriate instead of guessing.",
    tools=[calculator_tool, datetime_tool]
)

e1 = assistant.generate("What is 89 * 12?", session)
print(f"[{e1.agent_name}] {e1.content}")

e2 = assistant.generate("What is the current date and time?", session)
print(f"\n[{e2.agent_name}] {e2.content}")