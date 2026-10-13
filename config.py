"""Central configuration. Override with environment variables where noted."""
from __future__ import annotations

import os
from pathlib import Path

OLLAMA_URL = os.environ.get("BUTLER_OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("BUTLER_MODEL", "qwen2.5:7b")
MAX_AGENT_STEPS = 6          # hard cap on tool-call rounds per request
OLLAMA_TIMEOUT_S = 180

DATA_DIR = Path(os.environ.get("BUTLER_DATA_DIR", Path.home() / ".butler"))
AUDIT_FILE = DATA_DIR / "audit.jsonl"


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
