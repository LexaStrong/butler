# Butler

A local, policy-gated AI assistant for Windows. It runs in an elevated console, uses a local Ollama model, and can act only through named tools that pass a policy check and are written to an audit log.

Read `docs/` for architecture, tools, security, and troubleshooting. **Read `docs/SECURITY.md` before using it on anything you care about.**

## Quick start

1. Install Python 3.10+ with "Add to PATH" ticked.
2. Confirm your models: `ollama list`
3. In this folder, run: `pip install -r requirements.txt`
4. Double-click `doctor.bat` and accept the UAC prompt. Fix anything marked `[FAIL]`.
5. Double-click `run_butler.bat` and accept the UAC prompt.

Choose a model per run:

    run_butler.bat --model llama3.1:8b

Or set it once for all runs:

    setx BUTLER_MODEL llama3.1:8b

Open a new console after `setx`.

## Tests

    pytest -q

## Files

| Path | Purpose |
|---|---|
| `main.py` | Chat loop |
| `doctor.py` | Setup and health check |
| `run_butler.bat`, `doctor.bat` | Self-elevating launchers |
| `butler/policy.py` | Tiers, decisions, protected paths |
| `butler/executor.py` | The one gate every tool call passes through |
| `butler/tools.py` | Tool implementations and model-facing schemas |
| `butler/agent.py` | Ollama chat loop and approval prompts |
| `butler/audit.py` | Append-only JSONL audit log |
| `butler/admin.py` | Elevation check |
| `butler/config.py` | Settings and environment overrides |
| `tests/` | Pytest suite |
| `docs/` | Architecture, tools, security, troubleshooting, extending, changelog |

Audit log: `%USERPROFILE%\.butler\audit.jsonl`
