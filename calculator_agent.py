from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculator(expression):
    return eval(expression)

question = input("Ask math question: ")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",                                                         # Tool name = calculator
            "description": "Calculate math expressions exactly",                          # When should GPT use this?

            "parameters": {                                                               # What inputs does tool need?
                "type": "object",
                "properties": {                                                           # Input variable name = expression
                    "expression": {
                        "type": "string",                                                 # expression should be text
                        "description": "Math expression to calculate"
                    }
                },
                "required": ["expression"]                                                # i need expression to give as and input to calculator (ex: 3*4)
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
content=response.choices[0].message.content

if tool_calls:
    tool_call = tool_calls[0]
    tool_name = tool_call.function.name
    arguments = tool_call.function.arguments                                                     
    arguments = json.loads(arguments)                                                               # arguments = '{"expression":"500 * 2"}'   -->    arguments = {"expression": "500 * 2"}     JSON text/string  →  Python dictionary object
    expression = arguments["expression"]                                                            # expression = "500 * 2"
    result = calculator(expression)
    print("Result:", result)
else:
    print("Content:", content)
    





#How does it look like inside "RESPONSE"

# TOOL CALL RESPONSE

# {
#     "choices": [
#         {
#             "finish_reason": "tool_calls",

#             "message": {
#                 "role": "assistant",
#                 "content": None,

#                 "tool_calls": [
#                     {
#                         "function": {
#                             "name": "calculator",
#                             "arguments": "{\"expression\":\"500 * 2\"}"
#                         }
#                     }
#                 ]
#             }
#         }
#     ]
# }