# Router & Memory Bot

A small CLI chatbot that uses an OpenAI-compatible LLM for routing and general chat, and local tools for weather, math, and exchange-rate responses.

## Features

- Routes each user message into one of four intents:
  - `weather`
  - `math`
  - `exchange_rate`
  - `general_chat`
- Stores chat history in a JSON file and reloads it on the next run
- Supports `/reset` to clear the saved conversation
- Uses:
  - Open-Meteo for weather
  - a safe AST-based evaluator for math
  - a local dictionary for exchange rates against ILS

## Project Structure

```text
app/
  main.py              CLI entrypoint
  agent.py             Main orchestration logic
  router.py            LLM-based intent classifier
  general_chat.py      General chat fallback
  llm_client.py        OpenAI-compatible client wrapper
  config.py            Environment loading
  memory.py            History persistence
  prompts.py           System prompts
  tools/
    weather.py         Weather tool
    math_tool.py       Math tool
    exchange_rate.py   Exchange-rate tool
data/
  history.json         Generated local chat history file
```

## Requirements

- Python 3.8+
- An OpenAI-compatible API key and endpoint

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Or with a regular Python environment:

```powershell
python -m pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash
HISTORY_FILE=data/history.json
```

Notes:

- `LLM_API_KEY` is required for LLM-based routing and general chat.
- `LLM_BASE_URL` should point to an OpenAI-compatible endpoint.
- `LLM_MODEL` must be a model name supported by that endpoint.
- `HISTORY_FILE` is optional. If omitted, the app falls back to `history.json`.

## Running the App

From the project root:

```powershell
.\.venv\Scripts\python.exe -m app.main
```

If you are not using the local virtual environment:

```powershell
python -m app.main
```

## Commands

- `exit` or `quit` closes the app
- `/reset` clears the saved chat history

## Example Prompts

- `what is the weather in Tel Aviv?`
- `calculate 15 * (3 + 2)`
- `what is the dollar exchange rate?`
- `hi`

## Current Behavior

- Weather responses are fetched from Open-Meteo.
- Math is handled locally without using the LLM.
- Exchange rates are dictionary-based and currently return values relative to ILS.
- If LLM routing fails, the app falls back to `general_chat`.

## Persistence

Conversation history is stored as JSON and is loaded automatically on the next run.

By default, history is written to `data/history.json` when `HISTORY_FILE=data/history.json` is set in `.env`. This file is local runtime state and may be ignored by git, so it might not appear in the repository itself.

Current implementation writes history through Python file I/O in `app/memory.py`.

## Limitations

- Weather depends on external network access.
- Routing and general chat depend on the configured LLM being reachable.
- Exchange rates are static dictionary values, not live market data.
