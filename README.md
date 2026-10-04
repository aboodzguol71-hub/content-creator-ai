# منشئ المحتوى الذكي

مشروع عربي خفيف ومناسب للأجهزة المنزلية الاقتصادية، يهدف إلى:
- توليد نصوص عربية جذابة
- تحويل النص إلى صوت عربي محلي
- إنشاء فيديو قصير من محتوى عربي
- إعداد نشر محتوى على منصات مثل TikTok وInstagram وYouTube Shorts
- تشغيل كامل محليًا دون الاعتماد على خدمات باهظة الثمن

## المزايا
- يدعم العربية
- يعمل محليًا عبر Ollama
- مناسب لRAM 8GB
- يستخدم FFmpeg وTTS محلي
- نموذج مبسط وسهل التوسعة

## البنية

```text
smart-content-creator/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   ├── tts_service.py
│   │   ├── video_service.py
│   │   └── social_service.py
│   └── output/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── LICENSE
```

## المتطلبات الأساسية
- Python 3.10+
- Node.js 18+
- FFmpeg
- Ollama
- TTS محلي (Piper أو espeak-ng)
- ذاكرة RAM 8GB بما يكفي لتشغيل نسخ خفيفة من النماذج المحلية

## التثبيت السريع

### 1) تثبيت Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull qwen2.5:7b
```

### 2) تثبيت FFmpeg وTTS

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y ffmpeg espeak-ng
```

### 3) إعداد الـ Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) إعداد الـ Frontend

```bash
cd frontend
python3 -m http.server 8080
```

## تشغيل التطبيق

### Backend API

```bash
cd backend
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

افتح المتصفح على:
```text
http://localhost:8080
```

## استخدام التطبيق

1. اكتب موضوع المحتوى العربي في الحقل
2. اختر أسلوب التهيئة: إعلاني / تعليمي / تسويقي / قصصي
3. اختر منصة النشر: TikTok / Instagram / YouTube Shorts
4. اضغط على إنشاء محتوى
5. سيتم إنشاء:
   - نص عربي
   - صوت عربي
   - فيديو قصير
   - اقتراحات للنشر

## مثال طلب API

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "فوائد العمل الحر للأشخاص الشباب",
    "tone": "إعلامي",
    "platform": "YouTube Shorts",
    "language": "ar"
  }'
```

## ملاحظات حول الأداء

لأداء جيد على جهاز منزلي اقتصادي:
- استخدم نموذج صغير مثل qwen2.5:7b أو llama3.1:8b
- تجنب إنشاء فيديوهات طويلة جدًا
- ابتعد عن معالجة الصور المتقدمة أثناء المرحلة الأولى
- استخدم فيديوات 15-30 ثانية فقط في البداية

## الملفات المهمة
- `backend/app.py`: نقطة الدخول
- `backend/services/llm_service.py`: توليد النص العربي
- `backend/services/tts_service.py`: توليد الصوت العربي
- `backend/services/video_service.py`: إنشاء الفيديو
- `backend/services/social_service.py`: إعداد النصوص للنشر
- `frontend/index.html`: واجهة سهلة

## المرحلة القادمة
- دعم توليد صور من خلال Stable Diffusion محلي
- دعم نماذج عربية متخصصة
- نشر مباشر إلى القنوات
- نظام جدولة المحتوى

## الترخيص
MIT
