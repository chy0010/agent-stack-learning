from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculator(expression):
    return str(eval(expression))


def get_weather(city):
    return f"{city} is 70°F"


def get_stock_price(symbol):
    return f"{symbol} is $100"

question = input("Ask something: ")



stock_tool= {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Get stock price for a company ticker",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string"
                }
            },
            "required": ["symbol"]
        }
    }
}
    


calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform mathematical calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string"
                }
            },
            "required": ["expression"]
        }
    }
}

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string"
                }
            },
            "required": ["city"]
        }
    }
}


tools = [
    stock_tool,
    calculator_tool,
    weather_tool
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
    print("Selected Tool:", tool_call.function.name)
    print("Arguments:", tool_call.function.arguments)
    print(response.choices[0].message)