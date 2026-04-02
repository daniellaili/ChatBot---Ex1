from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

from app.types import LLMConfig


def _build_client(cfg: LLMConfig) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The 'openai' package is not installed. Install it to use LLM chat features."
        ) from exc

    kwargs: Dict[str, Any] = {"api_key": cfg.api_key or "missing-key"}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def chat_completion(
    cfg: LLMConfig,
    messages: Sequence[Dict[str, str]],
    *,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Run a chat completion. Uses the configured model and provider endpoint.
    Raises on HTTP/API errors so callers can handle or convert to user-facing text.
    """
    if not cfg.model:
        raise ValueError("LLM_MODEL is not set.")
    if not cfg.api_key:
        raise ValueError("LLM_API_KEY is not set.")

    client = _build_client(cfg)
    req: Dict[str, Any] = {
        "model": cfg.model,
        "messages": list(messages),
        "temperature": temperature,
    }
    if max_tokens is not None:
        req["max_tokens"] = max_tokens

    response = client.chat.completions.create(**req)
    choice = response.choices[0].message
    content = choice.content
    if not content:
        return ""
    return content.strip()
