"""Elevation checks. Butler is designed to run in an elevated console."""
from __future__ import annotations

import os
import platform


def is_elevated() -> bool:
    if platform.system() == "Windows":
        import ctypes
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            return False
    geteuid = getattr(os, "geteuid", None)
    return bool(geteuid and geteuid() == 0)
