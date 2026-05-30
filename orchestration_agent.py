from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    

def calculator(expression):
    return str(eval(expression))





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
        "description":"Perform ALL mathematical calculations. Use this tool whenever numbers need to be added, subtracted, multiplied, divided, or compared.",
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

tools = [
    stock_tool,
    calculator_tool,
]

question = input("Ask something: ")


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    tools=tools,
    parallel_tool_calls=True
)

tool_calls = response.choices[0].message.tool_calls

print("Number of tool calls:", len(tool_calls))

messages = [
    {
        "role": "user",
        "content": question
    },
    response.choices[0].message
]

for tool_call in tool_calls:

    arguments = json.loads(tool_call.function.arguments)
    tool_name = tool_call.function.name

    if tool_name == "get_stock_price":
        symbol = arguments["symbol"]
        result = get_stock_price(symbol)

    elif tool_name == "calculator":
        expression = arguments["expression"]
        result = calculator(expression)

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
    )

for tool_call in tool_calls:
    print("---------------------------------------------------------")
    print(tool_call.function.name)
    print(tool_call.function.arguments)
print("---------------------------------------------------------")
print(messages)

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(final_response.choices[0].message.content)

#tool call:[ChatCompletionMessageFunctionToolCall(id='call_nbfWVzSqm55YMsIuyA2X7zPK', function=Function(arguments='{"symbol": "GOOGL"}', name='get_stock_price'), type='function'),
#            ChatCompletionMessageFunctionToolCall(id='call_ggPGMvJWNjjoawWSHRSQfpQ2', function=Function(arguments='{"symbol": "AAPL"}', name='get_stock_price'), type='function')]

