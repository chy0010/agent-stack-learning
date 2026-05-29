from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = []
messages.append(
    {
        "role": "system",
        "content": """
You are a senior FAANG interviewer.

Ask technical questions one at a time.

Do not explain answers immediately.

Challenge weak answers.

Be professional but tough.
"""
    }
)

while True:
    question = input("You: ")
    if question.lower() == "quit":
        break
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    ai_reply = response.choices[0].message.content
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )
    print("AI:", ai_reply)


# CHAT MEMORY FLOW
#
# User speaks
# ↓
# save user message into messages list
# ↓
# send FULL conversation history to GPT
# ↓
# GPT generates answer
# ↓
# extract GPT answer
# ↓
# save GPT answer back into messages list
# ↓
# print answer
# ↓
# repeat