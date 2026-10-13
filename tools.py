"""Tool implementations and the JSON schemas the model sees.

Only tools listed in TOOL_SCHEMAS are visible to the model, and only tools in
IMPLEMENTATIONS can run.
"""
from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Callable

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None

MAX_READ_BYTES = 64 * 1024
MAX_LIST_ENTRIES = 200

APP_ALLOWLIST = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    "paint": "mspaint.exe",
}


def system_info() -> dict[str, Any]:
    info: dict[str, Any] = {
        "os": platform.platform(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }
    if psutil:
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(os.path.abspath(os.sep))
        info.update({
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "ram_total_gb": round(mem.total / 1e9, 1),
            "ram_used_percent": mem.percent,
            "disk_total_gb": round(disk.total / 1e9, 1),
            "disk_free_gb": round(disk.free / 1e9, 1),
        })
    return info


def list_directory(path: str) -> dict[str, Any]:
    p = Path(path).expanduser()
    if not p.is_dir():
        return {"error": f"not a directory: {p}"}
    entries = sorted(p.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    return {
        "path": str(p),
        "entries": [{"name": e.name, "type": "dir" if e.is_dir() else "file"}
                    for e in entries[:MAX_LIST_ENTRIES]],
        "truncated": len(entries) > MAX_LIST_ENTRIES,
    }


def read_text_file(path: str) -> dict[str, Any]:
    p = Path(path).expanduser()
    if not p.is_file():
        return {"error": f"not a file: {p}"}
    with p.open("rb") as f:
        data = f.read(MAX_READ_BYTES + 1)
    return {
        "path": str(p),
        "text": data[:MAX_READ_BYTES].decode("utf-8", errors="replace"),
        "truncated": len(data) > MAX_READ_BYTES,
    }


def list_processes(limit: int = 15) -> dict[str, Any]:
    if not psutil:
        return {"error": "psutil is not installed"}
    procs = []
    for proc in psutil.process_iter(["pid", "name", "memory_info"]):
        try:
            mi = proc.info["memory_info"]
            procs.append({"pid": proc.info["pid"], "name": proc.info["name"],
                          "mem_mb": round((mi.rss if mi else 0) / 1e6, 1)})
        except (psutil.Error, AttributeError):
            continue
    procs.sort(key=lambda p: p["mem_mb"], reverse=True)
    return {"top": procs[: max(1, min(int(limit), 50))]}


def open_app(name: str) -> dict[str, Any]:
    key = str(name).strip().lower()
    if key not in APP_ALLOWLIST:
        return {"error": f"'{name}' is not in the app allowlist",
                "allowed": sorted(APP_ALLOWLIST)}
    if platform.system() != "Windows":
        return {"error": "open_app only works on Windows"}
    subprocess.Popen([APP_ALLOWLIST[key]], shell=False)
    return {"launched": key}


def create_folder(path: str) -> dict[str, Any]:
    p = Path(path).expanduser()
    if p.exists():
        return {"error": f"already exists: {p}"}
    p.mkdir(parents=True)
    return {"created": str(p)}


IMPLEMENTATIONS: dict[str, Callable[..., dict[str, Any]]] = {
    "system_info": system_info,
    "list_directory": list_directory,
    "read_text_file": read_text_file,
    "list_processes": list_processes,
    "open_app": open_app,
    "create_folder": create_folder,
}


def _schema(name: str, description: str, props: dict[str, Any] | None = None,
            required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {"type": "object",
                           "properties": props or {},
                           "required": required or []},
        },
    }


TOOL_SCHEMAS: list[dict[str, Any]] = [
    _schema("system_info", "Get OS, CPU, RAM and disk summary."),
    _schema("list_directory", "List files and folders in a directory.",
            {"path": {"type": "string", "description": "Absolute directory path"}},
            ["path"]),
    _schema("read_text_file", "Read the start of a small text file.",
            {"path": {"type": "string", "description": "Absolute file path"}},
            ["path"]),
    _schema("list_processes", "List the top processes by memory use.",
            {"limit": {"type": "integer", "description": "How many, max 50"}}),
    _schema("open_app", "Open an allowlisted app.",
            {"name": {"type": "string", "enum": sorted(APP_ALLOWLIST)}}, ["name"]),
    _schema("create_folder", "Create a new folder. Fails if it already exists.",
            {"path": {"type": "string", "description": "Absolute folder path"}},
            ["path"]),
]
