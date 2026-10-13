# Changelog

## 0.2.0
- Single elevated process. Removed the localhost broker, token file, and HTTP layer.
- `executor.py` is now the one gate for all tool calls.
- Approval prompts for system-tier tools, typed confirmation for destructive tools.
- Protected write roots (Windows, Program Files, ProgramData).
- Removed the `set_volume` stub so the model cannot call a function that does nothing.
- `doctor.py` health check and self-elevating `.bat` launchers.
- `--model` flag to choose any installed Ollama model.
- Documentation: architecture, tools, security, troubleshooting, extending, changelog.

## 0.1.0
- Initial design: unelevated agent, elevated broker over localhost.
