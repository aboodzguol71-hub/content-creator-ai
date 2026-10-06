import sys
import os
from pathlib import Path

# إضافة المسار الأب إلى sys.path للوصول إلى backend
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QProgressBar,
        QTabWidget, QScrollArea, QMessageBox, QFileDialog, QSpinBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor
    import requests
    import json
    from datetime import datetime
except ImportError:
    print("خطأ: PyQt6 غير مثبت. يرجى تثبيته بـ: pip install PyQt6")
    sys.exit(1)


class ContentGeneratorWorker(QThread):
    """عامل لتوليد المحتوى في thread منفصل"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, topic, tone, platform, duration):
        super().__init__()
        self.topic = topic
        self.tone = tone
        self.platform = platform
        self.duration = duration
        # محاولة الاتصال بـ localhost أو 127.0.0.1
        self.api_urls = [
            "http://127.0.0.1:8000",
            "http://localhost:8000",
            "http://0.0.0.0:8000"
        ]
        self.api_url = None

    def run(self):
        try:
            # البحث عن الخادم الذي يعمل
            self.api_url = self._find_working_server()
            if not self.api_url:
                self.error.emit(
                    "لم يتمكن من العثور على الخادم.\n"
                    "تأكد من تشغيل الخادم بـ:\n"
                    "python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000"
                )
                return

            self.progress.emit(f"جاري الاتصال بالخادم على {self.api_url}...")
            
            payload = {
                "topic": self.topic,
                "tone": self.tone,
                "platform": self.platform,
                "language": "ar",
                "duration_seconds": self.duration
            }
            
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                data = response.json()
                self.finished.emit(data)
            else:
                self.error.emit(f"خطأ من الخادم: {response.status_code}\n{response.text}")
        except requests.exceptions.ConnectionError as e:
            self.error.emit(
                f"لم يتمكن من الاتصال بالخادم.\n"
                f"الخطأ: {str(e)}\n\n"
                f"تأكد من تشغيل الخادم بـ:\n"
                f"cd ~/content-creator-ai\n"
                f"source venv/bin/activate\n"
                f"python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000"
            )
        except Exception as e:
            self.error.emit(f"حدث خطأ: {str(e)}")

    def _find_working_server(self):
        """البحث عن الخادم الذي يعمل"""
        for url in self.api_urls:
            try:
                response = requests.get(f"{url}/health", timeout=2)
                if response.status_code == 200:
                    return url
            except:
                continue
        return None


class SmartContentCreatorApp(QMainWindow):
    """تطبيق سطح المكتب لمنشئ المحتوى الذكي"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.server_url = None
        self.init_ui()
        self.setWindowTitle("منشئ المحتوى الذكي")
        self.setGeometry(100, 100, 1200, 800)
        self.apply_dark_theme()
        
        # التحقق من الخادم عند البدء
        QTimer.singleShot(500, self.check_server)

    def init_ui(self):
        """إنشاء واجهة المستخدم"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # شريط الرأس
        header_layout = QHBoxLayout()
        title = QLabel("منشئ المحتوى الذكي 🎬")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        status_label = QLabel("حالة الاتصال: جاري التحقق...")
        self.status_label = status_label
        header_layout.addWidget(status_label)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # إنشاء التبويبات
        tabs = QTabWidget()
        
        # التبويب الأول: المولد
        generator_tab = self.create_generator_tab()
        tabs.addTab(generator_tab, "المولد")
        
        # التبويب الثاني: المخرجات
        output_tab = self.create_output_tab()
        tabs.addTab(output_tab, "المخرجات")
        
        # التبويب الثالث: الإعدادات
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "الإعدادات")
        
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)

    def create_generator_tab(self):
        """إنشاء تبويب المولد"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # الموضوع
        layout.addWidget(QLabel("موضوع المحتوى:"))
        self.topic_input = QTextEdit()
        self.topic_input.setPlaceholderText(
            "أدخل موضوع المحتوى...\nمثال: فوائد القراءة اليومية"
        )
        self.topic_input.setMaximumHeight(100)
        layout.addWidget(self.topic_input)
        
        # الأسلوب والمنصة
        options_layout = QHBoxLayout()
        
        options_layout.addWidget(QLabel("الأسلوب:"))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(["إعلامي", "تعليمي", "تسويقي", "قصصي"])
        options_layout.addWidget(self.tone_combo)
        
        options_layout.addSpacing(20)
        
        options_layout.addWidget(QLabel("المنصة:"))
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "YouTube Shorts",
            "Instagram Reels",
            "TikTok"
        ])
        options_layout.addWidget(self.platform_combo)
        
        options_layout.addSpacing(20)
        
        options_layout.addWidget(QLabel("المدة (ثانية):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(10)
        self.duration_spin.setMaximum(60)
        self.duration_spin.setValue(20)
        options_layout.addWidget(self.duration_spin)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        layout.addSpacing(10)
        
        # شريط التقدم
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # رسالة التقدم
        self.progress_label = QLabel("جاهز للبدء")
        layout.addWidget(self.progress_label)
        
        layout.addSpacing(10)
        
        # الزر
        self.generate_btn = QPushButton("🚀 إنشاء محتوى")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.generate_btn.clicked.connect(self.generate_content)
        layout.addWidget(self.generate_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_output_tab(self):
        """إنشاء تبويب المخرجات"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        # النص المولد
        content_layout.addWidget(QLabel("النص المولد:"))
        self.script_output = QTextEdit()
        self.script_output.setReadOnly(True)
        self.script_output.setMaximumHeight(150)
        content_layout.addWidget(self.script_output)
        
        # خطة النشر
        content_layout.addWidget(QLabel("خطة النشر:"))
        self.social_output = QTextEdit()
        self.social_output.setReadOnly(True)
        self.social_output.setMaximumHeight(200)
        content_layout.addWidget(self.social_output)
        
        # معلومات الملفات
        content_layout.addWidget(QLabel("الملفات المُنتجة:"))
        self.files_output = QTextEdit()
        self.files_output.setReadOnly(True)
        self.files_output.setMaximumHeight(150)
        content_layout.addWidget(self.files_output)
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        layout.addWidget(scroll)
        
        # أزرار المخرجات
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("📋 نسخ النص")
        copy_btn.clicked.connect(self.copy_script)
        button_layout.addWidget(copy_btn)
        
        open_folder_btn = QPushButton("📁 فتح مجلد المخرجات")
        open_folder_btn.clicked.connect(self.open_output_folder)
        button_layout.addWidget(open_folder_btn)
        
        layout.addLayout(button_layout)
        widget.setLayout(layout)
        return widget

    def create_settings_tab(self):
        """إنشاء تبويب الإعدادات"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # معلومات الخادم
        layout.addWidget(QLabel("معلومات الخادم:"))
        
        server_info_layout = QHBoxLayout()
        self.server_label = QLabel("عنوان الخادم: جاري البحث...")
        self.server_status_icon = QLabel("🔴")
        server_info_layout.addWidget(self.server_status_icon)
        server_info_layout.addWidget(self.server_label)
        server_info_layout.addStretch()
        layout.addLayout(server_info_layout)
        
        # زر الاتصال
        reconnect_btn = QPushButton("🔄 إعادة الاتصال")
        reconnect_btn.clicked.connect(self.check_server)
        layout.addWidget(reconnect_btn)
        
        layout.addSpacing(20)
        
        # معلومات المشروع
        layout.addWidget(QLabel("معلومات المشروع:"))
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setText(
            "منشئ المحتوى الذكي\n\n"
            "إصدار: 1.0.0\n"
            "لغة البرمجة: Python\n"
            "واجهة المستخدم: PyQt6\n"
            "محرك AI: Ollama + Qwen2.5\n\n"
            "ميزات:\n"
            "✓ توليد نصوص عربية\n"
            "✓ تحويل النص إلى صوت\n"
            "✓ إنشاء فيديو قصير\n"
            "✓ تشغيل محلي 100%\n"
            "✓ مناسب للأجهزة الاقتصادية"
        )
        about_text.setMaximumHeight(250)
        layout.addWidget(about_text)
        
        # المساعدة
        layout.addWidget(QLabel("المساعدة:"))
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setText(
            "كيفية الاستخدام:\n\n"
            "1. تأكد من تشغيل Ollama: ollama serve\n"
            "2. تأكد من تشغيل الخادم: python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000\n"
            "3. اكتب موضوع المحتوى\n"
            "4. اختر الأسلوب والمنصة\n"
            "5. اضغط 'إنشاء محتوى'\n"
            "6. انتظر حتى يتم إنشاء النص والصوت والفيديو\n"
            "7. انسخ النص أو افتح مجلد المخرجات"
        )
        help_text.setMaximumHeight(200)
        layout.addWidget(help_text)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def generate_content(self):
        """توليد محتوى جديد"""
        if not self.server_url:
            QMessageBox.warning(
                self,
                "خطأ",
                "الخادم غير متصل.\nيرجى التحقق من حالة الاتصال في تبويب الإعدادات."
            )
            return
        
        topic = self.topic_input.toPlainText().strip()
        
        if not topic:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال موضوع المحتوى")
            return
        
        tone = self.tone_combo.currentText()
        platform = self.platform_combo.currentText()
        duration = self.duration_spin.value()
        
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_label.setText("جاري توليد المحتوى...")
        
        self.worker = ContentGeneratorWorker(topic, tone, platform, duration)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def on_generation_finished(self, data):
        """معالجة النتيجة النهائية"""
        # عرض النص
        self.script_output.setText(data.get("script", "لا توجد بيانات"))
        
        # عرض خطة النشر
        social_plan = data.get("social_plan", {})
        social_text = f"""
المنصة: {social_plan.get('platform', 'N/A')}
الخطاف: {social_plan.get('hook', 'N/A')}
الهاشتاجات: {' '.join(social_plan.get('hashtags', []))}
الطول الموصى به: {social_plan.get('recommended_length', 'N/A')}
الحالة: {social_plan.get('status', 'N/A')}
        """
        self.social_output.setText(social_text)
        
        # عرض معلومات الملفات
        files_text = f"""
الموضوع: {data.get('topic', 'N/A')}
ملف الصوت: {data.get('audio', 'N/A')}
ملف الفيديو: {data.get('video', 'N/A')}
مجلد المخرجات: {data.get('output_dir', 'N/A')}
        """
        self.files_output.setText(files_text)
        
        self.progress_label.setText("✓ تم إنشاء المحتوى بنجاح!")
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.information(
            self,
            "نجاح",
            "تم إنشاء المحتوى بنجاح!\nيمكنك عرض الملفات في تبويب 'المخرجات'"
        )

    def on_generation_error(self, error_msg):
        """معالجة الأخطاء"""
        self.progress_label.setText(f"❌ خطأ: {error_msg}")
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "خطأ", error_msg)

    def update_progress(self, message):
        """تحديث رسالة التقدم"""
        self.progress_label.setText(message)
        self.progress_bar.setValue(
            (self.progress_bar.value() + 10) % 100
        )

    def check_server(self):
        """التحقق من حالة الخادم"""
        urls = [
            "http://127.0.0.1:8000",
            "http://localhost:8000",
            "http://0.0.0.0:8000"
        ]
        
        for url in urls:
            try:
                response = requests.get(f"{url}/health", timeout=2)
                if response.status_code == 200:
                    self.server_url = url
                    self.status_label.setText(f"حالة الاتصال: 🟢 متصل ({url})")
                    self.server_label.setText(f"عنوان الخادم: {url}")
                    self.server_status_icon.setText("🟢")
                    return
            except:
                continue
        
        self.server_url = None
        self.status_label.setText("حالة الاتصال: 🔴 غير متصل")
        self.server_label.setText("عنوان الخادم: لم يتم العثور على الخادم")
        self.server_status_icon.setText("🔴")

    def copy_script(self):
        """نسخ النص إلى الحافظة"""
        text = self.script_output.toPlainText()
        if text:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "نجاح", "تم نسخ النص")
        else:
            QMessageBox.warning(self, "تحذير", "لا يوجد نص للنسخ")

    def open_output_folder(self):
        """فتح مجلد المخرجات"""
        output_dir = Path("backend/output").resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        import platform
        import subprocess
        
        if platform.system() == "Windows":
            subprocess.run(["explorer", str(output_dir)])
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(output_dir)])
        else:
            subprocess.run(["xdg-open", str(output_dir)])

    def apply_dark_theme(self):
        """تطبيق مظهر داكن"""
        dark_stylesheet = """
        QMainWindow, QWidget {
            background-color: #1e1e2e;
            color: #e2e8f0;
        }
        QLabel {
            color: #e2e8f0;
        }
        QTextEdit, QLineEdit, QComboBox, QSpinBox {
            background-color: #2d2d44;
            color: #e2e8f0;
            border: 1px solid #44475a;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton {
            background-color: #6366f1;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4f46e5;
        }
        QPushButton:pressed {
            background-color: #4338ca;
        }
        QPushButton:disabled {
            background-color: #44475a;
            color: #6272a4;
        }
        QProgressBar {
            border: 1px solid #44475a;
            border-radius: 5px;
            background-color: #2d2d44;
        }
        QProgressBar::chunk {
            background-color: #6366f1;
        }
        QTabWidget::pane {
            border: 1px solid #44475a;
        }
        QTabBar::tab {
            background-color: #2d2d44;
            color: #6272a4;
            padding: 8px 20px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #6366f1;
            color: white;
        }
        """
        self.setStyleSheet(dark_stylesheet)


def main():
    app = QApplication(sys.argv)
    window = SmartContentCreatorApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
