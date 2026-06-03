from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from mcp import ClientSession
from mcp.client.stdio import stdio_client,StdioServerParameters
import anyio

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

calculator_tool = {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "You MUST use this tool for any mathematical operation involving numbers. Never calculate manually.",
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

tools=[
    calculator_tool,
    stock_tool
]

question = input("Ask something: ")

response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    tools=tools,
    parallel_tool_calls=True
)

messages = [
                {
                    "role": "user",
                    "content": question
                },
                response.choices[0].message
            ]

tool_calls = response.choices[0].message.tool_calls

print(tool_calls)

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)

async def main():

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            for tool_call in tool_calls:

                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                result = await session.call_tool(
                    tool_name,
                    arguments
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result.content[0].text)
                    }
                )

            final_response = client.chat.completions.create(
                model="gpt-5.5",
                messages=messages
            )

            print(final_response.choices[0].message.content)

anyio.run(main)