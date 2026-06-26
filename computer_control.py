from __future__ import annotations

import subprocess
import time
from pathlib import Path


def _p():
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
    return pyautogui


def _copy_to_clipboard(text: str) -> None:
    subprocess.run(["pbcopy"], input=text, text=True, check=False)


def _paste_from_clipboard() -> str:
    r = subprocess.run(["pbpaste"], capture_output=True, text=True, check=False)
    return r.stdout


def computer_control(*args, **kwargs):
    parameters = kwargs.get("parameters") or (args[0] if args else {}) or {}
    action = str(parameters.get("action", "")).lower().strip()
    try:
        pg = _p()
        if action in ("type", "smart_type"):
            text = str(parameters.get("text", ""))
            if parameters.get("clear_first"):
                pg.hotkey("command", "a")
            # paste is faster and works with symbols better than typing key-by-key
            _copy_to_clipboard(text)
            pg.hotkey("command", "v")
            return "Typed text."

        if action == "click":
            x, y = int(parameters.get("x", 0)), int(parameters.get("y", 0))
            pg.click(x, y)
            return f"Clicked at {x}, {y}."

        if action == "double_click":
            x, y = int(parameters.get("x", 0)), int(parameters.get("y", 0))
            pg.doubleClick(x, y)
            return f"Double-clicked at {x}, {y}."

        if action == "right_click":
            x, y = int(parameters.get("x", 0)), int(parameters.get("y", 0))
            pg.rightClick(x, y)
            return f"Right-clicked at {x}, {y}."

        if action == "move":
            x, y = int(parameters.get("x", 0)), int(parameters.get("y", 0))
            pg.moveTo(x, y, duration=0.15)
            return f"Moved mouse to {x}, {y}."

        if action == "hotkey":
            keys = str(parameters.get("keys", "")).replace("+", ",").split(",")
            keys = [k.strip().lower().replace("cmd", "command").replace("ctrl", "control") for k in keys if k.strip()]
            if not keys:
                return "No hotkey keys provided."
            pg.hotkey(*keys)
            return "Pressed hotkey " + "+".join(keys) + "."

        if action == "press":
            key = str(parameters.get("key", ""))
            if not key:
                return "No key provided."
            pg.press(key.lower())
            return f"Pressed {key}."

        if action == "scroll":
            direction = str(parameters.get("direction", "down")).lower()
            amount = int(parameters.get("amount", 5))
            pg.scroll(amount if direction == "up" else -amount)
            return f"Scrolled {direction}."

        if action == "copy":
            pg.hotkey("command", "c")
            time.sleep(0.1)
            return _paste_from_clipboard() or "Copied selection."

        if action == "paste":
            text = parameters.get("text")
            if text is not None:
                _copy_to_clipboard(str(text))
            pg.hotkey("command", "v")
            return "Pasted."

        if action == "clear_field":
            pg.hotkey("command", "a")
            pg.press("backspace")
            return "Cleared field."

        if action == "wait":
            seconds = float(parameters.get("seconds", 1))
            time.sleep(max(0, min(seconds, 30)))
            return f"Waited {seconds} seconds."

        if action == "screenshot":
            path = str(parameters.get("path") or (Path.home() / "Desktop" / "jarvis_screenshot.png"))
            img = pg.screenshot()
            img.save(path)
            return f"Screenshot saved to {path}."

        if action == "focus_window":
            title = str(parameters.get("title", ""))
            if title:
                subprocess.run(["osascript", "-e", f'tell application "{title}" to activate'], check=False)
                return f"Focused {title}."
            return "No window/app title provided."

        return f"Unknown computer_control action: {action}."
    except Exception as e:
        return f"computer_control failed: {e}. On Mac, enable Accessibility and Screen Recording for Terminal/Python."
