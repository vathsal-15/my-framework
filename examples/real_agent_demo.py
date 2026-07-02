from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()  # reads GROQ_API_KEY from your .env file

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What is 2 + 2? Answer in one short sentence."}
    ]
)

print(response.choices[0].message.content)