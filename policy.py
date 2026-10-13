"""Policy: tiers, decisions, and argument-level rules.

This is code, not model output. The model cannot change its own permissions.
Unknown tools are denied by default.
"""
from __future__ import annotations

import os
from enum import Enum
from pathlib import PureWindowsPath
from typing import Any


class Tier(str, Enum):
    READ = "read"
    REVERSIBLE = "reversible"
    SYSTEM = "system"
    DESTRUCTIVE = "destructive"
    FORBIDDEN = "forbidden"


class Decision(str, Enum):
    ALLOW = "allow"
    CONFIRM = "confirm"
    TYPED_CONFIRM = "typed_confirm"
    DENY = "deny"


TOOL_TIERS: dict[str, Tier] = {
    "system_info": Tier.READ,
    "list_directory": Tier.READ,
    "read_text_file": Tier.READ,
    "list_processes": Tier.READ,
    "open_app": Tier.REVERSIBLE,
    "create_folder": Tier.REVERSIBLE,
    # Reserved tiers. No implementation exists yet, so the model cannot reach them.
    "install_package": Tier.SYSTEM,
    "delete_path": Tier.DESTRUCTIVE,
    "format_drive": Tier.FORBIDDEN,
}

_DECISION_FOR_TIER: dict[Tier, Decision] = {
    Tier.READ: Decision.ALLOW,
    Tier.REVERSIBLE: Decision.ALLOW,
    Tier.SYSTEM: Decision.CONFIRM,
    Tier.DESTRUCTIVE: Decision.TYPED_CONFIRM,
    Tier.FORBIDDEN: Decision.DENY,
}

# Even with elevation, Butler never writes under these locations.
PROTECTED_WRITE_ROOTS = [
    r"C:\Windows",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\ProgramData",
]

WRITE_TOOLS = {"create_folder"}


def tier_for(tool_name: str) -> Tier:
    return TOOL_TIERS.get(tool_name, Tier.FORBIDDEN)


def decide(tool_name: str) -> Decision:
    return _DECISION_FOR_TIER[tier_for(tool_name)]


def _lower_parts(path: str) -> tuple[str, ...]:
    raw = PureWindowsPath(path)
    if not raw.is_absolute():
        raw = PureWindowsPath(os.path.abspath(path))
    return tuple(p.lower() for p in raw.parts)


def argument_violation(tool_name: str, args: dict[str, Any]) -> str | None:
    """Return a human-readable reason if the arguments break a hard rule, else None."""
    if tool_name in WRITE_TOOLS:
        target = _lower_parts(str(args.get("path", "")))
        for root in PROTECTED_WRITE_ROOTS:
            rp = tuple(p.lower() for p in PureWindowsPath(root).parts)
            if target[: len(rp)] == rp:
                return f"writes under {root} are blocked"
    return None
