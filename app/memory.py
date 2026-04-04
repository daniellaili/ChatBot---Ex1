from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.types import ChatMessage


def load_history(path: Path) -> List[ChatMessage]:
    if not path.is_file():
        return []
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []

    out: List[ChatMessage] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in ("user", "assistant"):
            continue
        if not isinstance(content, str):
            continue
        out.append({"role": role, "content": content})
    return out


def save_history(path: Path, history: List[ChatMessage]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = [{"role": m["role"], "content": m["content"]} for m in history]
    path.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
