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

def get_stock_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return f"{symbol.upper()} stock price is ${price}"

    except Exception as e:
        return f"Unable to fetch stock price for {symbol}"

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
                        "type": "string"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker like AAPL, TSLA, MSFT"
                    }
                },
                "required": ["symbol"]
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

    if tool_name == "get_weather":
        city = arguments["city"]
        result = get_weather(city)
        
    elif tool_name == "get_stock_price":
        symbol = arguments["symbol"]
        result = get_stock_price(symbol)

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