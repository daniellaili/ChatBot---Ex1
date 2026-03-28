# Router & Memory Bot

A small **Python CLI** agent that classifies user intent, routes to tools (weather, math, exchange rates), persists chat history, and falls back to a general **OpenAI-compatible** chat model.

## Features

- **Router**: LLM returns **JSON only**; invalid JSON, unknown intents, or missing required fields → **general chat** fallback.
- **Tools**: real weather (Open-Meteo), safe deterministic math (`ast`), static FX table.
- **Memory**: loads/saves `history.json` after each turn; `/reset` clears history.

## Setup

```bash
cd router_memory_bot
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

| Variable       | Purpose                                      |
|----------------|----------------------------------------------|
| `LLM_API_KEY`  | Provider API key (e.g. Google AI Studio key) |
| `LLM_BASE_URL` | OpenAI-compatible base URL (optional if default) |
| `LLM_MODEL`    | Model name your provider expects             |

Example for **Google Generative Language OpenAI-compatible** endpoint:

```env
LLM_API_KEY=your_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-1.5-flash
```

Use the exact base URL and model string your provider documents; the client does **not** hardcode OpenAI’s public URL.

Optional:

```env
CHAT_HISTORY_PATH=history.json
```

## Run

From the `router_memory_bot` directory (so `app` is importable):

```bash
python -m app.main
```

## CLI

- `exit` / `quit` — leave the loop.
- `/reset` — clear in-memory history and delete the history file content (empty save).

## Layout

- `app/agent.py` — orchestration
- `app/router.py` — classification + JSON validation
- `app/llm_client.py` — OpenAI-compatible client wrapper
- `app/memory.py` — JSON persistence
- `app/general_chat.py` — fallback chat with full history
- `app/tools/` — `weather`, `math_tool`, `exchange_rate`

## Assignment notes

Intent JSON contract (classifier output):

```json
{
  "intent": "weather | math | exchange_rate | general_chat",
  "city": "string or null",
  "expression": "string or null",
  "currency_code": "string or null"
}
```

Weather data is from **Open-Meteo** (no API key). Exchange rates are **illustrative** static values, not live market data.
