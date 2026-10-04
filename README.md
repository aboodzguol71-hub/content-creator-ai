# منشئ المحتوى الذكي - Smart Content Creator AI

**تطبيق عربي احترافي لتوليد المحتوى بالذكاء الاصطناعي**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/status-active-green.svg)](#)

---

## 📋 نظرة عامة

تطبيق شامل لتوليد محتوى عربي احترافي تلقائياً:
- 📝 **توليد نصوص عربية** بأساليب مختلفة
- 🔊 **تحويل النص إلى صوت عربي** محلي
- 🎬 **إنشاء فيديوهات قصيرة** (15-30 ثانية)
- 📱 **خطط نشر** على TikTok و Instagram و YouTube Shorts
- 💻 **واجهة سطح مكتب** سهلة وجميلة
- ⚡ **تشغيل محلي 100%** بدون خدمات سحابية
- 💰 **مناسب للأجهزة الاقتصادية** (8GB RAM كافي)

---

## 🎯 المميزات الرئيسية

✅ **عربي بالكامل** - واجهة وكود وآلات ذكية
✅ **لا يحتاج إنترنت دائم** - تشغيل محلي آمن
✅ **AI محلي** - Ollama + Qwen2.5 للعربية
✅ **TTS محلي** - espeak-ng و Piper للصوت العربي
✅ **GUI احترافية** - PyQt6 مع تصميم داكن حديث
✅ **تثبيت بأمر واحد** - Windows و Linux و macOS
✅ **مخرجات متعددة** - نص + صوت + فيديو + خطة نشر
✅ **خفيف الوزن** - استهلاك منخفض للموارد

---

## 📊 متطلبات النظام

| المتطلب | الحد الأدنى | الموصى به |
|---------|-----------|----------|
| **RAM** | 8 GB | 16 GB |
| **CPU** | رباعي النوى | سداسي النوى+ |
| **Storage** | 50 GB | 100 GB |
| **Python** | 3.10+ | 3.11+ |
| **OS** | Windows 10+ / Ubuntu 20.04+ / macOS 12+ | - |

---

## 🚀 التثبيت السريع

### **Windows (حقق النقر)**
```batch
install.bat
```

### **Linux / macOS (سطر واحد)**
```bash
chmod +x install.sh && ./install.sh
```

### **الخطوات اليدوية (اختياري)**

**1. تثبيت المتطلبات:**
```bash
# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv ffmpeg espeak-ng

# macOS
brew install python@3.11 ffmpeg espeak-ng

# Windows
# حمل من: https://www.python.org/downloads/
# FFmpeg: https://ffmpeg.org/download.html
```

**2. تثبيت Ollama:**
```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# حمل من: https://ollama.com/download
```

**3. سحب النموذج:**
```bash
ollama pull qwen2.5:7b
```

**4. إعداد المشروع:**
```bash
git clone https://github.com/aboodzguol71-hub/content-creator-ai.git
cd content-creator-ai
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

---

## 🎮 التشغيل

### **الطريقة الأولى: استخدام السكربت**

**Linux/macOS:**
```bash
./run.sh
```

**Windows:**
```batch
run.bat
```

### **الطريقة الثانية: التشغيل اليدوي**

**نافذة 1 - تشغيل Ollama:**
```bash
ollama serve
```

**نافذة 2 - تشغيل الخادم:**
```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**نافذة 3 - تشغيل التطبيق:**
```bash
cd ..
source venv/bin/activate
python desktop/app.py
```

---

## 💻 استخدام التطبيق

### **الواجهة الرسومية (Desktop)**

1. **اكتب موضوع المحتوى**
   - مثال: "فوائد الرياضة الصباحية"

2. **اختر الأسلوب**
   - إعلامي / تعليمي / تسويقي / قصصي

3. **اختر المنصة**
   - YouTube Shorts / Instagram Reels / TikTok

4. **حدد المدة**
   - 15-30 ثانية

5. **اضغط "إنشاء محتوى"**
   - سينتظر 1-2 دقيقة

6. **شاهد النتائج**
   - النص العربي
   - الصوت المُوَلّد
   - الفيديو النهائي
   - خطة النشر

### **API (للمطورين)**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "فوائد القراءة",
    "tone": "تعليمي",
    "platform": "YouTube Shorts",
    "language": "ar",
    "duration_seconds": 20
  }'
```

**الرد:**
```json
{
  "status": "success",
  "script": "النص العربي...",
  "audio": "path/to/voice.wav",
  "video": "path/to/final_video.mp4",
  "social_plan": {
    "platform": "YouTube Shorts",
    "hook": "خطاف الفيديو...",
    "hashtags": ["#تعليمي", "#محتوى", ...],
    "recommended_length": "15-30 ثانية"
  }
}
```

---

## 📁 هيكل المشروع

```
content-creator-ai/
├── backend/                 # API والخوارزميات
│   ├── app.py              # تطبيق FastAPI الرئيسي
│   ├── config.py           # الإعدادات
│   ├── requirements.txt     # مكتبات Python
│   ├── services/           # الخدمات
│   │   ├── llm_service.py       # توليد النصوص
│   │   ├── tts_service.py       # توليد الصوت
│   │   ├── video_service.py     # إنشاء الفيديو
│   │   └── social_service.py    # خطط النشر
│   └── output/             # المخرجات المُنتجة
├── desktop/                # تطبيق سطح المكتب
│   └── app.py             # واجهة PyQt6
├── frontend/              # واجهة الويب (اختياري)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── install.sh             # سكربت التثبيت (Linux/macOS)
├── install.bat            # سكربت التثبيت (Windows)
├── run.sh                 # سكربت التشغيل (Linux/macOS)
├── run.bat                # سكربت التشغيل (Windows)
├── .env.example           # مثال الإعدادات
├── docker-compose.yml     # تكوين Docker
├── LICENSE                # رخصة MIT
└── README.md             # هذا الملف
```

---

## 🔧 الإعدادات

**نسخ الملف:**
```bash
cp .env.example .env
```

**تعديل `.env`:**
```env
# Ollama
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5:7b

# TTS
DEFAULT_VOICE=female
PIPER_MODEL=ar_JO.voice

# العام
DEFAULT_TONE=إعلامي
DEFAULT_PLATFORM=YouTube Shorts
```

---

## 📚 دليل الاستخدام المتقدم

### **تغيير نموذج AI**

في `.env`:
```env
OLLAMA_MODEL=mistral-nemo
```

النماذج المدعومة:
- `qwen2.5:7b` (الأفضل للعربية)
- `llama3.1:8b`
- `mistral-nemo`
- `neural-chat:7b`

### **تفعيل TTS المحلي**

```bash
# Piper (الأفضل)
pip install piper-tts
ollama pull piper

# أو espeak-ng
sudo apt-get install espeak-ng
```

### **إنشاء فيديوهات بدقة أعلى**

عدّل في `backend/services/video_service.py`:
```python
quality = "high"  # تغيير من "medium"
```

---

## ⚡ نصائح للأداء الأفضل

1. **استخدم جهاز بـ 8GB+ RAM**
2. **شغّل Ollama مسبقاً** (أو استخدم `ollama serve` في نافذة)
3. **لا تفتح تطبيقات أخرى** أثناء التوليد
4. **استخدم مواضيع قصيرة** (5-10 كلمات)
5. **اختر مدة فيديو قصيرة** (15-20 ثانية) للأداء الأسرع

---

## 🐛 حل المشاكل

### **الخطأ: "Failed to connect to Ollama"**
```bash
# تأكد من تشغيل Ollama
ollama serve

# أو في نافذة منفصلة
ps aux | grep ollama
```

### **الخطأ: "FFmpeg not found"**
```bash
# Linux
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### **الخطأ: "PyQt6 not installed"**
```bash
source venv/bin/activate
pip install PyQt6
```

### **الخطأ: "No module named backend"**
```bash
# تأكد من وجود __init__.py
touch backend/__init__.py
touch backend/services/__init__.py
```

---

## 📊 أمثلة على الاستخدام

### **مثال 1: محتوى تعليمي**
```
الموضوع: أهمية النوم المنتظم
الأسلوب: تعليمي
المنصة: YouTube Shorts
النتيجة: فيديو تعليمي احترافي (20 ثانية)
```

### **مثال 2: محتوى تسويقي**
```
الموضوع: منتج العناية بالبشرة
الأسلوب: تسويقي
المنصة: Instagram Reels
النتيجة: فيديو ترويجي جذاب (15 ثانية)
```

### **مثال 3: قصة قصيرة**
```
الموضوع: قصة نجاح
الأسلوب: قصصي
المنصة: TikTok
النتيجة: فيديو قصصي مشوق (30 ثانية)
```

---

## 🤝 المساهمة

نرحب بالمساهمات! يمكنك:
1. Fork المشروع
2. إنشاء فرع جديد: `git checkout -b feature/amazing-feature`
3. Commit التغييرات: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. فتح Pull Request

---

## 📄 الرخصة

هذا المشروع مرخص تحت [MIT License](LICENSE)

---

## 📞 التواصل والدعم

- **Issues**: https://github.com/aboodzguol71-hub/content-creator-ai/issues
- **Discussions**: https://github.com/aboodzguol71-hub/content-creator-ai/discussions

---

## 🌟 إذا أعجبك المشروع

لا تنسى إضافة ⭐ للمستودع!

---

**آخر تحديث**: 2026-10-04
**الإصدار**: 1.0.0
**الحالة**: ✅ نشط وقيد التطوير
