"""Orchestrates classification, tool routing, persistence, and general chat."""

from __future__ import annotations

from pathlib import Path

from app.general_chat import general_chat
from app.memory import load_history, save_history
from app.router import classify_intent
from app.tools.exchange_rate import get_exchange_rate
from app.tools.math_tool import calculate_math
from app.tools.weather import get_weather
from app.types import ChatMessage, LLMConfig, message_dict


def load_session(history_path: Path) -> list[ChatMessage]:
    return load_history(history_path)


def reset_session(history: list[ChatMessage], history_path: Path) -> None:
    history.clear()
    save_history(history_path, history)


def handle_user_message(
    history: list[ChatMessage],
    history_path: Path,
    llm_config: LLMConfig,
    user_text: str,
) -> str:
    user_text = user_text.strip()
    if not user_text:
        return "Say something, or type 'exit' to quit."

    decision = classify_intent(llm_config, user_text)
    reply: str

    if decision.intent == "weather" and decision.city:
        reply = get_weather(decision.city)
    elif decision.intent == "math" and decision.expression:
        reply = calculate_math(decision.expression)
    elif decision.intent == "exchange_rate" and decision.currency_code:
        reply = get_exchange_rate(decision.currency_code)
    else:
        reply = general_chat(llm_config, history, user_text)

    history.append(message_dict("user", user_text))
    history.append(message_dict("assistant", reply))
    save_history(history_path, history)
    return reply
