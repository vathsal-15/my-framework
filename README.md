![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

# my-framework

A multi-agent AI framework with built-in time-travel debugging — rewind, fork, diff, and replay any agent conversation.

Inspired by [AutoGen](https://github.com/microsoft/autogen), but with one core difference: every agent conversation is recorded as an event log, so you can go back to any point, branch off, compare what happened differently, and deterministically replay a run — like Git, but for AI agent conversations.

## Why?

When multiple AI agents talk to each other, debugging is hard. If something goes wrong three steps in, you usually have to start the whole run over and hope you can reproduce the issue. This framework lets you rewind to the exact moment things went wrong, branch from there, directly compare the two outcomes, and replay a run deterministically to verify a fix actually worked.

## Features

- **Event-sourced sessions** — every agent message is a recorded, linked event
- **`fork_at()`** — rewind to any point in a conversation and branch it
- **`diff()`** — compare two conversation branches and see exactly where they diverged
- **`replay()`** — deterministically re-run a session using cached responses
- **Multi-agent pipelines** — chain agents together (e.g., researcher → writer → reviewer)
- **Real AI agents** — powered by Groq's fast inference API
- **Tool-calling** — agents can invoke external functions (calculator, datetime, and easily extensible to more)

## Installation

```bash
pip install -r requirements.txt
```

You'll need a free Groq API key from [console.groq.com](https://console.groq.com). Create a `.env` file in the project root:
```
GROQ_API_KEY=your-key-here
```

## Quickstart

```python
from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()
questioner = Agent(name="questioner", system_prompt="You ask short trivia questions.")
answerer = Agent(name="answerer", system_prompt="You answer briefly.")

q_event = questioner.generate("Ask a one-sentence trivia question.", session)
a_event = answerer.generate(q_event.content, session)

# Rewind to right after the question, before the answer
forked = session.fork_at(q_event.id)
a_event_2 = answerer.generate(q_event.content, forked)

# See exactly how the two branches differed
diff_result = session.diff(forked)
for entry in diff_result:
    print(entry)

# Deterministically replay the original run
replayed = session.replay({"questioner": questioner, "answerer": answerer})
```

## Examples

See the `examples/` folder for runnable demos:
- `basic_event.py`, `basic_session.py` — core data model basics
- `fork_demo.py`, `diff_demo.py` — rewind and compare conversations
- `replay_demo.py` — deterministic replay with caching
- `real_agent_demo.py`, `real_session_demo.py` — real AI agents logging to a session
- `three_agent_pipeline.py` — a researcher → writer → reviewer pipeline
- `pipeline_fork_diff.py` — forking and diffing a multi-agent pipeline
- `tool_use_demo.py`, `multi_tool_demo.py` — agents using external tools like a calculator and datetime

## Status

Core primitives (`Event`, `Session`, `fork_at`, `diff`, `replay`) are implemented and tested with live AI agents across both simple 2-agent conversations and multi-agent pipelines. Basic tool-calling is now supported. Next up: full MCP protocol support for connecting to real external MCP servers.

## License

MIT