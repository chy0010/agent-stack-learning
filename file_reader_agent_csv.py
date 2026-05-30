from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



df = pd.read_csv("Fact_Sales_1.csv")

text = df.head(20).to_string()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"Summarize this CSV:\n\n{text}"
        }
    ]
)

print(response.choices[0].message.content)