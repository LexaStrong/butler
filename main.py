"""Butler chat loop. Run from an elevated console (see run_butler.bat)."""
from __future__ import annotations

import argparse

from butler.admin import is_elevated
from butler.agent import Agent
from butler.config import DEFAULT_MODEL


def main() -> None:
    parser = argparse.ArgumentParser(description="Butler, a local PC assistant.")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Ollama model name, e.g. qwen2.5:7b or llama3.1:8b")
    args = parser.parse_args()

    if not is_elevated():
        print("Warning: not running elevated. Admin-only actions will fail.")

    agent = Agent(model=args.model)
    print(f"Butler ready (model: {args.model}). Type a request, or 'quit' to exit.")
    while True:
        try:
            text = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text.lower() in {"quit", "exit"}:
            break
        try:
            print(f"\nbutler> {agent.ask(text)}")
        except Exception as exc:  # noqa: BLE001
            print(f"\nbutler> error: {exc}")


if __name__ == "__main__":
    main()
