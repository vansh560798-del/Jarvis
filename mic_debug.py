import json
import os
import time
from pathlib import Path

import sounddevice as sd

BASE_DIR = Path(__file__).resolve().parent
SEND_SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024


def select_input_device():
    env_dev = os.environ.get("JARVIS_MIC_DEVICE")
    if env_dev not in (None, ""):
        return int(env_dev) if str(env_dev).isdigit() else env_dev

    cfg_path = BASE_DIR / "config" / "audio_config.json"
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        dev = cfg.get("input_device")
        if dev not in (None, ""):
            return int(dev) if str(dev).isdigit() else dev

    try:
        default_in = sd.default.device[0]
        if default_in is not None and default_in >= 0:
            info = sd.query_devices(default_in)
            if info.get("max_input_channels", 0) > 0:
                return default_in
    except Exception:
        pass

    for i, info in enumerate(sd.query_devices()):
        if info.get("max_input_channels", 0) > 0:
            return i
    return None


def list_mics():
    print("\nAvailable input devices:\n")
    for i, info in enumerate(sd.query_devices()):
        if info.get("max_input_channels", 0) > 0:
            marker = "*" if sd.default.device[0] == i else " "
            print(f"{marker} [{i}] {info.get('name')}  inputs={info.get('max_input_channels')}  default_sr={info.get('default_samplerate')}")


def main():
    list_mics()
    dev = select_input_device()
    if dev is None:
        print("\n❌ No microphone found.")
        return
    info = sd.query_devices(dev)
    print(f"\nUsing mic: [{dev}] {info.get('name')}")
    print("Speak now for 5 seconds...\n")

    peak = 0
    chunks = 0

    def callback(indata, frames, time_info, status):
        nonlocal peak, chunks
        if status:
            print("status:", status)
        data = bytes(indata)
        # int16 little-endian level check without numpy
        vals = memoryview(data).cast('h')
        if vals:
            level = max(abs(x) for x in vals)
            peak = max(peak, level)
            chunks += 1
            bar = "█" * min(40, int(level / 800))
            print(f"level {level:5d} {bar}", end="\r")

    try:
        with sd.RawInputStream(device=dev, samplerate=SEND_SAMPLE_RATE, channels=CHANNELS, dtype="int16", blocksize=CHUNK_SIZE, callback=callback):
            time.sleep(5)
    except Exception as e:
        print(f"\n❌ Mic stream failed: {e}")
        print("Mac fix: System Settings → Privacy & Security → Microphone → enable Terminal/Python/VS Code, then restart Terminal.")
        return

    print("\n")
    if chunks == 0:
        print("❌ Mic opened, but no audio chunks arrived.")
    elif peak < 300:
        print(f"⚠️ Mic is detected but audio is almost silent. Peak={peak}. Check input volume or choose another mic.")
    else:
        print(f"✅ Mic is working. Peak={peak}. Now run: python3 main.py")

    cfg_dir = BASE_DIR / "config"
    cfg_dir.mkdir(exist_ok=True)
    (cfg_dir / "audio_config.json").write_text(json.dumps({"input_device": dev}, indent=2), encoding="utf-8")
    print(f"Saved selected mic to config/audio_config.json: {dev}")


if __name__ == "__main__":
    main()
