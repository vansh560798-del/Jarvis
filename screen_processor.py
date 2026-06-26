from __future__ import annotations

import subprocess
from pathlib import Path
from datetime import datetime


def screen_process(*args, **kwargs):
    parameters = kwargs.get("parameters") or (args[0] if args else {}) or {}
    angle = str(parameters.get("angle", "screen")).lower()
    text = str(parameters.get("text", "Analyze this screen."))
    out_dir = Path.home() / "Desktop" / "Jarvis_Screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    try:
        if angle == "camera":
            return "Camera capture is not enabled in this Mac build yet. Use screen capture."
        # macOS built-in screenshot. Requires Screen Recording permission.
        r = subprocess.run(["screencapture", "-x", str(path)], capture_output=True, text=True, check=False)
        if r.returncode != 0:
            return "Screen capture failed. Enable Screen Recording for Terminal/Python in Privacy & Security."
        return f"Screen captured for: {text}. Saved at {path}."
    except Exception as e:
        return f"screen_process failed: {e}. Enable Screen Recording permission."
