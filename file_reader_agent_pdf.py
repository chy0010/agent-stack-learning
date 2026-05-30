from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pypdf import PdfReader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

reader = PdfReader("Meta.pdf")
text = ""

for page in reader.pages:
    text += page.extract_text()

question = input("What do you want to know? ")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"""Document:{text} Question:{question}"""
        }
    ]
)

print(response.choices[0].message.content)    