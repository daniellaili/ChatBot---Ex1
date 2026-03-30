"""Shared typed structures for routing, chat, and configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, TypedDict

IntentName = Literal["weather", "math", "exchange_rate", "general_chat"]


class ChatMessage(TypedDict):
    """Single turn in persisted conversation history."""

    role: Literal["user", "assistant"]
    content: str


class ClassificationPayload(TypedDict, total=False):
    """Strict JSON contract from the classifier LLM."""

    intent: str
    city: str
    expression: str
    currency_code: str


@dataclass(frozen=True)
class RoutingDecision:
    """Validated routing outcome after parsing classifier JSON."""

    intent: IntentName
    city: Optional[str] = None
    expression: Optional[str] = None
    currency_code: Optional[str] = None


@dataclass(frozen=True)
class LLMConfig:
    """OpenAI-compatible client settings."""

    api_key: str
    base_url: Optional[str]
    model: str


def message_dict(role: Literal["user", "assistant"], content: str) -> ChatMessage:
    return {"role": role, "content": content}


def history_to_openai_messages(history: List[ChatMessage]) -> List[Dict[str, Any]]:
    return [{"role": m["role"], "content": m["content"]} for m in history]
