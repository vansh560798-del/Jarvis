from __future__ import annotations
import platform
import subprocess
import shutil

_APP_ALIASES = {
    "browser": "Safari", "safari": "Safari", "chrome": "Google Chrome",
    "google chrome": "Google Chrome", "edge": "Microsoft Edge",
    "vscode": "Visual Studio Code", "vs code": "Visual Studio Code",
    "terminal": "Terminal", "finder": "Finder", "settings": "System Settings",
    "system settings": "System Settings", "notes": "Notes", "messages": "Messages",
    "whatsapp": "WhatsApp", "spotify": "Spotify", "photoshop": "Adobe Photoshop 2025",
}

def open_app(parameters=None, response=None, player=None, **kwargs):
    parameters = parameters or {}
    app = str(parameters.get("app_name") or parameters.get("app") or "").strip()
    if not app:
        return "No app name given."
    app = _APP_ALIASES.get(app.lower(), app)
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", "-a", app])
        elif system == "Windows":
            import os
            os.startfile(app)  # type: ignore[attr-defined]
        else:
            subprocess.Popen([shutil.which(app) or app])
        return f"Opened {app}."
    except Exception as e:
        return f"Could not open {app}: {e}"
