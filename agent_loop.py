from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import anyio
from mcp import ClientSession
from mcp.client.stdio import (stdio_client,StdioServerParameters)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)

calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "You MUST use this tool for all mathematical calculations.",
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

stock_tool = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Get stock price for a company ticker.",
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

tools = [
    calculator_tool,
    stock_tool
]

question = input("Ask something: ")

messages = [
    {
        "role": "system",
        "content": """
You are an AI agent.

You may call tools multiple times.

Keep calling tools until you have enough information.

Never perform math yourself.
Always use calculator tool.
"""
    },
    {
        "role": "user",
        "content": question
    }
]


async def main():

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            loop_count = 1

            while True:

                print(f"\n===== LOOP {loop_count} =====")

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=tools,
                    parallel_tool_calls=True
                )

                message = response.choices[0].message

                messages.append(message)

                # GPT is done
                if not message.tool_calls:

                    print("\nFINAL ANSWER:\n")
                    print(message.content)
                    break

                # Execute tools
                for tool_call in message.tool_calls:

                    tool_name = tool_call.function.name

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    print(
                        f"Calling Tool: {tool_name}"
                    )
                    print(arguments)

                    result = await session.call_tool(
                        tool_name,
                        arguments
                    )

                    tool_output = str(
                        result.content[0].text
                    )

                    print(
                        f"Tool Result: {tool_output}"
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_output
                        }
                    )

                loop_count += 1


anyio.run(main)