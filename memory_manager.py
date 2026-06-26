from __future__ import annotations
import json
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parent / "memory.json"

def load_memory() -> dict:
    try:
        if MEMORY_FILE.exists():
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

def update_memory(data: dict) -> None:
    memory = load_memory()
    for category, values in (data or {}).items():
        if isinstance(values, dict):
            memory.setdefault(category, {}).update(values)
        else:
            memory[category] = values
    MEMORY_FILE.write_text(json.dumps(memory, indent=2), encoding="utf-8")

def format_memory_for_prompt(memory: dict) -> str:
    if not memory:
        return ""
    return "[MEMORY]\n" + json.dumps(memory, ensure_ascii=False, indent=2)
