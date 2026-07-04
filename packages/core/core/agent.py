from groq import Groq
from datetime import datetime
import os
import uuid
import hashlib
import re

from packages.core.core.events import Event
from packages.core.core.session import Session

_response_cache: dict[str, str] = {}

class Agent:
    def __init__(self, name: str, system_prompt: str = "", tools: list = None):
        self.name = name
        self.tools = tools or []
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        tool_instructions = ""
        if self.tools:
            tool_list = "\n".join(f"- {t.name}: {t.description}" for t in self.tools)
            tool_instructions = (
                f"\n\nYou have access to these tools:\n{tool_list}\n"
                f"To use a tool, respond ONLY with: TOOL_CALL: <tool_name>(<argument>)\n"
                f"For example: TOOL_CALL: calculator(2 + 2)"
            )
        self.system_prompt = system_prompt + tool_instructions

    def _cache_key(self, user_message: str) -> str:
        raw = f"{self.name}|{self.system_prompt}|{user_message}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _try_tool_call(self, content: str) -> str | None:
        match = re.match(r"TOOL_CALL:\s*(\w+)\((.*)\)", content.strip())
        if not match:
            return None
        tool_name, arg = match.group(1), match.group(2)
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.run(expression=arg)
        return None

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

        tool_result = self._try_tool_call(content)
        event_type = "message"
        if tool_result is not None:
            content = f"{content}\n[Tool result: {tool_result}]"
            event_type = "tool_call"

        event = Event(
            id=str(uuid.uuid4()),
            parent_id=session.last_event_id(),
            timestamp=datetime.now(),
            agent_name=self.name,
            content=content,
            event_type=event_type,
            prompt=user_message
        )
        session.append(event)
        return event