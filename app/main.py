from __future__ import annotations

import asyncio

from app.agent import Agent
from app.config import get_settings
from app.memory import history_exists


async def run() -> None:
    settings = get_settings()

    if not settings.llm_api_key:
        print("Missing LLM_API_KEY in .env")
        return

    if not settings.llm_base_url:
        print("Missing LLM_BASE_URL in .env")
        return

    had_history = history_exists(settings.history_file)
    agent = Agent.create(settings)

    print("Router & Memory Bot started.")
    if had_history and agent.history:
        print("Welcome back. Previous history was loaded.")
    else:
        print("Starting a fresh conversation.")
    print("Type '/reset' to clear memory. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        response = await agent.handle_input(user_input)
        print(f"Bot: {response}\n")


if __name__ == "__main__":
    asyncio.run(run())