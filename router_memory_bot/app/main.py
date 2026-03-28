"""CLI entrypoint for Router & Memory Bot."""

from __future__ import annotations

import sys

from app.agent import handle_user_message, load_session, reset_session
from app.config import get_history_path, get_llm_config


def _print_banner() -> None:
    print("Router & Memory Bot")
    print("Commands: exit | quit | /reset")
    print("Uses LLM_* env vars (OpenAI-compatible API).")
    print()


def main() -> int:
    _print_banner()
    cfg = get_llm_config()
    history_path = get_history_path()
    history = load_session(history_path)

    if not cfg.api_key or not cfg.model:
        print(
            "Warning: LLM_API_KEY and LLM_MODEL should be set for full functionality.",
            file=sys.stderr,
        )

    while True:
        try:
            line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0

        if not line:
            continue
        lower = line.lower()
        if lower in {"exit", "quit", "/exit", "/quit"}:
            print("Bye.")
            return 0
        if lower == "/reset":
            reset_session(history, history_path)
            print("History cleared.")
            continue

        try:
            answer = handle_user_message(history, history_path, cfg, line)
        except Exception as exc:
            print(f"Bot: Something went wrong: {exc}")
            continue
        print(f"Bot: {answer}")


if __name__ == "__main__":
    raise SystemExit(main())
