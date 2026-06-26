import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQ = ROOT / "requirements.txt"

def run(cmd, *, check=True):
    print("$", " ".join(map(str, cmd)))
    return subprocess.run(cmd, check=check)

print("Installing JARVIS requirements for macOS...")

if platform.system() == "Darwin":
    if shutil.which("brew") is None:
        print("\n⚠️ Homebrew not found. Install it first if sounddevice fails:")
        print("   https://brew.sh")
    else:
        print("Installing PortAudio using Homebrew...")
        run(["brew", "install", "portaudio"], check=False)

run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
run([sys.executable, "-m", "pip", "install", "-r", str(REQ)])

print("Installing Playwright browsers...")
run([sys.executable, "-m", "playwright", "install"], check=False)

print("\n✅ Setup complete!")
print("Run: python3 main.py")
