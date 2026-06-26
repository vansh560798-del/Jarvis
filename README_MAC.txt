JARVIS macOS run guide

1) Open Terminal in this folder.
2) Create a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate

3) Install requirements:
   python3 setup.py

4) Start:
   python3 main.py

On first launch, paste your Gemini API key into the setup screen.

If sounddevice fails on Mac, install Homebrew, then run:
   brew install portaudio
   pip install sounddevice

If macOS blocks mic/screen controls, allow Terminal or Python in:
System Settings > Privacy & Security > Microphone / Accessibility / Screen Recording.

MIC FIX:
1. Give mic permission:
   System Settings -> Privacy & Security -> Microphone -> enable Terminal / Python / VS Code.
   Restart Terminal after changing this.
2. Run: python3 mic_debug.py
3. Speak for 5 seconds. If the level moves, run: python3 main.py
4. To force a mic device manually:
   JARVIS_MIC_DEVICE=0 python3 main.py
