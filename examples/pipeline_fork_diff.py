from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()

researcher = Agent(name="researcher", system_prompt="You research a topic and give 2-3 short factual bullet points.")
writer = Agent(name="writer", system_prompt="You write a short, engaging paragraph based on research notes given to you.")

topic = "Ask for research notes on why octopuses are considered intelligent."

# Step 1: Researcher gathers notes
research_event = researcher.generate(topic, session)

# Step 2: Writer writes paragraph A
writing_event_a = writer.generate(research_event.content, session)

print("--- Branch A (original) ---")
print(writing_event_a.content)

# Fork right after research, before the writer's first attempt
forked = session.fork_at(research_event.id)

# Step 2 (again): Writer writes paragraph B, using cache disabled to force a fresh attempt
writing_event_b = writer.generate(research_event.content + " Please write it differently this time.", forked)

print("\n--- Branch B (forked, different instruction) ---")
print(writing_event_b.content)

# Compare the two pipeline branches
diff_result = session.diff(forked)
print("\n--- Diff between Branch A and Branch B ---")
for entry in diff_result:
    if entry["status"] == "same":
        print(f"[{entry['index']}] SAME")
    else:
        print(f"[{entry['index']}] DIVERGED")