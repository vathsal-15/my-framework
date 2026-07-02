from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()

math_agent = Agent(name="math_agent", system_prompt="You are a math expert. Answer briefly.")

event = math_agent.generate("What is the square root of 144?", session)

print("--- Session history ---")
for e in session.history():
    print(f"[{e.agent_name}] {e.content}")