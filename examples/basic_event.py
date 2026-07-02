from packages.core.core.events import Event
from datetime import datetime
import uuid

e1 = Event(
    id=str(uuid.uuid4()),
    parent_id=None,
    timestamp=datetime.now(),
    agent_name="agent_a",
    content="Hello from agent A",
    event_type="message"
)

print(e1)