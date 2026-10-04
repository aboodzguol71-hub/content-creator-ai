#!/bin/bash

# منشئ المحتوى الذكي - سكريبت التثبيت الموحد
# Smart Content Creator - Unified Installation Script

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
NC='\033[0m' # No Color

# وظيفة للطباعة الملونة
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# التحقق من نظام التشغيل
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "linux")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "نظام التشغيل غير مدعوم. يرجى استخدام Linux أو macOS"
    exit 1
fi

print_status "نظام التشغيل المكتشف: $OS"
echo ""

# 1. التحقق من المتطلبات الأساسية
print_status "التحقق من المتطلبات الأساسية..."

# Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 غير مثبت"
    if [ "$OS" = "linux" ]; then
        print_status "تثبيت Python 3..."
        if [ "$DISTRO" = "Ubuntu" ] || [ "$DISTRO" = "Debian" ]; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif [ "$DISTRO" = "Fedora" ]; then
            sudo dnf install -y python3 python3-pip
        fi
    elif [ "$OS" = "macos" ]; then
        print_error "يرجى تثبيت Python 3 من https://www.python.org/downloads/"
        exit 1
    fi
else
    print_success "Python 3 مثبت"
fi

# FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    print_warning "FFmpeg غير مثبت. جاري التثبيت..."
    if [ "$OS" = "linux" ]; then
        if [ "$DISTRO" = "Ubuntu" ] || [ "$DISTRO" = "Debian" ]; then
            sudo apt-get install -y ffmpeg
        elif [ "$DISTRO" = "Fedora" ]; then
            sudo dnf install -y ffmpeg
        fi
    elif [ "$OS" = "macos" ]; then
        if ! command -v brew &> /dev/null; then
            print_error "Homebrew غير مثبت. يرجى تثبيته أولاً من https://brew.sh"
            exit 1
        fi
        brew install ffmpeg
    fi
    print_success "FFmpeg تم تثبيته بنجاح"
else
    print_success "FFmpeg مثبت"
fi

# TTS
if ! command -v espeak-ng &> /dev/null; then
    print_warning "espeak-ng غير مثبت. جاري التثبيت..."
    if [ "$OS" = "linux" ]; then
        if [ "$DISTRO" = "Ubuntu" ] || [ "$DISTRO" = "Debian" ]; then
            sudo apt-get install -y espeak-ng
        elif [ "$DISTRO" = "Fedora" ]; then
            sudo dnf install -y espeak-ng
        fi
    elif [ "$OS" = "macos" ]; then
        brew install espeak-ng
    fi
    print_success "espeak-ng تم تثبيته بنجاح"
else
    print_success "espeak-ng مثبت"
fi

echo ""
print_status "تثبيت Ollama (محرك AI المحلي)..."

# Ollama
if ! command -v ollama &> /dev/null; then
    if [ "$OS" = "linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [ "$OS" = "macos" ]; then
        # macOS: تحميل من الموقع الرسمي
        print_status "يرجى تحميل Ollama من: https://ollama.com/download"
        print_status "أو تثبيت عبر Homebrew:"
        print_status "brew install ollama"
    fi
else
    print_success "Ollama مثبت"
fi

echo ""
print_status "تثبيت نموذج AI المحلي (qwen2.5:7b)..."
print_warning "قد يستغرق هذا بعض الوقت (حسب سرعة الإنترنت)"

if ! command -v ollama &> /dev/null; then
    print_warning "Ollama لم يتم تثبيته تلقائياً. يرجى تثبيته يدوياً من https://ollama.com"
    print_status "بعد التثبيت، قم بتشغيل: ollama pull qwen2.5:7b"
else
    ollama pull qwen2.5:7b || print_warning "قد تكون هناك مشكلة في تحميل النموذج"
fi

echo ""
echo "=========================================="
print_status "إعداد بيئة Python المحلية..."
echo "=========================================="
echo ""

# إنشاء virtual environment
if [ ! -d "venv" ]; then
    print_status "إنشاء بيئة Python المحلية (venv)..."
    python3 -m venv venv
    print_success "تم إنشاء venv"
else
    print_success "venv موجود بالفعل"
fi

# تفعيل virtual environment
print_status "تفعيل البيئة المحلية..."
source venv/bin/activate

# تحديث pip
print_status "تحديث pip..."
pip install --upgrade pip setuptools wheel

# تثبيت المتطلبات
print_status "تثبيت مكتبات Python المطلوبة..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
    print_success "تم تثبيت جميع مكتبات Python"
else
    print_warning "لم يتم العثور على backend/requirements.txt"
fi

# إنشاء ملفات التكوين
echo ""
echo "=========================================="
print_status "إنشاء ملفات التكوين..."
echo "=========================================="
echo ""

if [ ! -f ".env" ]; then
    print_status "إنشاء ملف .env..."
    cp .env.example .env
    print_success "تم إنشاء .env من .env.example"
else
    print_success ".env موجود بالفعل"
fi

# إنشاء مجلدات المخرجات
print_status "إنشاء مجلدات المشروع..."
mkdir -p backend/output
mkdir -p logs
print_success "تم إنشاء المجلدات"

echo ""
echo "=========================================="
echo -e "${GREEN}تم التثبيت بنجاح!${NC}"
echo "=========================================="
echo ""
echo "الخطوات التالية:"
echo ""
echo "1. تشغيل Ollama في نافذة منفصلة:"
echo -e "   ${BLUE}ollama serve${NC}"
echo ""
echo "2. تشغيل الخادم الخلفي (Backend):"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}cd backend${NC}"
echo -e "   ${BLUE}uvicorn app:app --reload --host 0.0.0.0 --port 8000${NC}"
echo ""
echo "3. تشغيل تطبيق سطح المكتب (في نافذة منفصلة):"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}python desktop/app.py${NC}"
echo ""
echo "أو استخدم السكريبت الشامل:"
echo -e "   ${BLUE}./run.sh${NC}"
echo ""
