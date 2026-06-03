# 🤖 Agent Stack Learning

> A hands-on progression from your first chatbot to a fully orchestrated, MCP-powered AI agent — all in Python.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What You'll Learn

- How to call the OpenAI API from scratch
- How to give an agent memory, personality, and streaming output
- How to wire up **function/tool calling** so the model can run real code
- How to handle **multi-tool orchestration** across several APIs
- How to read and reason over **CSV and PDF files**
- How to build and connect to an **MCP server** for modular, reusable tools

---

## Quick Start

```bash
# 1. Clone and enter the repo
git clone https://github.com/chy0010/agent-stack-learning.git
cd agent-stack-learning

# 2. Set up your environment
cp .env.example .env
# → Add your OpenAI API key inside .env

# 3. Install dependencies
pip install openai python-dotenv requests pandas pypdf mcp anyio

# 4. Run your first agent
python agent.py
```

> Type `quit` to exit any chat-loop example.

---

## Learning Path

Work through the scripts in order — each one builds on the last.

| # | File | Concept |
|---|------|---------|
| 1 | `agent.py` | Single-turn chat with the OpenAI API |
| 2 | `memory_agent.py` | Multi-turn memory via message history |
| 3 | `personality_bot.py` | System prompts and persona shaping |
| 4 | `streaming_bot.py` | Streaming responses token-by-token |
| 5 | `calculator_agent.py` | Function calling — first tool integration |
| 6 | `weather_agent.py` | Calling a real external API via tool use |
| 7 | `stock_agent.py` | Multiple tools in one agent |
| 8 | `multi_tool_agent.py` | Model chooses between calculator, weather & stocks |
| 9 | `file_reader_agent_csv.py` | Reading & summarising CSV data with pandas |
| 10 | `file_reader_agent_pdf.py` | Extracting text from PDFs and Q&A over them |
| 11 | `orchestration_agent.py` | Chaining tool calls to combine results |
| 12 | `mcp_server.py` | Building a reusable MCP tool server |
| 13 | `mcp_client.py` | Connecting to the MCP server directly |
| 14 | `mcp_agent.py` | Routing OpenAI tool calls through MCP |

---

## Architecture Overview

```
Basic Chat ──► Memory ──► Personality ──► Streaming
                                              │
                                              ▼
                            Tool Calling (calculator / weather / stocks)
                                              │
                                              ▼
                               File Readers (CSV / PDF)
                                              │
                                              ▼
                              Orchestration Agent (multi-tool)
                                              │
                                              ▼
                         MCP Server ◄──── MCP Agent ◄──── MCP Client
```

---

## Sample Data

| File | Used by |
|------|---------|
| `Fact_Sales_1.csv` | `file_reader_agent_csv.py` |
| `Meta.pdf` | `file_reader_agent_pdf.py` |
| `sample.txt` | General file-reading practice |

---

## Setup Details

### Environment Variables

Copy `.env.example` to `.env` and fill in your key:

```
OPENAI_API_KEY=sk-...
```

### Running the MCP Examples

The MCP agent requires the server to be running first:

```bash
# Terminal 1 — start the server
python mcp_server.py

# Terminal 2 — run the agent or client
python mcp_agent.py
python mcp_client.py
```

---

## Notes

- The `calculator_agent.py` uses Python `eval()` — fine for demos, but swap it for a proper math parser in production.
- All agents default to `gpt-4o-mini` to keep API costs low while learning.
- No frameworks (LangChain, etc.) are used on purpose — everything is written against the raw OpenAI API so you can see exactly what's happening.
