#!/bin/bash

# سكريبت تشغيل تطبيق منشئ المحتوى الذكي
# Smart Content Creator - Run Script

set -e

echo "=========================================="
echo "منشئ المحتوى الذكي - برنامج التشغيل"
echo "=========================================="
echo ""

# الألوان
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# تفعيل البيئة المحلية
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[!] البيئة المحلية غير موجودة. يرجى تشغيل install.sh أولاً${NC}"
    exit 1
fi

source venv/bin/activate

echo -e "${GREEN}[✓] البيئة المحلية مفعلة${NC}"
echo ""

# التحقق من Ollama
echo -e "${BLUE}[*] التحقق من Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}[!] Ollama غير مثبت أو غير متاح في PATH${NC}"
    echo "تأكد من تثبيت Ollama من: https://ollama.com"
else
    # محاولة التحقق من حالة Ollama
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}[!] Ollama غير قيد التشغيل${NC}"
        echo -e "${BLUE}[*] ابدأ Ollama في نافذة منفصلة بـ: ollama serve${NC}"
    else
        echo -e "${GREEN}[✓] Ollama قيد التشغيل${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "اختر الخيار:"
echo "=========================================="
echo "1) تشغيل الخادم الخلفي (Backend) فقط"
echo "2) تشغيل تطبيق سطح المكتب (Desktop GUI)"
echo "3) تشغيل كلا الخيارين (في نوافذ منفصلة)"
echo ""
read -p "اختيارك (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}[*] تشغيل الخادم الخلفي...${NC}"
        cd backend
        uvicorn app:app --reload --host 0.0.0.0 --port 8000
        ;;
    2)
        echo ""
        echo -e "${BLUE}[*] تشغيل تطبيق سطح المكتب...${NC}"
        python desktop/app.py
        ;;
    3)
        echo ""
        echo -e "${BLUE}[*] تشغيل الخادم الخلفي في الخلفية...${NC}"
        cd backend
        uvicorn app:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
        BACKEND_PID=$!
        echo -e "${GREEN}[✓] الخادم الخلفي يعمل (PID: $BACKEND_PID)${NC}"
        
        cd ..
        sleep 2
        
        echo -e "${BLUE}[*] تشغيل تطبيق سطح المكتب...${NC}"
        python desktop/app.py
        
        echo ""
        echo -e "${BLUE}[*] إيقاف الخادم الخلفي...${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        ;;
    *)
        echo -e "${YELLOW}[!] اختيار غير صحيح${NC}"
        exit 1
        ;;
esac
