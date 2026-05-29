from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_weather(city):

    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(url)                                           #get data from that url

    data = response.json()                                                  # covert JSON data into pyton readble formate

    temperature = data["current_condition"][0]["temp_F"]                     # get the exact temp

    return f"{city} temperature is {temperature}°F"                       


question = input("Ask something: ")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    tools=tools
)

tool_calls = response.choices[0].message.tool_calls

if tool_calls:

    tool_call = tool_calls[0]

    tool_name = tool_call.function.name

    arguments = tool_call.function.arguments

    arguments = json.loads(arguments)

    city = arguments["city"]

    result = get_weather(city)

    messages = [
    {
        "role": "user",
        "content": question
    },response.choices[0].message,{
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    }]

    final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
    final_answer = final_response.choices[0].message.content
    print(final_answer)