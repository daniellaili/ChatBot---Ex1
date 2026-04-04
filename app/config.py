from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from app.types import LLMConfig

_ENV_LOADED = False

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        return None


def _ensure_env_loaded() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    load_dotenv()
    _ENV_LOADED = True


def get_llm_config() -> LLMConfig:
    _ensure_env_loaded()
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url_raw = os.environ.get("LLM_BASE_URL", "").strip()
    model = os.environ.get("LLM_MODEL", "").strip()
    base_url: Optional[str] = base_url_raw if base_url_raw else None
    return LLMConfig(api_key=api_key, base_url=base_url, model=model)


def get_history_path() -> Path:
    _ensure_env_loaded()
    raw = os.environ.get("CHAT_HISTORY_PATH", os.environ.get("HISTORY_FILE", "history.json")).strip()
    return Path(raw).expanduser().resolve()
