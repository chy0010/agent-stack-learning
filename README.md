# Agent Stack Learning

This repository is a step-by-step learning project for building simple OpenAI agents in Python. Each file focuses on one idea: basic chat, memory, personality, streaming, and tool calling.

## Files

| File | What it teaches |
| --- | --- |
| `agent.py` | A basic one-question chatbot using the OpenAI API. |
| `memory_agent.py` | A chatbot that remembers the current conversation by storing messages in a list. |
| `personality_bot.py` | A chatbot with a system prompt that makes it act like a senior FAANG interviewer. |
| `streaming_bot.py` | A chatbot that streams the answer live instead of waiting for the full response. |
| `calculator_agent.py` | A function-calling example where the model can choose a calculator tool. |
| `weather_agent.py` | A function-calling example where the model can fetch current weather for a city. |
| `stock_agent.py` | A function-calling example with weather and stock price tools. |
| `multi_tool_agent.py` | A multi-tool example that lets the model choose between calculator, weather, and stock tools. |
| `.env.example` | Shows the environment variable needed to run the project. |
| `.gitignore` | Keeps secrets, virtual environments, and Python cache files out of Git. |

## Setup

Create a `.env` file based on `.env.example`:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Install the Python packages used by the scripts:

```bash
pip install openai python-dotenv requests
```

## Run Examples

```bash
python agent.py
python memory_agent.py
python streaming_bot.py
python calculator_agent.py
python weather_agent.py
python stock_agent.py
python multi_tool_agent.py
```

Type `quit` to exit the chat-loop examples.

## Learning Order

1. `agent.py`
2. `memory_agent.py`
3. `personality_bot.py`
4. `streaming_bot.py`
5. `calculator_agent.py`
6. `weather_agent.py`
7. `stock_agent.py`
8. `multi_tool_agent.py`

## Notes

This project is for learning. The calculator examples use Python `eval()`, which is useful for a small demo but should be replaced with a safer math parser in real applications.
