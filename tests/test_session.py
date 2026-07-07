from datetime import datetime
import uuid

from packages.core.core.events import Event
from packages.core.core.session import Session


def make_event(agent_name: str, content: str, parent_id: str = None, prompt: str = None) -> Event:
    return Event(
        id=str(uuid.uuid4()),
        parent_id=parent_id,
        timestamp=datetime.now(),
        agent_name=agent_name,
        content=content,
        event_type="message",
        prompt=prompt
    )


def test_append_and_history():
    session = Session()
    e1 = make_event("agent_a", "Hello")
    session.append(e1)
    assert session.history() == [e1]


def test_last_event_id_empty():
    session = Session()
    assert session.last_event_id() is None


def test_last_event_id_after_append():
    session = Session()
    e1 = make_event("agent_a", "Hello")
    session.append(e1)
    assert session.last_event_id() == e1.id


def test_fork_at_creates_independent_branch():
    session = Session()
    e1 = make_event("agent_a", "Question", parent_id=session.last_event_id())
    session.append(e1)
    e2 = make_event("agent_b", "Answer A", parent_id=session.last_event_id())
    session.append(e2)

    forked = session.fork_at(e1.id)

    # Forked session should only contain e1, not e2
    assert forked.history() == [e1]
    # Original session should be untouched
    assert session.history() == [e1, e2]


def test_diff_detects_same_and_diverged():
    session_a = Session()
    e1 = make_event("agent_a", "Question")
    session_a.append(e1)
    e2 = make_event("agent_b", "Answer A", parent_id=e1.id)
    session_a.append(e2)

    session_b = Session()
    session_b.append(e1)
    e3 = make_event("agent_b", "Answer B", parent_id=e1.id)
    session_b.append(e3)

    diff_result = session_a.diff(session_b)

    assert diff_result[0]["status"] == "same"
    assert diff_result[1]["status"] == "diverged"