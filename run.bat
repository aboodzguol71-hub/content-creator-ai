@echo off
REM سكريبت تشغيل تطبيق منشئ المحتوى الذكي على Windows
REM Smart Content Creator - Windows Run Script

echo ==========================================
echo منشئ المحتوى الذكي - برنامج التشغيل
echo ==========================================
echo.

if not exist "venv" (
    echo [!] البيئة المحلية غير موجودة
    echo يرجى تشغيل install.bat أولاً
    pause
    exit /b 1
)

echo [*] تفعيل البيئة المحلية...
call venv\Scripts\activate.bat

echo [OK] البيئة المحلية مفعلة
echo.

echo ==========================================
echo اختر الخيار:
echo ==========================================
echo 1) تشغيل الخادم الخلفي (Backend) فقط
echo 2) تشغيل تطبيق سطح المكتب (Desktop GUI)
echo 3) تشغيل كلا الخيارين
echo.
set /p choice=اختيارك (1/2/3): 

if "%choice%"=="1" (
    echo.
    echo [*] تشغيل الخادم الخلفي...
    cd backend
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
) else if "%choice%"=="2" (
    echo.
    echo [*] تشغيل تطبيق سطح المكتب...
    python desktop\app.py
) else if "%choice%"=="3" (
    echo.
    echo [*] تشغيل الخادم الخلفي في الخلفية...
    cd backend
    start cmd /k "uvicorn app:app --host 0.0.0.0 --port 8000"
    cd ..
    timeout /t 2 /nobreak
    echo.
    echo [*] تشغيل تطبيق سطح المكتب...
    python desktop\app.py
) else (
    echo [!] اختيار غير صحيح
    pause
    exit /b 1
)
