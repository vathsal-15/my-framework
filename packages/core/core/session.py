from packages.core.core.events import Event

class Session:
    def __init__(self):
        self._events: list[Event] = []

    def append(self, event: Event) -> None:
        self._events.append(event)

    def history(self) -> list[Event]:
        return self._events

    def last_event_id(self) -> str | None:
        if not self._events:
            return None
        return self._events[-1].id

    def fork_at(self, event_id: str) -> "Session":
        """Create a new Session containing only events up to and including event_id."""
        new_session = Session()
        for event in self._events:
            new_session.append(event)
            if event.id == event_id:
                break
        return new_session
    
    def diff(self, other: "Session") -> list[dict]:
        """Compare this session with another and show where they diverge."""
        results = []
        max_len = max(len(self._events), len(other._events))

        for i in range(max_len):
            e1 = self._events[i] if i < len(self._events) else None
            e2 = other._events[i] if i < len(other._events) else None

            if e1 and e2 and e1.content == e2.content and e1.agent_name == e2.agent_name:
                results.append({"index": i, "status": "same", "content": e1.content})
            else:
                results.append({
                    "index": i,
                    "status": "diverged",
                    "session_a": f"[{e1.agent_name}] {e1.content}" if e1 else None,
                    "session_b": f"[{e2.agent_name}] {e2.content}" if e2 else None,
                })

        return results    

    def replay(self, agents: dict) -> "Session":
        """Re-run this session's events using cached responses for identical results."""
        new_session = Session()
        for event in self._events:
            agent = agents.get(event.agent_name)
            if agent:
                agent.generate(event.prompt if event.prompt else "", new_session)
            else:
                new_session.append(event)
        return new_session    