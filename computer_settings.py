from __future__ import annotations

import subprocess


def _osa(script: str):
    return subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)


def computer_settings(*args, **kwargs):
    parameters = kwargs.get("parameters") or (args[0] if args else {}) or {}
    action = str(parameters.get("action") or parameters.get("description") or "").lower()
    value = parameters.get("value")
    try:
        if "volume" in action:
            if value is None:
                value = "50"
            _osa(f"set volume output volume {int(value)}")
            return f"Volume set to {value}."
        if "mute" in action:
            _osa("set volume with output muted")
            return "Muted."
        if "unmute" in action:
            _osa("set volume without output muted")
            return "Unmuted."
        if "brightness" in action:
            return "Brightness control needs the optional `brightness` CLI. Install with: brew install brightness"
        if "screenshot" in action:
            subprocess.run(["screencapture", "-x", str(value or "$HOME/Desktop/jarvis_screenshot.png")], check=False)
            return "Screenshot taken."
        if "lock" in action:
            subprocess.run(["pmset", "displaysleepnow"], check=False)
            return "Locked/slept display."
        if "dark" in action:
            _osa('tell application "System Events" to tell appearance preferences to set dark mode to true')
            return "Dark mode enabled."
        if "light" in action:
            _osa('tell application "System Events" to tell appearance preferences to set dark mode to false')
            return "Light mode enabled."
        if "close" in action:
            _osa('tell application "System Events" to keystroke "w" using command down')
            return "Closed active window/tab."
        if "fullscreen" in action:
            _osa('tell application "System Events" to keystroke "f" using {control down, command down}')
            return "Toggled fullscreen."
        return "Mac settings module is active. Try volume, mute, dark mode, screenshot, lock, close window, or fullscreen."
    except Exception as e:
        return f"computer_settings failed: {e}. Enable Accessibility/Automation permissions."
