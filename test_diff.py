from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()

questioner = Agent(name="questioner", system_prompt="You ask short trivia questions.")
answerer = Agent(name="answerer", system_prompt="You answer briefly and confidently.")

q_event = questioner.generate("Ask an open-ended opinion question about the best programming language.", session)
a_event = answerer.generate(q_event.content, session)

forked = session.fork_at(q_event.id)
a_event_2 = answerer.generate(q_event.content, forked)

# Compare the two conversations
diff_result = session.diff(forked)

print("--- Diff between original and forked session ---")
for entry in diff_result:
    if entry["status"] == "same":
        print(f"[{entry['index']}] SAME: {entry['content']}")
    else:
        print(f"[{entry['index']}] DIVERGED:")
        print(f"    Session A: {entry['session_a']}")
        print(f"    Session B: {entry['session_b']}")