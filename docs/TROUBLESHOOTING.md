# Troubleshooting

**`python` is not recognised in the elevated window.**
The elevated session can see a different PATH. Reinstall Python with "Add
python.exe to PATH" ticked, or replace `python` in `run_butler.bat` and
`doctor.bat` with the full path to `python.exe`.

**`doctor.py` says Ollama is not reachable.**
Start Ollama (tray app, or `ollama serve`). Open `http://localhost:11434/api/tags`
in a browser. You should see JSON.

**Model not available.**
Run `ollama list` and pass the exact name, including the tag, for example
`--model qwen2.5:7b`.

**The model answers in plain text and never calls tools.**
Not every model supports tool calling. Try `qwen2.5:7b` or `llama3.1:8b`. Check
the model's Ollama page for a "tools" capability.

**Tool calls fail with "bad arguments".**
The model used a wrong argument name. Ask again with the exact path, or check
`docs/TOOLS.md` for the expected names.

**`psutil` errors or missing system info.**
Run `pip install -r requirements.txt` with the same Python that runs Butler.

**The window closes immediately.**
Start Butler with `run_butler.bat`, not `main.py` directly. The launcher adds a
`pause` at the end.

**UAC prompt appears but nothing starts.**
Click Yes. If you clicked No, the launcher stops. Run it again.
