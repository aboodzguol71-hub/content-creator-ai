@echo off
REM منشئ المحتوى الذكي - سكريبت التثبيت على Windows
REM Smart Content Creator - Windows Installation Script

echo ==========================================
echo منشئ المحتوى الذكي - برنامج التثبيت
echo Smart Content Creator - Installation
echo ==========================================
echo.

REM التحقق من Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python غير مثبت
    echo يرجى تحميل Python من: https://www.python.org/downloads/
    echo تأكد من تفعيل "Add Python to PATH" أثناء التثبيت
    pause
    exit /b 1
) else (
    echo [OK] Python مثبت
)

REM التحقق من FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [!] FFmpeg غير مثبت
    echo يرجى تحميل FFmpeg من: https://ffmpeg.org/download.html
    echo أو استخدم Chocolatey: choco install ffmpeg
    pause
) else (
    echo [OK] FFmpeg مثبت
)

REM التحقق من Ollama
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [!] Ollama غير مثبت
    echo يرجى تحميل Ollama من: https://ollama.com/download
    pause
) else (
    echo [OK] Ollama مثبت
)

echo.
echo [*] إنشاء بيئة Python المحلية...

if not exist "venv" (
    python -m venv venv
    echo [OK] تم إنشاء venv
) else (
    echo [OK] venv موجود بالفعل
)

echo.
echo [*] تفعيل البيئة المحلية...
call venv\Scripts\activate.bat

echo [*] تحديث pip...
python -m pip install --upgrade pip setuptools wheel

echo [*] تثبيت مكتبات Python...
if exist "backend\requirements.txt" (
    pip install -r backend\requirements.txt
    echo [OK] تم تثبيت جميع المكتبات
) else (
    echo [!] لم يتم العثور على backend\requirements.txt
)

echo.
echo [*] إنشاء مجلدات المشروع...
if not exist "backend\output" mkdir backend\output
if not exist "logs" mkdir logs
echo [OK] تم إنشاء المجلدات

echo.
echo [*] إنشاء ملف .env...
if not exist ".env" (
    copy .env.example .env
    echo [OK] تم إنشاء .env
) else (
    echo [OK] .env موجود بالفعل
)

echo.
echo ==========================================
echo تم التثبيت بنجاح!
echo ==========================================
echo.
echo الخطوات التالية:
echo.
echo 1. تشغيل Ollama (في نافذة منفصلة):
echo    ollama serve
echo.
echo 2. تشغيل الخادم الخلفي (في نافذة منفصلة):
echo    venv\Scripts\activate.bat
echo    cd backend
echo    uvicorn app:app --reload --host 0.0.0.0 --port 8000
echo.
echo 3. تشغيل تطبيق سطح المكتب (في نافذة منفصلة):
echo    venv\Scripts\activate.bat
echo    python desktop\app.py
echo.
echo أو استخدم:
echo    run.bat
echo.
pause
