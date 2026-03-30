"""General LLM chat fallback with full conversation history."""

from __future__ import annotations

from typing import Dict, List

from app.llm_client import chat_completion
from app.prompts import GENERAL_CHAT_SYSTEM
from app.types import ChatMessage, LLMConfig, history_to_openai_messages


def general_chat(cfg: LLMConfig, history: List[ChatMessage], user_input: str) -> str:
    """Answer using the chat model with system prompt + full history + current user turn."""
    messages: List[Dict[str, str]] = [{"role": "system", "content": GENERAL_CHAT_SYSTEM}]
    messages.extend(history_to_openai_messages(history))
    messages.append({"role": "user", "content": user_input})
    try:
        return chat_completion(cfg, messages, temperature=0.6, max_tokens=1024)
    except Exception as exc:
        return f"Sorry, the language model request failed: {exc}"
