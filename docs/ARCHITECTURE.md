# Architecture

## Overview

Butler is one elevated Python process.

```
you (console)
   │ text
   ▼
agent.py ── HTTP ──► Ollama (localhost:11434, local model)
   │ tool call (name + JSON args)
   ▼
executor.py
   1. tier decision            (policy.decide)
   2. argument rules           (policy.argument_violation)
   3. user approval if needed  (agent.console_confirm)
   4. run implementation       (tools.IMPLEMENTATIONS)
   5. audit every step         (audit.record)
   │ result (JSON)
   ▼
agent.py → back to the model → answer to you
```

## Why one process

Version 0.1 split the model from an elevated broker connected by a localhost
HTTP server with a token file. That added a listening socket and an auth path
without protecting against the model itself. Since you asked for everything to
run elevated, v0.2 removes the server. The security boundary is now the
executor, and every tool call goes through the same checks in the same process.

## Design rules

- **The model proposes; code decides.** The model can only call tools in the
  schema list, and it cannot change policy.
- **Default deny.** Unknown names are denied. A tool with no implementation
  cannot run even if it is named.
- **Hard rules beat approvals.** Writes under `C:\Windows`, `C:\Program Files`,
  `C:\Program Files (x86)`, and `C:\ProgramData` are refused before you are asked.
- **Everything is audited.** Proposals, blocks, approvals, denials, and results
  are JSON lines.
- **Tool output is data.** The system prompt tells the model not to follow
  instructions found in tool output. That is a soft control. The hard controls
  are the allowlists, tiers, and protected roots.

## Module map

| Module | Responsibility | Depends on |
|---|---|---|
| `config` | Settings and paths | nothing |
| `admin` | Elevation check | nothing |
| `audit` | Append-only log | config |
| `policy` | Tiers, decisions, argument rules | nothing |
| `tools` | Implementations and schemas | psutil (optional) |
| `executor` | Gate: policy, rules, approval, run, audit | policy, tools, audit |
| `agent` | Ollama loop and approval prompts | executor, tools, config |
| `main`, `doctor` | Entry points | agent, admin, config |

## Data locations

- Audit log: `%USERPROFILE%\.butler\audit.jsonl`
- Override the folder with `BUTLER_DATA_DIR`.
- Override the Ollama address with `BUTLER_OLLAMA_URL`.
