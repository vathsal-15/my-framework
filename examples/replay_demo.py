from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()
answerer = Agent(name="answerer", system_prompt="You answer briefly.")

e1 = answerer.generate("What is the capital of France?", session)
print("--- Original run ---")
print(f"[{e1.agent_name}] {e1.content}")

# Replay the session using the same agent
replayed = session.replay({"answerer": answerer})
print("\n--- Replayed run ---")
for e in replayed.history():
    print(f"[{e.agent_name}] {e.content}")

print("\n--- Identical? ---")
print(session.history()[0].content == replayed.history()[0].content)