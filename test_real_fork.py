from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()

questioner = Agent(name="questioner", system_prompt="You ask short trivia questions.")
answerer = Agent(name="answerer", system_prompt="You answer briefly and confidently.")

# Agent A asks a question
q_event = questioner.generate("Ask a one-sentence trivia question about space.", session)

# Agent B answers it
a_event = answerer.generate(q_event.content, session)

print("--- Original conversation ---")
for e in session.history():
    print(f"[{e.agent_name}] {e.content}")

# Fork right after the question, before the original answer
forked = session.fork_at(q_event.id)

# Get a second, different answer in the forked branch
a_event_2 = answerer.generate(q_event.content, forked)

print("\n--- Forked conversation (different answer attempt) ---")
for e in forked.history():
    print(f"[{e.agent_name}] {e.content}")