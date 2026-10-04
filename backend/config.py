import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "backend" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
DEFAULT_TONE = os.getenv("DEFAULT_TONE", "إعلامي")
DEFAULT_PLATFORM = os.getenv("DEFAULT_PLATFORM", "YouTube Shorts")
