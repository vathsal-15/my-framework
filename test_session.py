from packages.core.core.events import Event
from packages.core.core.session import Session
from datetime import datetime
import uuid

session = Session()

# Agent A sends a message
e1 = Event(
    id=str(uuid.uuid4()),
    parent_id=session.last_event_id(),
    timestamp=datetime.now(),
    agent_name="agent_a",
    content="What is 2 + 2?",
    event_type="message"
)
session.append(e1)

# Agent B replies, linked to Agent A's message
e2 = Event(
    id=str(uuid.uuid4()),
    parent_id=session.last_event_id(),
    timestamp=datetime.now(),
    agent_name="agent_b",
    content="2 + 2 = 4",
    event_type="message"
)
session.append(e2)

# Print the full conversation history
for event in session.history():
    print(f"[{event.agent_name}] {event.content}  (parent: {event.parent_id})")