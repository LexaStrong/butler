"""Append-only JSONL audit log. Every proposal, decision, and result is recorded."""
from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from typing import Any

from butler.config import AUDIT_FILE, ensure_data_dir

_lock = threading.Lock()


def record(event: str, **fields: Any) -> None:
    ensure_data_dir()
    entry = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, **fields}
    line = json.dumps(entry, default=str)
    with _lock, AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
