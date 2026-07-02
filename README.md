# my-framework

A multi-agent AI framework with built-in time-travel debugging — rewind, fork, and diff any agent conversation.

Inspired by [AutoGen](https://github.com/microsoft/autogen), but with one core difference: every agent conversation is recorded as an event log, so you can go back to any point, branch off, and compare what happened differently — like Git, but for AI agent conversations.

## Why?

When multiple AI agents talk to each other, debugging is hard. If something goes wrong three steps in, you usually have to start the whole run over and hope you can reproduce the issue. This framework lets you rewind to the exact moment things went wrong, branch from there, and directly compare the two outcomes.

## Features

- **Event-sourced sessions** — every agent message is a recorded, linked event
- **`fork_at()`** — rewind to any point in a conversation and branch it
- **`diff()`** — compare two conversation branches and see exactly where they diverged
- **Real AI agents** — powered by Groq's fast inference API

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
```

## Status

Early prototype. Core primitives (`Event`, `Session`, `fork_at`, `diff`) are implemented and tested with live AI agents. Next up: `replay()` for deterministic re-execution.

## License

MIT