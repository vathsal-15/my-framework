from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    id: str
    parent_id: str | None
    timestamp: datetime
    agent_name: str
    content: str
    event_type: str  # "message" or "tool_call"