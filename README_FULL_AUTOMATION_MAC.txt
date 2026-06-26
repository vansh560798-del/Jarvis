JARVIS FULL AUTOMATION MAC BUILD

Run:
python3 setup.py
python3 mac_permissions.py
python3 mic_debug.py
python3 main.py

You MUST allow macOS permissions:
System Settings > Privacy & Security:
- Microphone
- Accessibility
- Screen Recording
- Automation

Enable them for whichever app runs Jarvis:
Terminal, Python, or VS Code.

What works in this build:
- open Safari/Chrome/apps
- open websites and search web
- basic Safari/Chrome tab actions
- keyboard typing, paste, hotkeys
- mouse click, double click, right click, scroll, move
- screenshots / screen capture
- volume, mute, dark mode, fullscreen, close window

Examples to say:
- Open Safari
- Search YouTube for lo-fi music
- Take screenshot of my screen
- Click at 500 400
- Type hello world
- Press enter
- Set volume to 60
- Turn on dark mode

Mac safety note:
Move your mouse to the top-left corner to emergency-stop PyAutoGUI actions.
