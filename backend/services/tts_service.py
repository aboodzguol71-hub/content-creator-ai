import os
import shutil
import subprocess
import wave
from pathlib import Path

try:
    from backend.config import OUTPUT_DIR
except ImportError:
    from config import OUTPUT_DIR


def generate_audio(script: str) -> str:
    output_file = OUTPUT_DIR / "voice.wav"

    if shutil.which("piper"):
        piper_model = os.getenv("PIPER_MODEL", "")
        if piper_model:
            subprocess.run(
                ["piper", "--model", piper_model, "--output_file", str(output_file)],
                input=script,
                text=True,
                check=False,
            )
            if output_file.exists() and output_file.stat().st_size > 0:
                return str(output_file)

    if shutil.which("espeak-ng"):
        with open(OUTPUT_DIR / "temp_text.txt", "w", encoding="utf-8") as f:
            f.write(script)
        subprocess.run(
            ["espeak-ng", "-w", str(output_file), "-f", str(OUTPUT_DIR / "temp_text.txt")],
            check=False,
        )
        if output_file.exists() and output_file.stat().st_size > 0:
            return str(output_file)

    # fallback: إنشاء ملف صوت صامت ومناسب لعمليات FFmpeg
    create_silent_wav(output_file)
    return str(output_file)


def create_silent_wav(path):
    """ينشئ ملف WAV صامت وعمل مع FFmpeg دون فشل."""
    sample_rate = 22050
    duration_seconds = 1
    total_frames = sample_rate * duration_seconds

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        silence = b"\x00\x00" * total_frames
        wav_file.writeframes(silence)
