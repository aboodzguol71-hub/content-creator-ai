#!/bin/bash
# سكربت التثبيت الشامل لـ منشئ المحتوى الذكي
# Smart Content Creator - Complete Installation Script

set -e

echo "=========================================="
echo "منشئ المحتوى الذكي - برنامج التثبيت"
echo "Smart Content Creator - Installation"
echo "=========================================="
echo ""

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[*]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

# كشف النظام
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "linux")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "نظام تشغيل غير مدعوم"
    exit 1
fi

print_status "النظام المكتشف: $OS"
echo ""

# 1. المتطلبات الأساسية
print_status "التحقق من المتطلبات الأساسية..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 غير مثبت"
    if [ "$OS" = "linux" ]; then
        if [ "$DISTRO" = "Ubuntu" ] || [ "$DISTRO" = "Debian" ]; then
            sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
        fi
    fi
else
    print_success "Python 3 مثبت"
fi

if ! command -v ffmpeg &> /dev/null; then
    print_warning "FFmpeg غير مثبت. جاري التثبيت..."
    if [ "$OS" = "linux" ]; then
        [ "$DISTRO" = "Ubuntu" ] || [ "$DISTRO" = "Debian" ] && sudo apt-get install -y ffmpeg
    elif [ "$OS" = "macos" ]; then
        brew install ffmpeg 2>/dev/null || print_warning "استخدم: brew install ffmpeg"
    fi
else
    print_success "FFmpeg مثبت"
fi

if ! command -v espeak-ng &> /dev/null; then
    print_warning "espeak-ng غير مثبت. جاري التثبيت..."
    if [ "$OS" = "linux" ]; then
        [ "$DISTRO" = "Ubuntu" ] || [ "$DISTRO" = "Debian" ] && sudo apt-get install -y espeak-ng
    elif [ "$OS" = "macos" ]; then
        brew install espeak-ng 2>/dev/null || print_warning "استخدم: brew install espeak-ng"
    fi
else
    print_success "espeak-ng مثبت"
fi

echo ""
print_status "تثبيت Ollama..."

if ! command -v ollama &> /dev/null; then
    if [ "$OS" = "linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh 2>/dev/null || print_warning "فشل تثبيت Ollama. ثبّته يدويًا من https://ollama.com"
    elif [ "$OS" = "macos" ]; then
        print_warning "ثبّت Ollama من https://ollama.com/download"
    fi
else
    print_success "Ollama مثبت"
fi

echo ""
echo "=========================================="
print_status "تجهيز بيئة Python..."
echo "=========================================="

if [ ! -d "venv" ]; then
    print_status "إنشاء بيئة Python..."
    python3 -m venv venv
    print_success "تم إنشاء البيئة"
fi

print_status "تفعيل البيئة..."
source venv/bin/activate

print_status "تحديث pip..."
pip install --upgrade pip setuptools wheel -q

print_status "تثبيت المكتبات..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt -q
    print_success "تم تثبيت جميع المكتبات"
fi

echo ""
echo "=========================================="
print_status "إعداد المشروع..."
echo "=========================================="

mkdir -p backend/output logs
print_success "تم إنشاء المجلدات"

if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || print_warning ".env.example غير موجود"
    print_success "تم إنشاء ملف .env"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✓ تم التثبيت بنجاح!${NC}"
echo "=========================================="
echo ""
echo "الخطوات التالية:"
echo ""
echo "1️⃣  شغّل Ollama في نافذة منفصلة:"
echo -e "   ${BLUE}ollama serve${NC}"
echo ""
echo "2️⃣  ثم استخدم السكربت:"
echo -e "   ${BLUE}./run.sh${NC}"
echo ""
echo "أو شغّل يدويًا:"
echo ""
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}python desktop/app.py${NC}"
echo ""
