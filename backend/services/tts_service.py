import os
import shutil
import subprocess
from pathlib import Path

from backend.config import OUTPUT_DIR


def generate_audio(script: str) -> str:
    output_file = OUTPUT_DIR / "voice.wav"

    if shutil.which("piper"):
        # مثال: نموذج عربي إذا كان مثبتًا، أو استخدام نموذج افتراضي موجود
        piper_model = os.getenv("PIPER_MODEL", "")
        if piper_model:
            subprocess.run(
                ["piper", "--model", piper_model, "--output_file", str(output_file)],
                input=script,
                text=True,
                check=False,
            )
            if output_file.exists():
                return str(output_file)

    if shutil.which("espeak-ng"):
        with open(OUTPUT_DIR / "temp_text.txt", "w", encoding="utf-8") as f:
            f.write(script)
        subprocess.run(
            ["espeak-ng", "-w", str(output_file), "-f", str(OUTPUT_DIR / "temp_text.txt")],
            check=False,
        )
        if output_file.exists():
            return str(output_file)

    # fallback: إنشاء ملف صوتي فارغ لاختبار التشغيل
    with open(output_file, "wb") as f:
        f.write(b"\x00")
    return str(output_file)
