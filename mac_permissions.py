print("""
JARVIS macOS permissions checklist

Open: System Settings > Privacy & Security

Turn ON for Terminal, Python, or VS Code:
1. Microphone       - voice input
2. Accessibility    - mouse/keyboard control
3. Screen Recording - seeing your screen / screenshots
4. Automation       - controlling Safari, Finder, System Events

After changing permissions, fully quit Terminal/VS Code and open it again.

Test commands:
python3 mic_debug.py
python3 -c "import pyautogui; print(pyautogui.position())"
python3 -c "import subprocess; subprocess.run(['screencapture','-x','screen_test.png']); print('screen_test.png saved')"
""")
