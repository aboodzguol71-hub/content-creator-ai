#!/bin/bash
# سكربت تشغيل منشئ المحتوى الذكي بسهولة

set -e

echo "=========================================="
echo "منشئ المحتوى الذكي"
echo "=========================================="
echo ""

if [ ! -d "venv" ]; then
    echo "[!] البيئة المحلية غير موجودة. شغّل install.sh أولاً"
    exit 1
fi

source venv/bin/activate

echo "[*] التحقق من Ollama..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "[!] Ollama غير مشغّل"
    echo "[*] شغّل في نافذة أخرى: ollama serve"
    echo ""
fi

echo "[*] اختر خيارك:"
echo "1) تطبيق سطح المكتب (GUI)"
echo "2) الخادم فقط (Backend)"
echo "3) كليهما"
echo ""
read -p "اختيارك (1/2/3): " choice

case $choice in
    1)
        python desktop/app.py
        ;;
    2)
        cd backend
        uvicorn app:app --reload --host 0.0.0.0 --port 8000
        ;;
    3)
        cd backend
        uvicorn app:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
        sleep 2
        cd ..
        python desktop/app.py
        ;;
    *)
        echo "[!] خيار غير صحيح"
        exit 1
        ;;
esac
