"""The single gate every tool call passes through.

Order: tier decision -> argument rules -> user confirmation -> run -> audit.
"""
from __future__ import annotations

from typing import Any, Callable

from butler import audit, policy, tools

# confirm(tool_name, decision, args) -> True if the user approved
Confirmer = Callable[[str, policy.Decision, dict[str, Any]], bool]


def run_tool(name: str, args: dict[str, Any], confirm: Confirmer) -> dict[str, Any]:
    if not isinstance(args, dict):
        return {"error": "arguments must be an object"}

    decision = policy.decide(name)
    audit.record("proposed", tool=name, args=args, decision=decision.value)

    if decision is policy.Decision.DENY:
        audit.record("blocked", tool=name, reason="forbidden or unknown tool")
        return {"error": f"'{name}' is not available"}

    violation = policy.argument_violation(name, args)
    if violation:
        audit.record("blocked", tool=name, reason=violation)
        return {"error": violation}

    if decision in (policy.Decision.CONFIRM, policy.Decision.TYPED_CONFIRM):
        if not confirm(name, decision, args):
            audit.record("denied_by_user", tool=name)
            return {"error": "the user did not approve this action"}

    impl = tools.IMPLEMENTATIONS.get(name)
    if impl is None:
        audit.record("error", tool=name, reason="no implementation")
        return {"error": f"'{name}' has no implementation"}

    try:
        result = impl(**args)
    except TypeError as exc:
        audit.record("error", tool=name, reason=f"bad arguments: {exc}")
        return {"error": f"bad arguments: {exc}"}
    except Exception as exc:  # noqa: BLE001 - report to the model, keep the app alive
        audit.record("error", tool=name, reason=str(exc))
        return {"error": f"tool failed: {exc}"}

    audit.record("executed", tool=name, ok="error" not in result)
    return result
