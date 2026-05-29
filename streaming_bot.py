from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = []
messages.append(
    {
    "role": "system",
    "content": "You are helpful"
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
    
    print("AI: ", end="", flush=True)                   # Print AI label before response starts streamingn ,end="" keeps cursor on same line , flush=True shows output immediately

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True                                     # Enable live streaming instead of waiting for full response
    )

    ai_reply = ""                                        # Create empty string to collect AI response chunks

    for chunk in response:                                # Loop through each incoming streamed chunk from OpenAI
        content = chunk.choices[0].delta.content

        if content:                                       # Some chunks may be empty, so only process real text
            print(content, end="", flush=True)            # Print chunk immediately for typing effect
            ai_reply += content                           # Add current chunk to full AI response

    print()

    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )