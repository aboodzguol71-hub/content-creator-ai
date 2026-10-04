import json
import os
import requests

from backend.config import OLLAMA_URL, OLLAMA_MODEL


def generate_script(topic: str, tone: str, platform: str, language: str = "ar") -> str:
    prompt = f"""
أنت منشئ محتوى عربي محترف ومبدع.
اللغة: {language}
الموضوع: {topic}
الأسلوب: {tone}
المنصة: {platform}

اكتب نصًا عربيًا جذابًا قصيرًا جدًا مناسبًا لفيديو قصير. التنسيق المطلوب:
1. عنوان جذاب
2. مقدمة قصيرة
3. نص رئيسي من 3 إلى 5 جمل
4. خاتمة قصيرة
5. لا تستخدم أكثر من 120 كلمة
6. استخدم أسلوب طبيعي ومباشر مناسب للمنصة
7. اجعلها قابلة للتسليم إلى صوت عربي

النص:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7},
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "").strip()
        if text:
            return text
    except Exception:
        pass

    return build_fallback_script(topic, tone, platform)


def build_fallback_script(topic: str, tone: str, platform: str) -> str:
    return f"""
عنوان: {topic}

في عالم اليوم، أصبح موضوع {topic} مهمًا جدًا لكل من يريد التقدم والنجاح.
هذا المحتوى يساعدك على فهم الفكرة الأساسية بشكل سريع ومباشر.
إذا كنت تريد تعلم المزيد، فابدأ اليوم بخطوة صغيرة ومستمرة.
النجاح يبدأ من الفهم، ومن ثم التنفيذ.

# {platform}
# {tone}
""".strip()
