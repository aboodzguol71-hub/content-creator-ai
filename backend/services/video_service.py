import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from backend.config import OUTPUT_DIR


def generate_video(script: str, audio_path: str, platform: str, duration_seconds: int = 20) -> str:
    bg_path = OUTPUT_DIR / "background.png"
    create_background_image(bg_path, script, platform)
    output_video = OUTPUT_DIR / "final_video.mp4"

    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg غير مثبت. يرجى تثبيته قبل إنشاء الفيديو.")

    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        str(bg_path),
        "-i",
        str(audio_path),
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-c:a",
        "aac",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        str(output_video),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"فشل إنشاء الفيديو: {result.stderr or result.stdout or 'خطأ غير معروف'}")
    return str(output_video)


def create_background_image(path: Path, script: str, platform: str) -> None:
    img = Image.new("RGB", (1280, 720), color=(17, 24, 39))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    title = platform[:25]
    draw.rectangle((60, 60, 1220, 660), outline=(79, 70, 229), width=3)
    draw.text((90, 120), title, fill=(255, 255, 255), font=font)

    lines = wrap_text(script, 28)
    y = 240
    for line in lines[:6]:
        draw.text((90, y), line, fill=(203, 213, 225), font=sub_font)
        y += 48

    img.save(path)


def wrap_text(text: str, max_chars: int):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if not word:
            continue
        if len(current) + len(word) + 1 <= max_chars:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
