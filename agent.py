from openai import OpenAI
from dotenv import load_dotenv
import os

# Step 1: load API key from .env
load_dotenv()

# Step 2: connect to OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 3: ask user for input
question = input("Ask me anything: ")

# Step 4: send question to AI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": question}
    ]
)

# Step 5: print answer
print("\nAI says:")
print(response.choices[0].message.content)