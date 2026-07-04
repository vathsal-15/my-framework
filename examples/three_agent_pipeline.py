from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

session = Session()

researcher = Agent(
    name="researcher",
    system_prompt="You research a topic and give 2-3 short factual bullet points."
)
writer = Agent(
    name="writer",
    system_prompt="You write a short, engaging paragraph based on research notes given to you."
)
reviewer = Agent(
    name="reviewer",
    system_prompt="You review a paragraph and give one specific piece of feedback to improve it."
)

topic = "Ask for research notes on why octopuses are considered intelligent."

# Step 1: Researcher gathers notes
research_event = researcher.generate(topic, session)

# Step 2: Writer turns notes into a paragraph
writing_event = writer.generate(research_event.content, session)

# Step 3: Reviewer critiques the paragraph
review_event = reviewer.generate(writing_event.content, session)

print("--- Full pipeline ---")
for e in session.history():
    print(f"\n[{e.agent_name}]\n{e.content}")