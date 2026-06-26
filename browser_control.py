from __future__ import annotations

import subprocess
import urllib.parse


def _browser_name(raw: str | None) -> str:
    b = (raw or "safari").lower().strip()
    return {
        "safari": "Safari",
        "chrome": "Google Chrome",
        "edge": "Microsoft Edge",
        "firefox": "Firefox",
        "brave": "Brave Browser",
        "opera": "Opera",
        "operagx": "Opera GX",
        "vivaldi": "Vivaldi",
    }.get(b, raw or "Safari")


def _osa(script: str) -> str:
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r.stdout.strip()


def _open_url(url: str, browser: str) -> None:
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    subprocess.run(["open", "-a", browser, url], check=False)


def browser_control(*args, **kwargs):
    parameters = kwargs.get("parameters") or (args[0] if args else {}) or {}
    action = str(parameters.get("action", "go_to")).lower().strip()
    browser = _browser_name(parameters.get("browser"))
    try:
        if action in ("go_to", "new_tab"):
            url = parameters.get("url") or parameters.get("text")
            if not url:
                return "No URL provided."
            _open_url(str(url), browser)
            return f"Opened {url} in {browser}."

        if action == "search":
            q = str(parameters.get("query") or parameters.get("text") or "")
            if not q:
                return "No search query provided."
            engine = str(parameters.get("engine", "google")).lower()
            base = {
                "google": "https://www.google.com/search?q=",
                "bing": "https://www.bing.com/search?q=",
                "duckduckgo": "https://duckduckgo.com/?q=",
                "yandex": "https://yandex.com/search/?text=",
            }.get(engine, "https://www.google.com/search?q=")
            url = base + urllib.parse.quote_plus(q)
            _open_url(url, browser)
            return f"Searched for {q} in {browser}."

        if action == "get_url":
            if browser == "Safari":
                return _osa('tell application "Safari" to get URL of front document')
            return _osa(f'tell application "{browser}" to get URL of active tab of front window')

        if action in ("back", "forward", "reload"):
            key = {"back": "[", "forward": "]", "reload": "r"}[action]
            modifier = "command"
            _osa(f'tell application "{browser}" to activate\ntell application "System Events" to keystroke "{key}" using {modifier} down')
            return f"Browser {action} done."

        if action == "close_tab":
            _osa(f'tell application "{browser}" to activate\ntell application "System Events" to keystroke "w" using command down')
            return "Closed browser tab."

        if action == "type":
            text = str(parameters.get("text", ""))
            _osa(f'tell application "{browser}" to activate')
            subprocess.run(["pbcopy"], input=text, text=True, check=False)
            _osa('tell application "System Events" to keystroke "v" using command down')
            return "Typed in browser."

        if action == "press":
            key = str(parameters.get("key", "return")).lower()
            if key == "enter": key = "return"
            _osa(f'tell application "{browser}" to activate\ntell application "System Events" to key code 36') if key == "return" else _osa(f'tell application "System Events" to keystroke "{key}"')
            return f"Pressed {key} in browser."

        return f"Browser action {action} needs screen control. Use computer_control click/type after screen_process screenshot."
    except Exception as e:
        return f"browser_control failed: {e}. Enable Automation permission for Terminal/Python to control {browser}."
