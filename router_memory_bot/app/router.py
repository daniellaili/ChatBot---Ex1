"""LLM-based intent classification with strict JSON validation."""

from __future__ import annotations

import json
import re
from typing import Any

from app.llm_client import chat_completion
from app.prompts import CLASSIFIER_SYSTEM
from app.types import ClassificationPayload, IntentName, LLMConfig, RoutingDecision

_VALID_INTENTS: frozenset[str] = frozenset({"weather", "math", "exchange_rate", "general_chat"})


def _extract_json_object(text: str) -> str | None:
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    fence = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text, re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return None


def _coerce_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return None


def _parse_payload(raw: str) -> ClassificationPayload | None:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data  # type: ignore[return-value]


def _validate_routing(payload: ClassificationPayload) -> RoutingDecision | None:
    intent_raw = payload.get("intent")
    if not isinstance(intent_raw, str):
        return None
    intent_norm = intent_raw.strip().lower()
    if intent_norm not in _VALID_INTENTS:
        return None
    intent: IntentName = intent_norm  # type: ignore[assignment]

    city = _coerce_str(payload.get("city"))
    expression = _coerce_str(payload.get("expression"))
    currency = _coerce_str(payload.get("currency_code"))

    if intent == "weather":
        if not city:
            return None
        return RoutingDecision(intent=intent, city=city)
    if intent == "math":
        if not expression:
            return None
        return RoutingDecision(intent=intent, expression=expression)
    if intent == "exchange_rate":
        if not currency:
            return None
        return RoutingDecision(intent=intent, currency_code=currency)
    return RoutingDecision(intent="general_chat")


def classify_intent(cfg: LLMConfig, user_input: str) -> RoutingDecision:
    """
    Classify the latest user message. On invalid JSON, missing fields, or unknown intent,
    returns intent general_chat so the orchestrator uses the general chat path.
    """
    trimmed = user_input.strip()
    if not trimmed:
        return RoutingDecision(intent="general_chat")

    messages = [
        {"role": "system", "content": CLASSIFIER_SYSTEM},
        {"role": "user", "content": trimmed},
    ]
    try:
        raw_reply = chat_completion(cfg, messages, temperature=0.0, max_tokens=256)
    except Exception:
        return RoutingDecision(intent="general_chat")

    blob = _extract_json_object(raw_reply)
    if not blob:
        return RoutingDecision(intent="general_chat")

    payload = _parse_payload(blob)
    if payload is None:
        return RoutingDecision(intent="general_chat")

    decision = _validate_routing(payload)
    if decision is None:
        return RoutingDecision(intent="general_chat")
    return decision
