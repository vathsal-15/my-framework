from packages.core.core.events import Event
from packages.core.core.session import Session
from datetime import datetime
import uuid

session = Session()

# Agent A asks a question
e1 = Event(
    id=str(uuid.uuid4()),
    parent_id=session.last_event_id(),
    timestamp=datetime.now(),
    agent_name="agent_a",
    content="What is 2 + 2?",
    event_type="message"
)
session.append(e1)

# Agent B gives a WRONG answer
e2 = Event(
    id=str(uuid.uuid4()),
    parent_id=session.last_event_id(),
    timestamp=datetime.now(),
    agent_name="agent_b",
    content="2 + 2 = 5",
    event_type="message"
)
session.append(e2)

print("--- Original session ---")
for event in session.history():
    print(f"[{event.agent_name}] {event.content}")

# Fork back to right after Agent A's question (before the wrong answer)
forked = session.fork_at(e1.id)

# Now Agent B gives a CORRECT answer in the forked branch
e3 = Event(
    id=str(uuid.uuid4()),
    parent_id=forked.last_event_id(),
    timestamp=datetime.now(),
    agent_name="agent_b",
    content="2 + 2 = 4",
    event_type="message"
)
forked.append(e3)

print("\n--- Forked session ---")
for event in forked.history():
    print(f"[{event.agent_name}] {event.content}")