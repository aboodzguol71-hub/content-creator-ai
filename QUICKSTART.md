# منشئ المحتوى الذكي - دليل البدء السريع

## ⚡ البدء في 5 دقائق

### الخطوة 1: التثبيت

**Linux/macOS:**
```bash
chmod +x install.sh && ./install.sh
```

**Windows:**
```batch
install.bat
```

### الخطوة 2: تشغيل Ollama

في نافذة منفصلة:
```bash
ollama serve
```

### الخطوة 3: تشغيل التطبيق

**Linux/macOS:**
```bash
./run.sh
```

**Windows:**
```batch
run.bat
```

---

## 🎯 الاستخدام الأساسي

1. اكتب موضوع المحتوى
2. اختر الأسلوب (إعلامي/تعليمي/تسويقي/قصصي)
3. اختر المنصة (YouTube/Instagram/TikTok)
4. اضغط "إنشاء محتوى"
5. انتظر النتائج

---

## 🔧 استكشاف الأخطاء

### Ollama لا يعمل
```bash
ollama pull qwen2.5:7b
ollama serve
```

### FFmpeg غير مثبت
```bash
# Ubuntu
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### PyQt6 غير مثبت
```bash
source venv/bin/activate
pip install PyQt6
```

---

## 📞 الحاجة إلى مساعدة؟

تحقق من [README.md](README.md) للحصول على معلومات أكثر تفصيلاً.
