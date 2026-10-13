"""Health check: Python, elevation, Ollama, the chosen model, and optional deps."""
from __future__ import annotations

import argparse
import sys

import requests

from butler.admin import is_elevated
from butler.config import DEFAULT_MODEL, OLLAMA_URL


def _mark(ok: bool) -> str:
    return "[ OK ]" if ok else "[FAIL]"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Butler's setup.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    failures = 0

    py_ok = sys.version_info >= (3, 10)
    print(f"{_mark(py_ok)} Python {sys.version.split()[0]} (need 3.10+)")
    failures += not py_ok

    elevated = is_elevated()
    print(f"{_mark(elevated)} Running elevated (administrator / root)")
    failures += not elevated

    try:
        import psutil  # noqa: F401
        print(f"{_mark(True)} psutil installed")
    except ImportError:
        print(f"{_mark(False)} psutil missing: pip install psutil")
        failures += 1

    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        names = [m["name"] for m in resp.json().get("models", [])]
        print(f"{_mark(True)} Ollama reachable at {OLLAMA_URL}")
        print(f"      installed models: {', '.join(names) or '(none)'}")
        wanted = args.model if ":" in args.model else f"{args.model}:latest"
        has_model = args.model in names or wanted in names
        print(f"{_mark(has_model)} model '{args.model}' available")
        failures += not has_model
    except requests.RequestException as exc:
        print(f"{_mark(False)} Ollama not reachable at {OLLAMA_URL}: {exc}")
        failures += 1

    print("\nAll checks passed." if failures == 0 else f"\n{failures} check(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
