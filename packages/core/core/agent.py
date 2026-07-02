from groq import Groq
from datetime import datetime
import os
import uuid
import hashlib

from packages.core.core.events import Event
from packages.core.core.session import Session

_response_cache: dict[str, str] = {}

class Agent:
    def __init__(self, name: str, system_prompt: str = ""):
        self.name = name
        self.system_prompt = system_prompt
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def _cache_key(self, user_message: str) -> str:
        raw = f"{self.name}|{self.system_prompt}|{user_message}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate(self, user_message: str, session: Session, use_cache: bool = True) -> Event:
        cache_key = self._cache_key(user_message)

        if use_cache and cache_key in _response_cache:
            content = _response_cache[cache_key]
        else:
            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})
            messages.append({"role": "user", "content": user_message})

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            content = response.choices[0].message.content
            _response_cache[cache_key] = content

        event = Event(
            id=str(uuid.uuid4()),
            parent_id=session.last_event_id(),
            timestamp=datetime.now(),
            agent_name=self.name,
            content=content,
            event_type="message",
            prompt=user_message
        )
        session.append(event)
        return event