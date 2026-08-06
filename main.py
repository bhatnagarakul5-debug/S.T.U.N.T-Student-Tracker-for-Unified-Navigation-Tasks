"""
STUNT: Student Tracker for Unified Navigation & Tasks
100% Native PyQt6 Python Desktop Application (main.py)
"""

import sys
import os
import json
import base64
import math
from datetime import datetime, date, timedelta

import db

from PyQt6.QtCore import Qt, QTimer, QUrl, QSize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QStackedWidget, QProgressBar, QFrame,
    QFileDialog, QMessageBox, QTabWidget, QListWidget, QListWidgetItem,
    QTextEdit, QGraphicsOpacityEffect, QScrollArea, QGridLayout, QFormLayout,
    QSystemTrayIcon
)
from PyQt6.QtGui import QIcon, QPixmap, QColor, QFont, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

# Matplotlib Qt Integration
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

THEMES = {
    "Glitchcore Dark": {
        "bg": "#0a0b10", "card": "#181a27", "primary": "#6366f1", "secondary": "#0ea5e9", "accent": "#10b981", "danger": "#f43f5e"
    },
    "Midnight Cyberpunk": {
        "bg": "#0d0914", "card": "#1c122c", "primary": "#ec4899", "secondary": "#a855f7", "accent": "#06b6d4", "danger": "#ff0055"
    },
    "Emerald Tech": {
        "bg": "#06140e", "card": "#0f291e", "primary": "#10b981", "secondary": "#06b6d4", "accent": "#f59e0b", "danger": "#ef4444"
    },
    "Solar Amber": {
        "bg": "#140e06", "card": "#291b0f", "primary": "#f59e0b", "secondary": "#f97316", "accent": "#10b981", "danger": "#ef4444"
    }
}

def generate_qss(theme_name="Glitchcore Dark"):
    t = THEMES.get(theme_name, THEMES["Glitchcore Dark"])
    return f"""
QMainWindow, QDialog {{
    background-color: {t['bg']};
    color: #f8fafc;
    font-family: 'Segoe UI', Inter, sans-serif;
}}

QWidget {{
    color: #cbd5e1;
    font-size: 13px;
}}

QFrame.card {{
    background-color: {t['card']};
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 16px;
}}

QFrame.hero-card {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(99, 102, 241, 0.15), stop:1 rgba(14, 165, 233, 0.05));
    border: 1px solid {t['primary']};
    border-radius: 12px;
}}

QFrame.dock {{
    background-color: #08090d;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}}

QFrame.sidebar {{
    background-color: {t['card']};
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}}

QFrame.drawer {{
    background-color: {t['card']};
    border-left: 1px solid rgba(255, 255, 255, 0.08);
}}

QLabel {{
    color: #cbd5e1;
}}

QLabel.h1 {{
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
}}

QLabel.h2 {{
    font-size: 17px;
    font-weight: 600;
    color: #ffffff;
}}

QLabel.h3 {{
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}}

QLabel.kpi-val {{
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
}}

QPushButton {{
    background-color: {t['card']};
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.2);
}}

QPushButton.primary {{
    background-color: {t['primary']};
    color: #ffffff;
    border: 1px solid {t['primary']};
}}

QPushButton.primary:hover {{
    background-color: {t['primary']};
    opacity: 0.85;
}}

QPushButton.success {{
    background-color: {t['accent']};
    color: #ffffff;
    border: 1px solid {t['accent']};
}}

QPushButton.danger {{
    background-color: {t['danger']};
    color: #ffffff;
    border: 1px solid {t['danger']};
}}

QPushButton.icon-btn {{
    background: transparent;
    border: none;
    padding: 6px;
}}

QPushButton.icon-btn:hover {{
    background-color: rgba(255, 255, 255, 0.08);
    border-radius: 6px;
}}

QLineEdit, QComboBox, QTextEdit {{
    background-color: #10121d;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 8px 12px;
}}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
    border-color: {t['primary']};
}}

QProgressBar {{
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 4px;
    text-align: center;
    color: transparent;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {t['primary']}, stop:1 {t['secondary']});
    border-radius: 4px;
}}

QTableWidget {{
    background-color: {t['card']};
    border: 1px solid rgba(255, 255, 255, 0.08);
    gridline-color: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
}}

QHeaderView::section {{
    background-color: #10121d;
    color: #64748b;
    padding: 10px;
    border: none;
    font-weight: 600;
    font-size: 11px;
}}

QTableWidget::item {{
    padding: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}}
"""

# Matplotlib Finance Chart Canvas
class FinanceChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#181a27')
        self.axes_donut = fig.add_subplot(121, facecolor='#181a27')
        self.axes_bar = fig.add_subplot(122, facecolor='#181a27')
        fig.tight_layout(pad=2.0)

        super().__init__(fig)
        self.setParent(parent)

    def update_charts(self, finances):
        self.axes_donut.clear()
        self.axes_bar.clear()

        categories = ["Food & Dining", "Transport & Transit", "Academics & Books", "Entertainment", "Personal Supplies", "Miscellaneous"]
        cat_totals = [sum(f['amount'] for f in finances if f['type'] == 'Expense' and f['category'] == cat) for cat in categories]

        non_zero = [(cat, val) for cat, val in zip(categories, cat_totals) if val > 0]
        if non_zero:
            labels, values = zip(*non_zero)
            colors = ['#f43f5e', '#0ea5e9', '#6366f1', '#f59e0b', '#10b981', '#8b5cf6']
            wedges, texts, autotexts = self.axes_donut.pie(
                values, labels=labels, autopct='%1.0f%%', startangle=140,
                colors=colors[:len(values)], textprops=dict(color='#cbd5e1', fontsize=9)
            )
            for at in autotexts: at.set_color('#ffffff'); at.set_fontsize(8); at.set_weight('bold')
            centre_circle = matplotlib.patches.Circle((0,0), 0.55, fc='#181a27')
            self.axes_donut.add_artist(centre_circle)
        else:
            self.axes_donut.text(0, 0, 'No Expenses Logged', color='#64748b', ha='center', va='center', fontsize=11)

        self.axes_donut.set_title('Expense Breakdown by Category', color='#ffffff', fontsize=11, fontweight='bold', pad=10)

        inc_total = sum(f['amount'] for f in finances if f['type'] == 'Income')
        exp_total = sum(f['amount'] for f in finances if f['type'] == 'Expense')

        bars = self.axes_bar.bar(['Total Income', 'Total Expense'], [inc_total, exp_total], color=['#0ea5e9', '#f43f5e'], width=0.45)
        self.axes_bar.set_title('Income vs Expense Overview (₹)', color='#ffffff', fontsize=11, fontweight='bold', pad=10)
        self.axes_bar.tick_params(colors='#94a3b8', labelsize=9)
        self.axes_bar.set_facecolor('#181a27')
        self.axes_bar.spines['top'].set_visible(False)
        self.axes_bar.spines['right'].set_visible(False)
        self.axes_bar.spines['left'].set_color('#1e2030')
        self.axes_bar.spines['bottom'].set_color('#1e2030')

        for bar in bars:
            yval = bar.get_height()
            if yval > 0:
                self.axes_bar.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f'₹{yval:,.0f}', ha='center', va='bottom', color='#ffffff', fontsize=9, fontweight='bold')

        self.draw()

# Matplotlib CGPA / SGPA Trend Canvas
class CgpaChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=2.5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#181a27')
        self.ax = fig.add_subplot(111, facecolor='#181a27')
        fig.tight_layout(pad=1.5)

        super().__init__(fig)
        self.setParent(parent)

    def update_chart(self, sgpa_list):
        self.ax.clear()
        if sgpa_list:
            sems = [f"Sem {s['sem']}" for s in sgpa_list]
            sgpas = [s['sgpa'] for s in sgpa_list]
            self.ax.plot(sems, sgpas, marker='o', color='#6366f1', linewidth=2.5, markersize=6, label='SGPA')
            self.ax.set_ylim(0, 10)
            self.ax.axhline(7.5, color='#f59e0b', linestyle='--', alpha=0.5, label='7.5 Target')
            self.ax.set_title('Semester SGPA Trend Line', color='#ffffff', fontsize=11, fontweight='bold')
            self.ax.tick_params(colors='#94a3b8', labelsize=9)
            self.ax.legend(facecolor='#121420', edgecolor='none', labelcolor='#cbd5e1')
            self.ax.spines['top'].set_visible(False); self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#1e2030'); self.ax.spines['bottom'].set_color('#1e2030')
        else:
            self.ax.text(0.5, 0.5, 'Log Grades to view SGPA Trend', color='#64748b', ha='center', va='center', fontsize=11)
        self.draw()

# Native Video Opening Splash Window
class StuntVideoSplash(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STUNT Platform")
        self.setFixedSize(640, 480)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget(self)
        layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        video_path = os.path.join(os.path.dirname(__file__), 'assets', 'RedandBlackGlitchcoreStuntLogo.mp4')
        if os.path.exists(video_path):
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.play()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.accept)
        self.timer.start(6000)

        self.video_widget.mousePressEvent = lambda e: self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)

# Task & Savings Celebration Window
class TaskCelebrationWindow(QDialog):
    def __init__(self, task_title, parent=None, is_savings=False):
        super().__init__(parent)
        self.setWindowTitle("Goal Accomplished! 🎉" if is_savings else "Task Accomplished! 🎉")
        self.setFixedSize(420, 260)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24); lay.setSpacing(14)

        icon_lbl = QLabel("🎯" if is_savings else "🎉", self); icon_lbl.setStyleSheet("font-size: 44px;")
        lay.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        title_lbl = QLabel("SAVINGS GOAL ACHIEVED!" if is_savings else "TASK COMPLETED!", self)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
        lay.addWidget(title_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        task_lbl = QLabel(f'"{task_title}"', self); task_lbl.setStyleSheet("font-size: 14px; font-weight: 600; color: #ffffff;"); task_lbl.setWordWrap(True)
        lay.addWidget(task_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        sub_lbl = QLabel("You have successfully saved enough funds to purchase this item!" if is_savings else "Great progress on your academic degree journey!", self)
        sub_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        lay.addWidget(sub_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_close = QPushButton("Continue", self); btn_close.setProperty("class", "primary")
        btn_close.clicked.connect(self.accept)
        lay.addWidget(btn_close)

# Native Edit Profile & Settings Dialog
class EditProfileDialog(QDialog):
    def __init__(self, parent, current_prof):
        super().__init__(parent)
        self.setWindowTitle("Edit Student Profile & Degree Settings")
        self.setFixedWidth(460)

        lay = QVBoxLayout(self); lay.setSpacing(14)

        hdr = QLabel("Student Profile & University Requirements", self); hdr.setProperty("class", "h2")
        lay.addWidget(hdr)

        form = QFormLayout()
        self.name_in = QLineEdit(self); self.name_in.setText(current_prof.get('name', 'Akul'))
        self.college_in = QLineEdit(self); self.college_in.setText(current_prof.get('college', 'University'))
        self.course_in = QLineEdit(self); self.course_in.setText(current_prof.get('course', 'B.Tech Computer Science'))
        self.batch_in = QLineEdit(self); self.batch_in.setText(current_prof.get('batch', '2026 – 2031'))

        self.start_in = QLineEdit(self); self.start_in.setText(current_prof.get('startDate', '2026-08-01'))
        self.end_in = QLineEdit(self); self.end_in.setText(current_prof.get('endDate', '2031-07-31'))
        self.sems_in = QLineEdit(self); self.sems_in.setText(str(current_prof.get('totalSemesters', 10)))

        self.att_pct_in = QLineEdit(self); self.att_pct_in.setText(str(current_prof.get('targetAttendancePct', 75.0)))
        self.budget_in = QLineEdit(self); self.budget_in.setText(str(current_prof.get('monthlyBudgetCap', 5000.0)))
        self.cgpa_in = QLineEdit(self); self.cgpa_in.setText(str(current_prof.get('targetCgpa', 8.5)))

        self.theme_combo = QComboBox(self)
        for t_name in THEMES.keys(): self.theme_combo.addItem(t_name)
        idx = self.theme_combo.findText(current_prof.get('themeName', 'Glitchcore Dark'))
        if idx != -1: self.theme_combo.setCurrentIndex(idx)

        form.addRow("Student Name:", self.name_in)
        form.addRow("College Name:", self.college_in)
        form.addRow("Course / Branch:", self.course_in)
        form.addRow("Batch Label:", self.batch_in)
        form.addRow("Degree Start Date (YYYY-MM-DD):", self.start_in)
        form.addRow("Degree End Date (YYYY-MM-DD):", self.end_in)
        form.addRow("Total Semesters (e.g. 10, 8, 6):", self.sems_in)
        form.addRow("University Min Attendance Target (%):", self.att_pct_in)
        form.addRow("Monthly Budget Cap (₹):", self.budget_in)
        form.addRow("Target Degree CGPA (0 - 10):", self.cgpa_in)
        form.addRow("Application UI Theme:", self.theme_combo)

        lay.addLayout(form)

        btn_save = QPushButton("Save Profile & Settings", self); btn_save.setProperty("class", "primary")
        btn_save.clicked.connect(self.save_profile)
        lay.addWidget(btn_save)

    def save_profile(self):
        try: sems = int(self.sems_in.text())
        except ValueError: sems = 10
        try: att_pct = float(self.att_pct_in.text())
        except ValueError: att_pct = 75.0
        try: budget = float(self.budget_in.text())
        except ValueError: budget = 5000.0
        try: cgpa = float(self.cgpa_in.text())
        except ValueError: cgpa = 8.5

        prof = {
            'name': self.name_in.text(),
            'college': self.college_in.text(),
            'course': self.course_in.text(),
            'batch': self.batch_in.text(),
            'startDate': self.start_in.text(),
            'endDate': self.end_in.text(),
            'totalSemesters': sems,
            'targetAttendancePct': att_pct,
            'monthlyBudgetCap': budget,
            'targetCgpa': cgpa,
            'themeName': self.theme_combo.currentText(),
            'avatar': 'assets/RedandBlackGlitchcoreStuntLogo.png'
        }
        db.save_profile(prof)
        self.accept()

# Native Main Window
class StuntMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("STUNT — Student Tracker for Unified Navigation & Tasks")
        self.resize(1366, 850)
        self.setMinimumSize(1024, 700)

        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'RedandBlackGlitchcoreStuntLogo.png')
        if os.path.exists(icon_path): self.setWindowIcon(QIcon(icon_path))

        self.tray_icon = QSystemTrayIcon(self)
        if os.path.exists(icon_path): self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("STUNT — Student Tracker Platform")
        self.tray_icon.show()

        db.init_db()
        self.data = db.get_all_data()
        self.profile = db.get_profile()

        self.pomo_seconds = 25 * 60
        self.pomo_is_running = False
        self.pomo_timer = QTimer(self)
        self.pomo_timer.timeout.connect(self.pomo_tick)

        # Background Timetable Lecture Alarm Timer (checks every 60s)
        self.alarm_timer = QTimer(self)
        self.alarm_timer.timeout.connect(self.check_lecture_alarms)
        self.alarm_timer.start(60000)

        self.active_sem = 1
        self.init_ui()

    def send_notification(self, title, message):
        if self.tray_icon.isSystemTrayAvailable():
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 4000)

    def check_lecture_alarms(self):
        today_str = datetime.now().strftime("%A")
        now_time = datetime.now()
        for slot in self.data.get('timetable', []):
            if slot['day'] == today_str:
                try:
                    slot_t = datetime.strptime(slot['start'], "%I:%M %p").replace(year=now_time.year, month=now_time.month, day=now_time.day)
                    diff = (slot_t - now_time).total_seconds()
                    if 0 <= diff <= 900: # Within 15 mins
                        self.send_notification("Upcoming Lecture Alarm! ⏰", f"Class '{slot['subject']}' in 15 mins at {slot['location']}")
                except ValueError:
                    pass

    def apply_theme(self):
        theme_name = self.profile.get('themeName', 'Glitchcore Dark')
        self.setStyleSheet(generate_qss(theme_name))

    def init_ui(self):
        self.apply_theme()

        main_widget = QWidget(self); self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget); main_layout.setContentsMargins(0, 0, 0, 0); main_layout.setSpacing(0)

        # 1. Left Dock
        dock = QFrame(self); dock.setProperty("class", "dock"); dock.setFixedWidth(64)
        dock_layout = QVBoxLayout(dock); dock_layout.setContentsMargins(10, 16, 10, 16); dock_layout.setSpacing(12)

        logo_lbl = QLabel(self)
        pix = QPixmap(os.path.join(os.path.dirname(__file__), 'assets', 'RedandBlackGlitchcoreStuntLogo.png'))
        if not pix.isNull(): logo_lbl.setPixmap(pix.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        dock_layout.addWidget(logo_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        nav_items = [
            ("Dashboard", "📊"),
            ("Academic CGPA", "🎓"),
            ("Syllabus & Units", "📚"),
            ("Tasks & Focus", "✅"),
            ("Attendance", "📋"),
            ("Finance & Savings", "💰"),
            ("Timetable", "📅"),
            ("Memories", "🖼️"),
            ("Milestones", "⏳")
        ]

        self.nav_btns = []
        for idx, (title, icon) in enumerate(nav_items):
            btn = QPushButton(icon, self); btn.setToolTip(title); btn.setFixedSize(44, 44)
            btn.clicked.connect(lambda checked, i=idx: self.switch_view(i))
            dock_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.nav_btns.append(btn)

        dock_layout.addStretch()

        settings_btn = QPushButton("⚙️", self); settings_btn.setToolTip("Settings & Backup"); settings_btn.setFixedSize(44, 44)
        settings_btn.clicked.connect(self.open_settings_dialog)
        dock_layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(dock)

        # 2. Sub-Sidebar Navigation
        self.sidebar = QFrame(self); self.sidebar.setProperty("class", "sidebar"); self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar); sidebar_layout.setContentsMargins(16, 16, 16, 16)

        side_title = QLabel("STUNT Platform", self); side_title.setProperty("class", "h2")
        sidebar_layout.addWidget(side_title)

        side_sub = QLabel("Academic Degree Tracker", self); side_sub.setStyleSheet("color: #64748b; font-size: 11px;")
        sidebar_layout.addWidget(side_sub)

        sidebar_layout.addSpacing(12)

        self.channels_list = QListWidget(self); self.channels_list.setStyleSheet("background: transparent; border: none;")
        sidebar_layout.addWidget(self.channels_list)

        self.prof_box = QFrame(self); self.prof_box.setProperty("class", "card")
        prof_lay = QVBoxLayout(self.prof_box); prof_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_prof_name = QLabel(self.profile['name'], self); self.lbl_prof_name.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        self.lbl_prof_course = QLabel(self.profile['course'], self); self.lbl_prof_course.setStyleSheet("font-size: 11px; color: #0ea5e9;")
        self.lbl_prof_college = QLabel(self.profile['college'], self); self.lbl_prof_college.setStyleSheet("font-size: 10px; color: #64748b;")

        btn_edit_prof = QPushButton("✏️ Edit Profile & Theme", self); btn_edit_prof.setStyleSheet("font-size: 11px; padding: 4px;")
        btn_edit_prof.clicked.connect(self.open_edit_profile_dialog)

        prof_lay.addWidget(self.lbl_prof_name); prof_lay.addWidget(self.lbl_prof_course)
        prof_lay.addWidget(self.lbl_prof_college); prof_lay.addWidget(btn_edit_prof)

        sidebar_layout.addWidget(self.prof_box)
        main_layout.addWidget(self.sidebar)

        # 3. Main Workspace Area
        workspace = QWidget(self)
        workspace_layout = QVBoxLayout(workspace); workspace_layout.setContentsMargins(0, 0, 0, 0); workspace_layout.setSpacing(0)

        topbar = QFrame(self); topbar.setFixedHeight(56); topbar.setStyleSheet("background: #0f1019; border-bottom: 1px solid rgba(255,255,255,0.08);")
        topbar_layout = QHBoxLayout(topbar); topbar_layout.setContentsMargins(16, 0, 16, 0)

        self.btn_toggle_sidebar = QPushButton("☰", self); self.btn_toggle_sidebar.setProperty("class", "icon-btn"); self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar)
        topbar_layout.addWidget(self.btn_toggle_sidebar)

        self.topbar_title = QLabel("Overview Dashboard", self); self.topbar_title.setProperty("class", "h2")
        topbar_layout.addWidget(self.topbar_title)

        topbar_layout.addStretch()

        btn_exp_pdf = QPushButton("📄 Export Report", self); btn_exp_pdf.setProperty("class", "primary"); btn_exp_pdf.clicked.connect(self.export_pdf_report)
        topbar_layout.addWidget(btn_exp_pdf)

        btn_add_savings = QPushButton("🎯 Savings Goal", self); btn_add_savings.setProperty("class", "success"); btn_add_savings.clicked.connect(self.open_savings_goal_dialog)
        topbar_layout.addWidget(btn_add_savings)

        btn_add_grade = QPushButton("+ Log Grade", self); btn_add_grade.clicked.connect(lambda: self.open_grade_dialog())
        topbar_layout.addWidget(btn_add_grade)

        btn_add_task = QPushButton("+ Add Task", self); btn_add_task.clicked.connect(lambda: self.open_task_dialog())
        topbar_layout.addWidget(btn_add_task)

        btn_log_att = QPushButton("+ Log Attendance", self); btn_log_att.clicked.connect(lambda: self.open_attendance_dialog())
        topbar_layout.addWidget(btn_log_att)

        self.btn_toggle_drawer = QPushButton("📊", self); self.btn_toggle_drawer.setProperty("class", "icon-btn"); self.btn_toggle_drawer.clicked.connect(self.toggle_drawer)
        topbar_layout.addWidget(self.btn_toggle_drawer)

        workspace_layout.addWidget(topbar)

        self.views_stack = QStackedWidget(self)
        workspace_layout.addWidget(self.views_stack)

        self.init_dashboard_view()
        self.init_cgpa_view()
        self.init_syllabus_view()
        self.init_tasks_view()
        self.init_attendance_view()
        self.init_finance_view()
        self.init_timetable_view()
        self.init_memories_view()
        self.init_milestones_view()

        main_layout.addWidget(workspace, stretch=1)

        # 4. Right Diagnostics Drawer
        self.drawer = QFrame(self); self.drawer.setProperty("class", "drawer"); self.drawer.setFixedWidth(240)
        drawer_layout = QVBoxLayout(self.drawer); drawer_layout.setContentsMargins(16, 16, 16, 16)

        diag_hdr = QLabel("System Diagnostics", self); diag_hdr.setProperty("class", "h3")
        drawer_layout.addWidget(diag_hdr)
        drawer_layout.addSpacing(10)

        card_student = QFrame(self); card_student.setProperty("class", "card")
        cs_lay = QVBoxLayout(card_student)
        cs_lay.addWidget(QLabel("STUDENT PROFILE", self))
        self.lbl_drawer_student = QLabel(self.profile['name'], self); self.lbl_drawer_student.setStyleSheet("font-weight: bold; color: #ffffff;")
        self.lbl_drawer_college = QLabel(self.profile['college'], self); self.lbl_drawer_college.setStyleSheet("font-size: 11px; color: #64748b;")
        cs_lay.addWidget(self.lbl_drawer_student); cs_lay.addWidget(self.lbl_drawer_college)
        drawer_layout.addWidget(card_student)

        card_target = QFrame(self); card_target.setProperty("class", "card")
        ct_lay = QVBoxLayout(card_target)
        ct_lay.addWidget(QLabel("UNIVERSITY MIN ATTENDANCE", self))
        self.lbl_drawer_min_att = QLabel("75.0% Minimum Required", self); self.lbl_drawer_min_att.setStyleSheet("color: #f59e0b; font-weight: bold;")
        ct_lay.addWidget(self.lbl_drawer_min_att)
        drawer_layout.addWidget(card_target)

        card_time = QFrame(self); card_time.setProperty("class", "card")
        ct2_lay = QVBoxLayout(card_time)
        ct2_lay.addWidget(QLabel("ACADEMIC DEGREE", self))
        self.lbl_drawer_days = QLabel("1826 Days Left", self); self.lbl_drawer_days.setStyleSheet("color: #0ea5e9; font-weight: bold;")
        ct2_lay.addWidget(self.lbl_drawer_days)
        drawer_layout.addWidget(card_time)

        drawer_layout.addStretch()
        main_layout.addWidget(self.drawer)

        self.switch_view(0)
        self.refresh_all_views()

    def open_edit_profile_dialog(self):
        dlg = EditProfileDialog(self, self.profile)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.profile = db.get_profile()
            self.apply_theme()
            self.refresh_all_views()

    def toggle_sidebar(self): self.sidebar.setVisible(not self.sidebar.isVisible())
    def toggle_drawer(self): self.drawer.setVisible(not self.drawer.isVisible())

    def switch_view(self, index):
        self.views_stack.setCurrentIndex(index)
        for idx, btn in enumerate(self.nav_btns):
            if idx == index: btn.setStyleSheet("background: #6366f1; color: #fff;")
            else: btn.setStyleSheet("background: #181a27; color: #cbd5e1;")

        self.channels_list.clear()
        titles = ["Overview Dashboard", "CGPA & Grade Intelligence", "Exam Syllabus Matrix", "Task & Focus Pomodoro", "Attendance & Bunk Safety", "Finance & Targeted Savings", "Weekly Timetable", "Memories Vault", "Milestones Feed"]
        self.topbar_title.setText(titles[index])

        if index == 0: self.channels_list.addItem("Summary Overview"); self.channels_list.addItem("5-Year Journey")
        elif index == 1: self.channels_list.addItem("Grades & SGPA Ledger"); self.channels_list.addItem("Target CGPA Predictor")
        elif index == 2: self.channels_list.addItem("Syllabus Units"); self.channels_list.addItem("Revision Tracker")
        elif index == 3: self.channels_list.addItem("Tasks & Goals"); self.channels_list.addItem("Pomodoro Focus Timer")
        elif index == 4: self.channels_list.addItem("Subject Cards & Bunk Safety"); self.channels_list.addItem("Attendance History")
        elif index == 5: self.channels_list.addItem("Targeted Savings Goals"); self.channels_list.addItem("Wallet & Expense Graphs"); self.channels_list.addItem("Transaction Ledger")
        elif index == 6: self.channels_list.addItem("Class Slots")
        elif index == 7: self.channels_list.addItem("Campus Photo Gallery")
        elif index == 8: self.channels_list.addItem("Milestone Timeline")

    # 1. DASHBOARD VIEW
    def init_dashboard_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24); lay.setSpacing(20)

        hero = QFrame(self); hero.setProperty("class", "hero-card"); hero_lay = QVBoxLayout(hero)
        self.lbl_journey_dates = QLabel("Academic Degree Journey", self); self.lbl_journey_dates.setProperty("class", "h2")
        hero_lay.addWidget(self.lbl_journey_dates)

        self.hero_progress = QProgressBar(self); self.hero_progress.setFixedHeight(10)
        hero_lay.addWidget(self.hero_progress)

        hero_met_lay = QHBoxLayout()
        self.lbl_days_elapsed = QLabel("0 Days Completed", self)
        self.lbl_degree_pct = QLabel("0.0% Degree Completion", self); self.lbl_degree_pct.setStyleSheet("color: #0ea5e9; font-weight: bold;")
        self.lbl_days_left = QLabel("0 Days Remaining", self)

        hero_met_lay.addWidget(self.lbl_days_elapsed); hero_met_lay.addWidget(self.lbl_degree_pct); hero_met_lay.addWidget(self.lbl_days_left)
        hero_lay.addLayout(hero_met_lay)
        lay.addWidget(hero)

        kpi_lay = QHBoxLayout(); kpi_lay.setSpacing(16)

        k1 = QFrame(self); k1.setProperty("class", "card"); k1_lay = QVBoxLayout(k1)
        k1_lay.addWidget(QLabel("Overall CGPA", self))
        self.kpi_cgpa_val = QLabel("0.00", self); self.kpi_cgpa_val.setProperty("class", "kpi-val"); self.kpi_cgpa_val.setStyleSheet("color: #6366f1;")
        k1_lay.addWidget(self.kpi_cgpa_val); kpi_lay.addWidget(k1)

        k2 = QFrame(self); k2.setProperty("class", "card"); k2_lay = QVBoxLayout(k2)
        k2_lay.addWidget(QLabel("Overall Attendance", self))
        self.kpi_att_val = QLabel("0.0%", self); self.kpi_att_val.setProperty("class", "kpi-val")
        k2_lay.addWidget(self.kpi_att_val); kpi_lay.addWidget(k2)

        k3 = QFrame(self); k3.setProperty("class", "card"); k3_lay = QVBoxLayout(k3)
        k3_lay.addWidget(QLabel("Total Savings Accumulated", self))
        self.kpi_savings_val = QLabel("₹0", self); self.kpi_savings_val.setProperty("class", "kpi-val"); self.kpi_savings_val.setStyleSheet("color: #10b981;")
        k3_lay.addWidget(self.kpi_savings_val); kpi_lay.addWidget(k3)

        k4 = QFrame(self); k4.setProperty("class", "card"); k4_lay = QVBoxLayout(k4)
        k4_lay.addWidget(QLabel("Syllabus Completion", self))
        self.kpi_syl_val = QLabel("0%", self); self.kpi_syl_val.setProperty("class", "kpi-val"); self.kpi_syl_val.setStyleSheet("color: #0ea5e9;")
        k4_lay.addWidget(self.kpi_syl_val); kpi_lay.addWidget(k4)

        k5 = QFrame(self); k5.setProperty("class", "card"); k5_lay = QVBoxLayout(k5)
        k5_lay.addWidget(QLabel("Task Completion", self))
        self.kpi_task_val = QLabel("0%", self); self.kpi_task_val.setProperty("class", "kpi-val"); self.kpi_task_val.setStyleSheet("color: #f59e0b;")
        k5_lay.addWidget(self.kpi_task_val); kpi_lay.addWidget(k5)

        lay.addLayout(kpi_lay)
        lay.addStretch()
        self.views_stack.addWidget(view)

    # 2. CGPA & GRADE INTELLIGENCE VIEW
    def init_cgpa_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("CGPA / SGPA Intelligence & Grade Ledger", self))
        hdr_lay.addStretch()
        btn_add_g = QPushButton("+ Log Subject Grade", self); btn_add_g.setProperty("class", "primary"); btn_add_g.clicked.connect(self.open_grade_dialog)
        hdr_lay.addWidget(btn_add_g)
        lay.addLayout(hdr_lay)

        cgpa_card = QFrame(self); cgpa_card.setProperty("class", "card")
        cc_lay = QHBoxLayout(cgpa_card)

        pred_box = QVBoxLayout()
        self.lbl_cgpa_current = QLabel("Current CGPA: 0.00", self); self.lbl_cgpa_current.setStyleSheet("font-size: 20px; font-weight: bold; color: #6366f1;")
        self.lbl_cgpa_target = QLabel("Target CGPA: 8.50", self); self.lbl_cgpa_target.setStyleSheet("font-size: 14px; color: #0ea5e9;")
        self.lbl_cgpa_needed = QLabel("Required SGPA in remaining semesters: N/A", self); self.lbl_cgpa_needed.setStyleSheet("font-size: 12px; color: #cbd5e1;")
        pred_box.addWidget(self.lbl_cgpa_current); pred_box.addWidget(self.lbl_cgpa_target); pred_box.addWidget(self.lbl_cgpa_needed)
        cc_lay.addLayout(pred_box)

        self.cgpa_canvas = CgpaChartCanvas(self, width=6, height=2.5, dpi=100)
        cc_lay.addWidget(self.cgpa_canvas)

        lay.addWidget(cgpa_card)

        self.grades_table = QTableWidget(self)
        self.grades_table.setColumnCount(6)
        self.grades_table.setHorizontalHeaderLabels(["Semester", "Subject Code", "Subject Name", "Credits", "Grade Points", "Actions"])
        self.grades_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.grades_table)

        self.views_stack.addWidget(view)

    # 3. SYLLABUS & REVISION MATRIX VIEW
    def init_syllabus_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24); lay.setSpacing(16)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Exam Syllabus & Revision Matrix", self))
        hdr_lay.addStretch()
        btn_add_unit = QPushButton("📚 + Add Syllabus Unit", self); btn_add_unit.setProperty("class", "primary"); btn_add_unit.clicked.connect(self.open_syllabus_dialog)
        hdr_lay.addWidget(btn_add_unit)
        lay.addLayout(hdr_lay)

        prog_card = QFrame(self); prog_card.setProperty("class", "card"); pc_lay = QVBoxLayout(prog_card)
        self.lbl_syl_summary = QLabel("Syllabus Revision Progress: 0 of 0 Units Completed (0%)", self); self.lbl_syl_summary.setStyleSheet("font-weight: bold; color: #ffffff;")
        pc_lay.addWidget(self.lbl_syl_summary)
        self.syl_progress_bar = QProgressBar(self); self.syl_progress_bar.setFixedHeight(8)
        pc_lay.addWidget(self.syl_progress_bar)
        lay.addWidget(prog_card)

        self.syl_table = QTableWidget(self)
        self.syl_table.setColumnCount(5)
        self.syl_table.setHorizontalHeaderLabels(["Subject", "Unit / Topic Title", "Revision Status", "Notes", "Actions"])
        self.syl_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.syl_table)

        self.views_stack.addWidget(view)

    # 4. TASKS & POMODORO VIEW
    def init_tasks_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Task Tracker & Pomodoro Focus Timer", self))
        hdr_lay.addStretch()
        btn_new_task = QPushButton("+ Create Goal / Task", self); btn_new_task.setProperty("class", "primary"); btn_new_task.clicked.connect(lambda: self.open_task_dialog())
        hdr_lay.addWidget(btn_new_task)
        lay.addLayout(hdr_lay)

        top_split = QHBoxLayout()

        prog_card = QFrame(self); prog_card.setProperty("class", "card"); pc_lay = QVBoxLayout(prog_card)
        self.lbl_task_summary = QLabel("Task Completion Progress: 0 of 0 Tasks Completed (0%)", self); self.lbl_task_summary.setStyleSheet("font-weight: bold; color: #ffffff;")
        pc_lay.addWidget(self.lbl_task_summary)
        self.task_progress_bar = QProgressBar(self); self.task_progress_bar.setFixedHeight(8)
        pc_lay.addWidget(self.task_progress_bar)
        top_split.addWidget(prog_card, stretch=2)

        pomo_card = QFrame(self); pomo_card.setProperty("class", "card"); po_lay = QVBoxLayout(pomo_card)
        po_lay.addWidget(QLabel("⏱️ POMODORO FOCUS TIMER", self))
        self.lbl_pomo_clock = QLabel("25:00", self); self.lbl_pomo_clock.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981;")
        po_lay.addWidget(self.lbl_pomo_clock, alignment=Qt.AlignmentFlag.AlignCenter)

        pomo_btn_lay = QHBoxLayout()
        self.btn_pomo_toggle = QPushButton("Start Focus", self); self.btn_pomo_toggle.setProperty("class", "success"); self.btn_pomo_toggle.clicked.connect(self.toggle_pomo)
        btn_pomo_reset = QPushButton("Reset", self); btn_pomo_reset.clicked.connect(self.reset_pomo)
        pomo_btn_lay.addWidget(self.btn_pomo_toggle); pomo_btn_lay.addWidget(btn_pomo_reset)
        po_lay.addLayout(pomo_btn_lay)

        top_split.addWidget(pomo_card, stretch=1)
        lay.addLayout(top_split)

        self.tasks_table = QTableWidget(self)
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["Title", "Category", "Due Date", "Priority", "Status", "Description", "Actions"])
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.tasks_table)

        self.views_stack.addWidget(view)

    def toggle_pomo(self):
        if self.pomo_is_running:
            self.pomo_timer.stop(); self.pomo_is_running = False; self.btn_pomo_toggle.setText("Resume Focus")
        else:
            self.pomo_timer.start(1000); self.pomo_is_running = True; self.btn_pomo_toggle.setText("Pause")

    def reset_pomo(self):
        self.pomo_timer.stop(); self.pomo_is_running = False; self.pomo_seconds = 25 * 60
        self.lbl_pomo_clock.setText("25:00"); self.btn_pomo_toggle.setText("Start Focus")

    def pomo_tick(self):
        if self.pomo_seconds > 0:
            self.pomo_seconds -= 1
            mins = self.pomo_seconds // 60; secs = self.pomo_seconds % 60
            self.lbl_pomo_clock.setText(f"{mins:02d}:{secs:02d}")
        else:
            self.reset_pomo()
            self.send_notification("Pomodoro Completed! 🍅", "Great 25-minute focus session! Take a 5-minute break.")

    # 5. ATTENDANCE & BUNK SAFETY CALCULATOR VIEW
    def init_attendance_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Attendance Tracker & Bunk Safety Calculator", self))
        hdr_lay.addStretch()

        self.att_sem_combo = QComboBox(self)
        for i in range(1, 11): self.att_sem_combo.addItem(f"Semester {i}", i)
        self.att_sem_combo.currentIndexChanged.connect(self.refresh_attendance_table)
        hdr_lay.addWidget(self.att_sem_combo)

        btn_add_sub = QPushButton("+ Add Subject", self); btn_add_sub.clicked.connect(self.open_subject_dialog)
        hdr_lay.addWidget(btn_add_sub)
        lay.addLayout(hdr_lay)

        self.sub_cards_area = QWidget(self)
        self.sub_cards_lay = QGridLayout(self.sub_cards_area)
        lay.addWidget(self.sub_cards_area)

        self.att_search = QLineEdit(self); self.att_search.setPlaceholderText("Search subject or date..."); self.att_search.textChanged.connect(self.refresh_attendance_table)
        lay.addWidget(self.att_search)

        self.att_table = QTableWidget(self)
        self.att_table.setColumnCount(6)
        self.att_table.setHorizontalHeaderLabels(["Date", "Semester", "Subject", "Status", "Remarks", "Actions"])
        self.att_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.att_table)

        self.views_stack.addWidget(view)

    # 6. FINANCE & TARGETED SAVINGS VIEW
    def init_finance_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24); lay.setSpacing(16)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Finance Ledger & Targeted Savings Goals", self))
        hdr_lay.addStretch()

        btn_add_sg = QPushButton("🎯 + New Savings Goal", self); btn_add_sg.setProperty("class", "success"); btn_add_sg.clicked.connect(self.open_savings_goal_dialog)
        hdr_lay.addWidget(btn_add_sg)

        btn_rec_allow = QPushButton("+ Receive Allowance", self); btn_rec_allow.clicked.connect(lambda: self.open_finance_dialog("Income"))
        hdr_lay.addWidget(btn_rec_allow)

        btn_log_exp = QPushButton("+ Log Expense", self); btn_log_exp.setProperty("class", "primary"); btn_log_exp.clicked.connect(lambda: self.open_finance_dialog("Expense"))
        hdr_lay.addWidget(btn_log_exp)

        lay.addLayout(hdr_lay)

        sg_header = QLabel("🎯 TARGETED SAVINGS GOALS & WISHLIST", self); sg_header.setProperty("class", "h3")
        lay.addWidget(sg_header)

        self.savings_cards_area = QWidget(self)
        self.savings_cards_lay = QGridLayout(self.savings_cards_area)
        lay.addWidget(self.savings_cards_area)

        graph_card = QFrame(self); graph_card.setProperty("class", "card")
        gc_lay = QVBoxLayout(graph_card); gc_lay.setContentsMargins(10, 10, 10, 10)

        self.finance_canvas = FinanceChartCanvas(self, width=9, height=3.0, dpi=100)
        gc_lay.addWidget(self.finance_canvas)
        lay.addWidget(graph_card)

        self.fin_search = QLineEdit(self); self.fin_search.setPlaceholderText("Search transaction description or category..."); self.fin_search.textChanged.connect(self.refresh_finance_table)
        lay.addWidget(self.fin_search)

        self.fin_table = QTableWidget(self)
        self.fin_table.setColumnCount(6)
        self.fin_table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Description", "Amount (₹)", "Actions"])
        self.fin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.fin_table)

        self.views_stack.addWidget(view)

    # 7. TIMETABLE VIEW
    def init_timetable_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Weekly Lecture Timetable", self))
        hdr_lay.addStretch()
        btn_add_slot = QPushButton("+ Add Class Slot", self); btn_add_slot.clicked.connect(self.open_timetable_dialog)
        hdr_lay.addWidget(btn_add_slot)
        lay.addLayout(hdr_lay)

        self.tt_table = QTableWidget(self)
        self.tt_table.setColumnCount(6)
        self.tt_table.setHorizontalHeaderLabels(["Day", "Time", "Subject", "Location", "Instructor", "Actions"])
        self.tt_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.tt_table)

        self.views_stack.addWidget(view)

    # 8. MEMORIES VIEW
    def init_memories_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Campus Memories Vault", self))
        hdr_lay.addStretch()
        btn_imp_photo = QPushButton("+ Import Photo", self); btn_imp_photo.clicked.connect(self.import_photo_dialog)
        hdr_lay.addWidget(btn_imp_photo)
        lay.addLayout(hdr_lay)

        self.mem_list = QListWidget(self)
        self.mem_list.setIconSize(QSize(160, 120))
        self.mem_list.setViewMode(QListWidget.ViewMode.IconMode)
        lay.addWidget(self.mem_list)

        self.views_stack.addWidget(view)

    # 9. MILESTONES VIEW
    def init_milestones_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Academic Milestones", self))
        hdr_lay.addStretch()
        btn_add_ms = QPushButton("+ Add Milestone", self); btn_add_ms.clicked.connect(self.open_milestone_dialog)
        hdr_lay.addWidget(btn_add_ms)
        lay.addLayout(hdr_lay)

        self.ms_table = QTableWidget(self)
        self.ms_table.setColumnCount(5)
        self.ms_table.setHorizontalHeaderLabels(["Date", "Category", "Title", "Description", "Actions"])
        self.ms_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.ms_table)

        self.views_stack.addWidget(view)

    # REFRESH VIEWS & CALCULATORS
    def refresh_all_views(self):
        self.data = db.get_all_data()
        self.profile = db.get_profile()

        self.lbl_prof_name.setText(self.profile['name'])
        self.lbl_prof_course.setText(self.profile['course'])
        self.lbl_prof_college.setText(self.profile['college'])

        self.lbl_drawer_student.setText(self.profile['name'])
        self.lbl_drawer_college.setText(self.profile['college'])

        target_att = self.profile.get('targetAttendancePct', 75.0)
        self.lbl_drawer_min_att.setText(f"{target_att:.1f}% Minimum Required")

        try:
            j_start = datetime.strptime(self.profile.get('startDate', '2026-08-01'), "%Y-%m-%d")
            j_end = datetime.strptime(self.profile.get('endDate', '2031-07-31'), "%Y-%m-%d")
        except ValueError:
            j_start = datetime(2026, 8, 1); j_end = datetime(2031, 7, 31)

        total_days = max(1, (j_end - j_start).days)
        today = datetime.now()

        elapsed = (today - j_start).days if today > j_start else 0
        elapsed = max(0, min(total_days, elapsed))
        days_left = max(0, total_days - elapsed)
        pct = (elapsed / total_days) * 100.0

        self.lbl_journey_dates.setText(f"{self.profile['course']} Journey ({self.profile.get('startDate')} to {self.profile.get('endDate')})")
        self.hero_progress.setValue(int(pct))
        self.lbl_days_elapsed.setText(f"{elapsed} Days Completed")
        self.lbl_degree_pct.setText(f"{pct:.1f}% Degree Completion")
        self.lbl_days_left.setText(f"{days_left} Days Remaining")
        self.lbl_drawer_days.setText(f"{days_left} Days Left")

        # 1. CGPA & SGPA Calculations
        grades = self.data.get('grades', [])
        total_pts = sum(g['credits'] * g['gradePoints'] for g in grades)
        total_creds = sum(g['credits'] for g in grades)
        cgpa = (total_pts / total_creds) if total_creds > 0 else 0.00
        self.kpi_cgpa_val.setText(f"{cgpa:.2f}")
        self.lbl_cgpa_current.setText(f"Current CGPA: {cgpa:.2f}")

        target_cgpa = self.profile.get('targetCgpa', 8.5)
        self.lbl_cgpa_target.setText(f"Target CGPA: {target_cgpa:.2f}")

        tot_sems = self.profile.get('totalSemesters', 10)
        done_sems = max(1, max((g['sem'] for g in grades), default=1))
        rem_sems = max(1, tot_sems - done_sems)

        req_sgpa = ((target_cgpa * tot_sems) - (cgpa * done_sems)) / rem_sems
        if req_sgpa > 10.0:
            self.lbl_cgpa_needed.setText(f"Target unreachable (requires SGPA > 10.0 in remaining {rem_sems} sems)")
        elif req_sgpa <= 0:
            self.lbl_cgpa_needed.setText(f"Target already achieved! Maintain steady performance.")
        else:
            self.lbl_cgpa_needed.setText(f"Need average SGPA of {req_sgpa:.2f} in remaining {rem_sems} semesters")

        sgpa_list = []
        for s in range(1, done_sems + 1):
            sem_g = [g for g in grades if g['sem'] == s]
            s_pts = sum(g['credits'] * g['gradePoints'] for g in sem_g)
            s_creds = sum(g['credits'] for g in sem_g)
            if s_creds > 0:
                sgpa_list.append({'sem': s, 'sgpa': round(s_pts / s_creds, 2)})

        self.cgpa_canvas.update_chart(sgpa_list)

        # 2. Attendance KPI
        logs = self.data['attendanceLogs']
        p_count = sum(1 for l in logs if l['status'] == 'Present')
        att_pct = (p_count / len(logs) * 100.0) if logs else 0.0
        self.kpi_att_val.setText(f"{att_pct:.1f}%")

        # 3. Targeted Savings KPI
        savings = self.data.get('savingsGoals', [])
        total_saved = sum(sg['currentSaved'] for sg in savings)
        self.kpi_savings_val.setText(f"₹{total_saved:,.0f}")

        # 4. Syllabus KPI
        syl = self.data.get('syllabus', [])
        c_syl = sum(1 for item in syl if item['status'] == 'Completed')
        syl_pct = (c_syl / len(syl) * 100.0) if syl else 0.0
        self.kpi_syl_val.setText(f"{syl_pct:.0f}%")
        self.lbl_syl_summary.setText(f"Syllabus Revision Progress: {c_syl} of {len(syl)} Units Completed ({syl_pct:.0f}%)")
        self.syl_progress_bar.setValue(int(syl_pct))

        # 5. Wallet KPI
        inc = sum(f['amount'] for f in self.data['finances'] if f['type'] == 'Income')
        exp = sum(f['amount'] for f in self.data['finances'] if f['type'] == 'Expense')

        budget_cap = self.profile.get('monthlyBudgetCap', 5000.0)
        if exp > budget_cap:
            self.send_notification("Monthly Budget Alert! ⚠️", f"Expenses (₹{exp:,.0f}) exceeded your cap of ₹{budget_cap:,.0f}!")

        # 6. Tasks KPI
        tasks = self.data['tasks']
        c_tasks = sum(1 for t in tasks if t['status'] == 'Completed')
        t_pct = (c_tasks / len(tasks) * 100.0) if tasks else 0.0
        self.kpi_task_val.setText(f"{t_pct:.0f}%")
        self.lbl_task_summary.setText(f"Task Completion Progress: {c_tasks} of {len(tasks)} Tasks Completed ({t_pct:.0f}%)")
        self.task_progress_bar.setValue(int(t_pct))

        self.refresh_syllabus_table()
        self.refresh_savings_goals_cards()
        self.refresh_grades_table()
        self.refresh_tasks_table()
        self.refresh_attendance_table()
        self.refresh_finance_table()
        self.refresh_timetable_table()
        self.refresh_memories_grid()
        self.refresh_milestones_table()

        self.finance_canvas.update_charts(self.data['finances'])

    # SYLLABUS TABLE
    def refresh_syllabus_table(self):
        syl = self.data.get('syllabus', [])
        self.syl_table.setRowCount(len(syl))
        for row, item in enumerate(syl):
            self.syl_table.setItem(row, 0, QTableWidgetItem(item['subjectName']))
            self.syl_table.setItem(row, 1, QTableWidgetItem(item['unitName']))
            self.syl_table.setItem(row, 2, QTableWidgetItem(item['status']))
            self.syl_table.setItem(row, 3, QTableWidgetItem(item.get('notes', '')))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            btn_toggle = QPushButton("Toggle Done", self); btn_toggle.setProperty("class", "success")
            btn_toggle.clicked.connect(lambda checked, s_item=item: self.toggle_syllabus_status(s_item))
            act_lay.addWidget(btn_toggle)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, s_item=item: self.open_syllabus_dialog(s_item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, sid=item['id']: self.delete_syllabus(sid))
            act_lay.addWidget(btn_del)

            self.syl_table.setCellWidget(row, 4, act_widget)

    def toggle_syllabus_status(self, item):
        item['status'] = 'Completed' if item['status'] != 'Completed' else 'In Progress'
        db.save_syllabus(item)
        self.refresh_all_views()

    def open_syllabus_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Syllabus Unit" if edit_item else "Add Syllabus Unit"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        sub_combo = QComboBox(dlg)
        sub_combo.setEditable(True)
        sub_combo.lineEdit().setPlaceholderText("Type or select subject name...")
        for s in self.data['subjects']: sub_combo.addItem(f"{s['name']} ({s['code']})", s['id'])
        if edit_item:
            sub_combo.setCurrentText(edit_item['subjectName'])

        unit_in = QLineEdit(dlg); unit_in.setText(edit_item['unitName'] if edit_item else "")
        status_combo = QComboBox(dlg); status_combo.addItems(["Pending", "In Progress", "Completed"])
        if edit_item:
            s_idx = status_combo.findText(edit_item['status'])
            if s_idx != -1: status_combo.setCurrentIndex(s_idx)

        notes_in = QLineEdit(dlg); notes_in.setText(edit_item.get('notes', '') if edit_item else "")

        lay.addWidget(QLabel("Subject:", dlg)); lay.addWidget(sub_combo)
        lay.addWidget(QLabel("Unit / Topic Title:", dlg)); lay.addWidget(unit_in)
        lay.addWidget(QLabel("Status:", dlg)); lay.addWidget(status_combo)
        lay.addWidget(QLabel("Notes:", dlg)); lay.addWidget(notes_in)

        btn_save = QPushButton("Save Unit", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            entered_sub = sub_combo.currentText().strip()
            if unit_in.text() and entered_sub:
                sub_id = sub_combo.currentData()
                sub_obj = next((s for s in self.data['subjects'] if s['id'] == sub_id or s['name'].lower() in entered_sub.lower()), None)
                if not sub_obj:
                    sub_id = f"sub-{int(datetime.now().timestamp())}"
                    sub_obj = {
                        'id': sub_id,
                        'sem': 1,
                        'name': entered_sub,
                        'code': entered_sub[:6].upper(),
                        'faculty': 'Faculty',
                        'targetPct': self.profile.get('targetAttendancePct', 75.0),
                        'color': '#6366f1'
                    }
                    db.save_subject(sub_obj)

                db.save_syllabus({
                    'id': edit_item['id'] if edit_item else f"syl-{int(datetime.now().timestamp())}",
                    'subjectId': sub_obj['id'],
                    'subjectName': entered_sub,
                    'unitName': unit_in.text(),
                    'status': status_combo.currentText(),
                    'notes': notes_in.text()
                })
                dlg.accept()
                self.refresh_all_views()

        btn_save.clicked.connect(save)
        dlg.exec()

    def delete_syllabus(self, sid):
        if QMessageBox.question(self, "Confirm Delete", "Delete syllabus unit?") == QMessageBox.StandardButton.Yes:
            db.delete_syllabus(sid)
            self.refresh_all_views()

    # FORMATTED PDF REPORT EXPORTER
    def export_pdf_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Academic & Financial Report", "STUNT_Academic_Report.html", "HTML Document (*.html);;All Files (*)")
        if file_path:
            p = self.profile
            inc = sum(f['amount'] for f in self.data['finances'] if f['type'] == 'Income')
            exp = sum(f['amount'] for f in self.data['finances'] if f['type'] == 'Expense')
            grades = self.data.get('grades', [])
            total_pts = sum(g['credits'] * g['gradePoints'] for g in grades)
            total_creds = sum(g['credits'] for g in grades)
            cgpa = (total_pts / total_creds) if total_creds > 0 else 0.00

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #0a0b10; color: #f8fafc; padding: 40px; }}
                    h1 {{ color: #6366f1; border-bottom: 2px solid #6366f1; padding-bottom: 10px; }}
                    .card {{ background: #181a27; border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ border: 1px solid rgba(255,255,255,0.1); padding: 10px; text-align: left; }}
                    th {{ background: #121420; color: #0ea5e9; }}
                </style>
            </head>
            <body>
                <h1>STUNT Academic & Financial Transcript</h1>
                <div class="card">
                    <h2>Student Profile</h2>
                    <p><b>Name:</b> {p.get('name')} | <b>College:</b> {p.get('college')}</p>
                    <p><b>Course:</b> {p.get('course')} | <b>Batch:</b> {p.get('batch')}</p>
                    <p><b>Cumulative CGPA:</b> {cgpa:.2f} | <b>Target CGPA:</b> {p.get('targetCgpa')}</p>
                    <p><b>Net Wallet Balance:</b> ₹{inc - exp:,.0f} | <b>Monthly Budget Cap:</b> ₹{p.get('monthlyBudgetCap'):,.0f}</p>
                </div>

                <div class="card">
                    <h2>Subject Grades Ledger</h2>
                    <table>
                        <tr><th>Semester</th><th>Code</th><th>Subject Name</th><th>Credits</th><th>Grade Points</th></tr>
                        {''.join(f"<tr><td>Sem {g['sem']}</td><td>{g['subjectCode']}</td><td>{g['subjectName']}</td><td>{g['credits']}</td><td>{g['gradePoints']}</td></tr>" for g in grades)}
                    </table>
                </div>

                <div class="card">
                    <h2>Targeted Savings Goals</h2>
                    <table>
                        <tr><th>Goal Item</th><th>Category</th><th>Target Amount</th><th>Current Saved</th><th>Target Date</th></tr>
                        {''.join(f"<tr><td>{sg['title']}</td><td>{sg['category']}</td><td>₹{sg['targetAmount']:,.0f}</td><td>₹{sg['currentSaved']:,.0f}</td><td>{sg['targetDate']}</td></tr>" for sg in self.data.get('savingsGoals', []))}
                    </table>
                </div>
            </body>
            </html>
            """
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            QMessageBox.information(self, "Export Complete", f"Academic Transcript exported to {file_path}!\nYou can open and print it directly from your web browser.")

    # TARGETED SAVINGS GOALS CARDS RENDERER
    def refresh_savings_goals_cards(self):
        for i in reversed(range(self.savings_cards_lay.count())):
            item = self.savings_cards_lay.itemAt(i)
            if item.widget(): item.widget().setParent(None)

        savings = self.data.get('savingsGoals', [])
        if not savings:
            lbl_empty = QLabel("No savings goals created yet. Click '+ New Savings Goal' to add items you want to save for!", self)
            lbl_empty.setStyleSheet("color: #64748b; font-style: italic;")
            self.savings_cards_lay.addWidget(lbl_empty, 0, 0)
            return

        for idx, sg in enumerate(savings):
            target = max(1.0, sg['targetAmount'])
            saved = sg['currentSaved']
            pct = min(100.0, (saved / target) * 100.0)

            card = QFrame(self); card.setProperty("class", "card")
            c_lay = QVBoxLayout(card)

            hdr = QHBoxLayout()
            hdr.addWidget(QLabel(f"🎯 <b>{sg['title']}</b> ({sg['category']})", self))
            hdr.addStretch()

            lbl_date = QLabel(f"Target: {sg['targetDate']}", self); lbl_date.setStyleSheet("font-size: 11px; color: #94a3b8;")
            hdr.addWidget(lbl_date)
            c_lay.addLayout(hdr)

            pbar = QProgressBar(self); pbar.setFixedHeight(8); pbar.setValue(int(pct))
            c_lay.addWidget(pbar)

            met_lay = QHBoxLayout()
            lbl_amt = QLabel(f"Saved: <b>₹{saved:,.0f}</b> / ₹{target:,.0f} ({pct:.1f}%)", self)
            lbl_amt.setStyleSheet("color: #10b981;" if pct >= 100 else "color: #0ea5e9;")
            met_lay.addWidget(lbl_amt)
            met_lay.addStretch()

            btn_dep = QPushButton("💵 Deposit Funds", self); btn_dep.setProperty("class", "success")
            btn_dep.clicked.connect(lambda checked, item=sg: self.open_deposit_dialog(item))
            met_lay.addWidget(btn_dep)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=sg: self.open_savings_goal_dialog(item))
            met_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, sgid=sg['id']: self.delete_savings_goal(sgid))
            met_lay.addWidget(btn_del)

            c_lay.addLayout(met_lay)
            self.savings_cards_lay.addWidget(card, idx // 2, idx % 2)

    def open_deposit_dialog(self, sg_item):
        dlg = QDialog(self); dlg.setWindowTitle(f"Deposit Funds to '{sg_item['title']}'"); dlg.setFixedWidth(340)
        lay = QVBoxLayout(dlg)

        lay.addWidget(QLabel(f"Target: ₹{sg_item['targetAmount']:,.0f} | Currently Saved: ₹{sg_item['currentSaved']:,.0f}", dlg))

        amt_in = QLineEdit(dlg); amt_in.setPlaceholderText("Enter deposit amount (₹)...")
        lay.addWidget(QLabel("Deposit Amount (₹):", dlg)); lay.addWidget(amt_in)

        btn_save = QPushButton("Confirm Deposit", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            try:
                dep = float(amt_in.text())
                sg_item['currentSaved'] += dep
                db.save_savings_goal(sg_item)

                db.save_finance({
                    'id': f"fin-{int(datetime.now().timestamp())}",
                    'type': 'Expense',
                    'category': 'Personal Supplies',
                    'amount': dep,
                    'desc': f"Savings Deposit towards '{sg_item['title']}'",
                    'date': date.today().strftime("%Y-%m-%d")
                })

                dlg.accept()
                self.refresh_all_views()
                if sg_item['currentSaved'] >= sg_item['targetAmount']:
                    celeb = TaskCelebrationWindow(sg_item['title'], self, is_savings=True)
                    celeb.exec()
                    self.send_notification("Savings Goal Reached! 🎉", f"You saved enough funds for '{sg_item['title']}'!")
                else:
                    self.send_notification("Savings Updated 💰", f"Added ₹{dep:,.0f} to '{sg_item['title']}'")
            except ValueError:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid number.")

        btn_save.clicked.connect(save)
        dlg.exec()

    def open_savings_goal_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Savings Goal" if edit_item else "New Targeted Savings Goal"); dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)

        title_in = QLineEdit(dlg); title_in.setText(edit_item['title'] if edit_item else "")
        title_in.setPlaceholderText("e.g. New Laptop, Smartphone, Trip")

        target_in = QLineEdit(dlg); target_in.setText(str(edit_item['targetAmount']) if edit_item else "")
        target_in.setPlaceholderText("Target Purchase Price (₹)")

        saved_in = QLineEdit(dlg); saved_in.setText(str(edit_item['currentSaved']) if edit_item else "0")

        cat_combo = QComboBox(dlg); cat_combo.addItems(["Electronics", "Tech Accessory", "Books & Courses", "Travel & Trip", "Personal Wishlist", "Other"])
        if edit_item:
            idx = cat_combo.findText(edit_item['category'])
            if idx != -1: cat_combo.setCurrentIndex(idx)

        date_in = QLineEdit(dlg); date_in.setText(edit_item['targetDate'] if edit_item else "2026-12-31")
        notes_in = QLineEdit(dlg); notes_in.setText(edit_item.get('notes', '') if edit_item else "")

        lay.addWidget(QLabel("Goal / Item Title:", dlg)); lay.addWidget(title_in)
        lay.addWidget(QLabel("Target Amount (₹):", dlg)); lay.addWidget(target_in)
        lay.addWidget(QLabel("Initial Saved Amount (₹):", dlg)); lay.addWidget(saved_in)
        lay.addWidget(QLabel("Category:", dlg)); lay.addWidget(cat_combo)
        lay.addWidget(QLabel("Target Date (YYYY-MM-DD):", dlg)); lay.addWidget(date_in)
        lay.addWidget(QLabel("Notes / Details:", dlg)); lay.addWidget(notes_in)

        btn_save = QPushButton("Save Goal", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            if title_in.text() and target_in.text():
                try:
                    db.save_savings_goal({
                        'id': edit_item['id'] if edit_item else f"sg-{int(datetime.now().timestamp())}",
                        'title': title_in.text(),
                        'targetAmount': float(target_in.text()),
                        'currentSaved': float(saved_in.text() or 0),
                        'targetDate': date_in.text(),
                        'category': cat_combo.currentText(),
                        'notes': notes_in.text()
                    })
                    dlg.accept()
                    self.refresh_all_views()
                    self.send_notification("Savings Goal Saved 🎯", f"Saved goal for '{title_in.text()}'")
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", "Target and Initial saved amounts must be valid numbers.")

        btn_save.clicked.connect(save)
        dlg.exec()

    def delete_savings_goal(self, sgid):
        if QMessageBox.question(self, "Confirm Delete", "Delete this savings goal?") == QMessageBox.StandardButton.Yes:
            db.delete_savings_goal(sgid)
            self.refresh_all_views()

    # GRADES TABLE
    def refresh_grades_table(self):
        grades = self.data.get('grades', [])
        self.grades_table.setRowCount(len(grades))
        for row, g in enumerate(grades):
            self.grades_table.setItem(row, 0, QTableWidgetItem(f"Sem {g['sem']}"))
            self.grades_table.setItem(row, 1, QTableWidgetItem(g['subjectCode']))
            self.grades_table.setItem(row, 2, QTableWidgetItem(g['subjectName']))
            self.grades_table.setItem(row, 3, QTableWidgetItem(str(g['credits'])))
            self.grades_table.setItem(row, 4, QTableWidgetItem(str(g['gradePoints'])))

            btn_del = QPushButton("Delete", self)
            btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, gid=g['id']: self.delete_grade(gid))
            self.grades_table.setCellWidget(row, 5, btn_del)

    def delete_grade(self, gid):
        db.delete_grade(gid)
        self.refresh_all_views()

    # ATTENDANCE BUNK SAFETY CALCULATOR
    def refresh_attendance_table(self):
        target_r = self.profile.get('targetAttendancePct', 75.0) / 100.0
        sem = self.att_sem_combo.currentData() or 1
        subjects = [s for s in self.data['subjects'] if s['sem'] == sem]

        for i in reversed(range(self.sub_cards_lay.count())):
            item = self.sub_cards_lay.itemAt(i)
            if item.widget(): item.widget().setParent(None)

        for col, s in enumerate(subjects):
            logs = [l for l in self.data['attendanceLogs'] if l['subjectId'] == s['id']]
            total = len(logs)
            present = sum(1 for l in logs if l['status'] == 'Present')
            pct = (present / total * 100.0) if total > 0 else 0.0

            card = QFrame(self); card.setProperty("class", "card")
            c_lay = QVBoxLayout(card)

            c_lay.addWidget(QLabel(f"<b>{s['name']}</b> ({s['code']})", self))
            c_lay.addWidget(QLabel(f"Attendance: {present}/{total} ({pct:.1f}%)", self))

            if total == 0:
                badge = QLabel("No classes logged yet", self); badge.setStyleSheet("color: #64748b;")
            elif pct >= (target_r * 100.0):
                safe_bunks = math.floor((present - target_r * total) / target_r)
                badge = QLabel(f"🟢 SAFE: Can bunk {safe_bunks} classes", self)
                badge.setStyleSheet("color: #10b981; font-weight: bold;")
            else:
                must_attend = math.ceil((target_r * total - present) / (1 - target_r))
                badge = QLabel(f"🔴 CRITICAL: Attend next {must_attend} lectures!", self)
                badge.setStyleSheet("color: #f43f5e; font-weight: bold;")

            c_lay.addWidget(badge)
            self.sub_cards_lay.addWidget(card, 0, col)

        query = self.att_search.text().lower() if hasattr(self, 'att_search') else ""
        logs = [l for l in self.data['attendanceLogs'] if not query or query in l['subjectName'].lower() or query in l['date'].lower()]

        self.att_table.setRowCount(len(logs))
        for row, l in enumerate(logs):
            self.att_table.setItem(row, 0, QTableWidgetItem(l['date']))
            self.att_table.setItem(row, 1, QTableWidgetItem(f"Sem {l['sem']}"))
            self.att_table.setItem(row, 2, QTableWidgetItem(l['subjectName']))
            self.att_table.setItem(row, 3, QTableWidgetItem(l['status']))
            self.att_table.setItem(row, 4, QTableWidgetItem(l.get('remarks', '')))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=l: self.open_attendance_dialog(item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, lid=l['id']: self.delete_att(lid))
            act_lay.addWidget(btn_del)

            self.att_table.setCellWidget(row, 5, act_widget)

    def delete_att(self, lid):
        if QMessageBox.question(self, "Confirm Delete", "Delete attendance log?") == QMessageBox.StandardButton.Yes:
            db.delete_attendance(lid)
            self.refresh_all_views()

    # TASKS TABLE
    def refresh_tasks_table(self):
        tasks = self.data['tasks']
        self.tasks_table.setRowCount(len(tasks))
        for row, t in enumerate(tasks):
            self.tasks_table.setItem(row, 0, QTableWidgetItem(t['title']))
            self.tasks_table.setItem(row, 1, QTableWidgetItem(t['category']))
            self.tasks_table.setItem(row, 2, QTableWidgetItem(f"{t['dueDate']} {t.get('dueTime', '')}"))
            self.tasks_table.setItem(row, 3, QTableWidgetItem(t['priority']))
            self.tasks_table.setItem(row, 4, QTableWidgetItem(t['status']))
            self.tasks_table.setItem(row, 5, QTableWidgetItem(t.get('desc', '')))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            if t['status'] != 'Completed':
                btn_done = QPushButton("Complete 🎉", self); btn_done.setProperty("class", "success")
                btn_done.clicked.connect(lambda checked, item=t: self.complete_task(item))
                act_lay.addWidget(btn_done)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=t: self.open_task_dialog(item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, tid=t['id']: self.delete_task(tid))
            act_lay.addWidget(btn_del)

            self.tasks_table.setCellWidget(row, 6, act_widget)

    def complete_task(self, task):
        task['status'] = 'Completed'
        db.save_task(task)
        self.refresh_all_views()
        self.send_notification("Task Accomplished! 🎉", f'Completed: "{task["title"]}"')
        celeb = TaskCelebrationWindow(task['title'], self)
        celeb.exec()

    def delete_task(self, tid):
        if QMessageBox.question(self, "Confirm Delete", "Delete task?") == QMessageBox.StandardButton.Yes:
            db.delete_task(tid)
            self.refresh_all_views()

    # FINANCE TABLE
    def refresh_finance_table(self):
        query = self.fin_search.text().lower() if hasattr(self, 'fin_search') else ""
        fin = [f for f in self.data['finances'] if not query or query in f['desc'].lower() or query in f['category'].lower()]

        self.fin_table.setRowCount(len(fin))
        for row, f in enumerate(fin):
            self.fin_table.setItem(row, 0, QTableWidgetItem(f['date']))
            self.fin_table.setItem(row, 1, QTableWidgetItem(f['type']))
            self.fin_table.setItem(row, 2, QTableWidgetItem(f['category']))
            self.fin_table.setItem(row, 3, QTableWidgetItem(f['desc']))
            self.fin_table.setItem(row, 4, QTableWidgetItem(f"₹{f['amount']:,.0f}"))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=f: self.open_finance_dialog(item['type'], item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, fid=f['id']: self.delete_fin(fid))
            act_lay.addWidget(btn_del)

            self.fin_table.setCellWidget(row, 5, act_widget)

    def delete_fin(self, fid):
        if QMessageBox.question(self, "Confirm Delete", "Delete transaction?") == QMessageBox.StandardButton.Yes:
            db.delete_finance(fid)
            self.refresh_all_views()

    # TIMETABLE TABLE
    def refresh_timetable_table(self):
        tt = self.data['timetable']
        self.tt_table.setRowCount(len(tt))
        for row, t in enumerate(tt):
            self.tt_table.setItem(row, 0, QTableWidgetItem(t['day']))
            self.tt_table.setItem(row, 1, QTableWidgetItem(f"{t['start']} - {t['end']}"))
            self.tt_table.setItem(row, 2, QTableWidgetItem(t['subject']))
            self.tt_table.setItem(row, 3, QTableWidgetItem(t['location']))
            self.tt_table.setItem(row, 4, QTableWidgetItem(t['instructor']))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=t: self.open_timetable_dialog(item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, tid=t['id']: self.delete_tt(tid))
            act_lay.addWidget(btn_del)

            self.tt_table.setCellWidget(row, 5, act_widget)

    def delete_tt(self, tid):
        if QMessageBox.question(self, "Confirm Delete", "Delete slot?") == QMessageBox.StandardButton.Yes:
            db.delete_timetable(tid)
            self.refresh_all_views()

    def refresh_memories_grid(self):
        self.mem_list.clear()
        for m in self.data['memories']:
            item = QListWidgetItem(m['title'])
            if m['src'].startswith('data:image'):
                header, encoded = m['src'].split(",", 1)
                data = base64.b64decode(encoded)
                img = QImage()
                img.loadFromData(data)
                item.setIcon(QIcon(QPixmap.fromImage(img)))
            elif os.path.exists(m['src']):
                item.setIcon(QIcon(m['src']))
            self.mem_list.addItem(item)

    # MILESTONES TABLE
    def refresh_milestones_table(self):
        ms = self.data['milestones']
        self.ms_table.setRowCount(len(ms))
        for row, m in enumerate(ms):
            self.ms_table.setItem(row, 0, QTableWidgetItem(m['date']))
            self.ms_table.setItem(row, 1, QTableWidgetItem(m['category']))
            self.ms_table.setItem(row, 2, QTableWidgetItem(m['title']))
            self.ms_table.setItem(row, 3, QTableWidgetItem(m.get('desc', '')))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=m: self.open_milestone_dialog(item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, mid=m['id']: self.delete_ms(mid))
            act_lay.addWidget(btn_del)

            self.ms_table.setCellWidget(row, 4, act_widget)

    def delete_ms(self, mid):
        if QMessageBox.question(self, "Confirm Delete", "Delete milestone?") == QMessageBox.StandardButton.Yes:
            db.delete_milestone(mid)
            self.refresh_all_views()

    # DIALOG OPENERS
    def open_grade_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Subject Grade" if edit_item else "Log Subject Grade"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        sem_in = QLineEdit(dlg); sem_in.setText(str(edit_item['sem']) if edit_item else "1")
        code_in = QLineEdit(dlg); code_in.setText(edit_item['subjectCode'] if edit_item else "")
        name_in = QLineEdit(dlg); name_in.setText(edit_item['subjectName'] if edit_item else "")
        cred_in = QLineEdit(dlg); cred_in.setText(str(edit_item['credits']) if edit_item else "4")

        gp_combo = QComboBox(dlg)
        grades_map = [("O (Outstanding - 10)", 10), ("A+ (Excellent - 9)", 9), ("A (Very Good - 8)", 8), ("B+ (Good - 7)", 7), ("B (Above Avg - 6)", 6), ("C (Average - 5)", 5), ("F (Fail - 0)", 0)]
        for label, val in grades_map: gp_combo.addItem(label, val)

        lay.addWidget(QLabel("Semester:", dlg)); lay.addWidget(sem_in)
        lay.addWidget(QLabel("Subject Code:", dlg)); lay.addWidget(code_in)
        lay.addWidget(QLabel("Subject Title:", dlg)); lay.addWidget(name_in)
        lay.addWidget(QLabel("Credit Hours:", dlg)); lay.addWidget(cred_in)
        lay.addWidget(QLabel("Grade Scored:", dlg)); lay.addWidget(gp_combo)

        btn_save = QPushButton("Save Grade Record", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            try:
                db.save_grade({
                    'id': edit_item['id'] if edit_item else f"gr-{int(datetime.now().timestamp())}",
                    'sem': int(sem_in.text()),
                    'subjectCode': code_in.text(),
                    'subjectName': name_in.text(),
                    'credits': int(cred_in.text()),
                    'gradePoints': gp_combo.currentData()
                })
                dlg.accept()
                self.refresh_all_views()
            except ValueError:
                pass

        btn_save.clicked.connect(save)
        dlg.exec()

    def open_task_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Task / Goal" if edit_item else "Create Task / Goal"); dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)

        title_in = QLineEdit(dlg); title_in.setText(edit_item['title'] if edit_item else "")
        cat_combo = QComboBox(dlg); cat_combo.addItems(["Assignment", "Project", "Exam Prep", "Daily Goal", "Personal Task"])
        if edit_item:
            c_idx = cat_combo.findText(edit_item['category'])
            if c_idx != -1: cat_combo.setCurrentIndex(c_idx)

        date_in = QLineEdit(dlg); date_in.setText(edit_item['dueDate'] if edit_item else date.today().strftime("%Y-%m-%d"))
        time_in = QLineEdit(dlg); time_in.setText(edit_item.get('dueTime', '11:59 PM') if edit_item else "11:59 PM")

        prio_combo = QComboBox(dlg); prio_combo.addItems(["High", "Medium", "Low"])
        if edit_item:
            p_idx = prio_combo.findText(edit_item['priority'])
            if p_idx != -1: prio_combo.setCurrentIndex(p_idx)

        desc_in = QLineEdit(dlg); desc_in.setText(edit_item.get('desc', '') if edit_item else "")

        lay.addWidget(QLabel("Task Title:", dlg)); lay.addWidget(title_in)
        lay.addWidget(QLabel("Category:", dlg)); lay.addWidget(cat_combo)
        lay.addWidget(QLabel("Due Date (YYYY-MM-DD):", dlg)); lay.addWidget(date_in)
        lay.addWidget(QLabel("Due Time:", dlg)); lay.addWidget(time_in)
        lay.addWidget(QLabel("Priority:", dlg)); lay.addWidget(prio_combo)
        lay.addWidget(QLabel("Description:", dlg)); lay.addWidget(desc_in)

        btn_save = QPushButton("Save Task", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            if title_in.text():
                db.save_task({
                    'id': edit_item['id'] if edit_item else f"task-{int(datetime.now().timestamp())}",
                    'title': title_in.text(),
                    'category': cat_combo.currentText(),
                    'dueDate': date_in.text(),
                    'dueTime': time_in.text(),
                    'priority': prio_combo.currentText(),
                    'status': edit_item['status'] if edit_item else 'Pending',
                    'desc': desc_in.text()
                })
                dlg.accept()
                self.refresh_all_views()
                self.send_notification("Task Saved 📌", f'Saved goal: "{title_in.text()}"')

        btn_save.clicked.connect(save)
        dlg.exec()

    def open_subject_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Subject" if edit_item else "Add Academic Subject"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        name_in = QLineEdit(dlg); name_in.setText(edit_item['name'] if edit_item else "")
        code_in = QLineEdit(dlg); code_in.setText(edit_item['code'] if edit_item else "")
        fac_in = QLineEdit(dlg); fac_in.setText(edit_item['faculty'] if edit_item else "")

        lay.addWidget(QLabel("Subject Title:", dlg)); lay.addWidget(name_in)
        lay.addWidget(QLabel("Subject Code:", dlg)); lay.addWidget(code_in)
        lay.addWidget(QLabel("Faculty:", dlg)); lay.addWidget(fac_in)

        btn_save = QPushButton("Save Subject", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            if name_in.text() and code_in.text():
                db.save_subject({
                    'id': edit_item['id'] if edit_item else f"sub-{int(datetime.now().timestamp())}",
                    'sem': edit_item['sem'] if edit_item else (self.att_sem_combo.currentData() or 1),
                    'name': name_in.text(),
                    'code': code_in.text(),
                    'faculty': fac_in.text() or 'Faculty',
                    'targetPct': self.profile.get('targetAttendancePct', 75.0),
                    'color': '#6366f1'
                })
                dlg.accept()
                self.refresh_all_views()

        btn_save.clicked.connect(save)
        dlg.exec()

    # EDITABLE WRITE-BY ATTENDANCE DIALOG
    def open_attendance_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Attendance Record" if edit_item else "Log Attendance Record"); dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)

        sub_combo = QComboBox(dlg)
        sub_combo.setEditable(True)
        sub_combo.lineEdit().setPlaceholderText("Write or select subject name...")

        for s in self.data['subjects']:
            sub_combo.addItem(f"{s['name']} ({s['code']})", s['id'])

        if edit_item:
            sub_combo.setCurrentText(edit_item['subjectName'])

        status_combo = QComboBox(dlg); status_combo.addItems(["Present", "Absent", "Leave", "Holiday"])
        if edit_item:
            s_idx = status_combo.findText(edit_item['status'])
            if s_idx != -1: status_combo.setCurrentIndex(s_idx)

        date_in = QLineEdit(dlg); date_in.setText(edit_item['date'] if edit_item else date.today().strftime("%Y-%m-%d"))
        rem_in = QLineEdit(dlg); rem_in.setText(edit_item.get('remarks', '') if edit_item else "")

        lay.addWidget(QLabel("Subject Name (Write or Select):", dlg)); lay.addWidget(sub_combo)
        lay.addWidget(QLabel("Status:", dlg)); lay.addWidget(status_combo)
        lay.addWidget(QLabel("Date (YYYY-MM-DD):", dlg)); lay.addWidget(date_in)
        lay.addWidget(QLabel("Remarks / Topic / Lab:", dlg)); lay.addWidget(rem_in)

        btn_save = QPushButton("Save Attendance Record", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            entered_sub = sub_combo.currentText().strip()
            if entered_sub:
                sub_id = sub_combo.currentData()
                sub_obj = next((s for s in self.data['subjects'] if s['id'] == sub_id or s['name'].lower() in entered_sub.lower()), None)
                if not sub_obj:
                    sub_id = f"sub-{int(datetime.now().timestamp())}"
                    sub_obj = {
                        'id': sub_id,
                        'sem': self.att_sem_combo.currentData() or 1,
                        'name': entered_sub,
                        'code': entered_sub[:6].upper(),
                        'faculty': 'Faculty',
                        'targetPct': self.profile.get('targetAttendancePct', 75.0),
                        'color': '#6366f1'
                    }
                    db.save_subject(sub_obj)

                db.save_attendance({
                    'id': edit_item['id'] if edit_item else f"att-{int(datetime.now().timestamp())}",
                    'sem': sub_obj['sem'],
                    'subjectId': sub_obj['id'],
                    'subjectName': entered_sub,
                    'date': date_in.text(),
                    'status': status_combo.currentText(),
                    'remarks': rem_in.text()
                })
                dlg.accept()
                self.refresh_all_views()
                self.send_notification("Attendance Recorded 📋", f'{status_combo.currentText()} logged for {entered_sub}')
            else:
                QMessageBox.warning(dlg, "Missing Subject", "Please write or select a subject name.")

        btn_save.clicked.connect(save)
        dlg.exec()

    def open_finance_dialog(self, ftype="Expense", edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Transaction" if edit_item else f"Log {ftype}"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        cat_combo = QComboBox(dlg)
        cats = ["Food & Dining", "Transport & Transit", "Academics & Books", "Entertainment", "Personal Supplies", "Monthly Allowance", "Miscellaneous"]
        cat_combo.addItems(cats)
        if edit_item:
            c_idx = cat_combo.findText(edit_item['category'])
            if c_idx != -1: cat_combo.setCurrentIndex(c_idx)

        amt_in = QLineEdit(dlg); amt_in.setText(str(edit_item['amount']) if edit_item else "")
        desc_in = QLineEdit(dlg); desc_in.setText(edit_item['desc'] if edit_item else "")
        date_in = QLineEdit(dlg); date_in.setText(edit_item['date'] if edit_item else date.today().strftime("%Y-%m-%d"))

        lay.addWidget(QLabel("Category:", dlg)); lay.addWidget(cat_combo)
        lay.addWidget(QLabel("Amount (₹):", dlg)); lay.addWidget(amt_in)
        lay.addWidget(QLabel("Description:", dlg)); lay.addWidget(desc_in)
        lay.addWidget(QLabel("Date:", dlg)); lay.addWidget(date_in)

        btn_save = QPushButton("Save Transaction", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            try:
                amt = float(amt_in.text())
                db.save_finance({
                    'id': edit_item['id'] if edit_item else f"fin-{int(datetime.now().timestamp())}",
                    'type': ftype,
                    'category': cat_combo.currentText(),
                    'amount': amt,
                    'desc': desc_in.text(),
                    'date': date_in.text()
                })
                dlg.accept()
                self.refresh_all_views()
                self.send_notification("Finance Ledger Updated 💰", f'{ftype} of ₹{amt:,.0f} logged ({cat_combo.currentText()})')
            except ValueError:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid number for amount.")

        btn_save.clicked.connect(save)
        dlg.exec()

    def open_timetable_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Class Slot" if edit_item else "Add Class Slot"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        day_combo = QComboBox(dlg); day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        if edit_item:
            d_idx = day_combo.findText(edit_item['day'])
            if d_idx != -1: day_combo.setCurrentIndex(d_idx)

        sub_in = QLineEdit(dlg); sub_in.setText(edit_item['subject'] if edit_item else "")
        start_in = QLineEdit(dlg); start_in.setText(edit_item['start'] if edit_item else "09:00 AM")
        end_in = QLineEdit(dlg); end_in.setText(edit_item['end'] if edit_item else "10:30 AM")
        loc_in = QLineEdit(dlg); loc_in.setText(edit_item['location'] if edit_item else "")
        inst_in = QLineEdit(dlg); inst_in.setText(edit_item['instructor'] if edit_item else "")

        lay.addWidget(QLabel("Day:", dlg)); lay.addWidget(day_combo)
        lay.addWidget(QLabel("Subject:", dlg)); lay.addWidget(sub_in)
        lay.addWidget(QLabel("Start Time:", dlg)); lay.addWidget(start_in)
        lay.addWidget(QLabel("End Time:", dlg)); lay.addWidget(end_in)
        lay.addWidget(QLabel("Location:", dlg)); lay.addWidget(loc_in)
        lay.addWidget(QLabel("Instructor:", dlg)); lay.addWidget(inst_in)

        btn_save = QPushButton("Save Slot", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            if sub_in.text():
                db.save_timetable({
                    'id': edit_item['id'] if edit_item else f"tt-{int(datetime.now().timestamp())}",
                    'sem': 1,
                    'day': day_combo.currentText(),
                    'subject': sub_in.text(),
                    'start': start_in.text(),
                    'end': end_in.text(),
                    'location': loc_in.text(),
                    'instructor': inst_in.text()
                })
                dlg.accept()
                self.refresh_all_views()

        btn_save.clicked.connect(save)
        dlg.exec()

    def import_photo_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.webp)")
        if file_path and os.path.exists(file_path):
            ext = os.path.splitext(file_path)[1].replace('.', '')
            with open(file_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            b64_src = f"data:image/{ext};base64,{encoded}"

            db.save_memory({
                'id': f"mem-{int(datetime.now().timestamp())}",
                'title': os.path.basename(file_path),
                'date': date.today().strftime("%Y-%m-%d"),
                'tag': 'Campus',
                'src': b64_src
            })
            self.refresh_all_views()
            self.send_notification("Memory Saved 🖼️", f'Imported photo: {os.path.basename(file_path)}')

    def open_milestone_dialog(self, edit_item=None):
        dlg = QDialog(self); dlg.setWindowTitle("Edit Milestone" if edit_item else "Add Milestone"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        cat_combo = QComboBox(dlg); cat_combo.addItems(["Exam", "Project", "Hackathon", "Internship", "Fest", "CGPA"])
        if edit_item:
            m_idx = cat_combo.findText(edit_item['category'])
            if m_idx != -1: cat_combo.setCurrentIndex(m_idx)

        title_in = QLineEdit(dlg); title_in.setText(edit_item['title'] if edit_item else "")
        date_in = QLineEdit(dlg); date_in.setText(edit_item['date'] if edit_item else date.today().strftime("%Y-%m-%d"))
        desc_in = QLineEdit(dlg); desc_in.setText(edit_item.get('desc', '') if edit_item else "")

        lay.addWidget(QLabel("Category:", dlg)); lay.addWidget(cat_combo)
        lay.addWidget(QLabel("Title:", dlg)); lay.addWidget(title_in)
        lay.addWidget(QLabel("Date:", dlg)); lay.addWidget(date_in)
        lay.addWidget(QLabel("Description:", dlg)); lay.addWidget(desc_in)

        btn_save = QPushButton("Save Milestone", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            if title_in.text():
                db.save_milestone({
                    'id': edit_item['id'] if edit_item else f"ms-{int(datetime.now().timestamp())}",
                    'category': cat_combo.currentText(),
                    'title': title_in.text(),
                    'date': date_in.text(),
                    'desc': desc_in.text()
                })
                dlg.accept()
                self.refresh_all_views()

        btn_save.clicked.connect(save)
        dlg.exec()

    def open_settings_dialog(self):
        dlg = QDialog(self); dlg.setWindowTitle("System Settings & Data Management"); dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)

        btn_exp_pdf = QPushButton("📄 Export Academic & Financial Report", dlg); btn_exp_pdf.setProperty("class", "primary")
        btn_exp_pdf.clicked.connect(self.export_pdf_report)
        lay.addWidget(btn_exp_pdf)

        btn_exp = QPushButton("Export Database Backup JSON", dlg)
        btn_exp.clicked.connect(self.export_backup)
        lay.addWidget(btn_exp)

        btn_imp = QPushButton("Import Database Backup JSON", dlg)
        btn_imp.clicked.connect(self.import_backup)
        lay.addWidget(btn_imp)

        btn_sample = QPushButton("Load Sample 5-Year Data", dlg)
        btn_sample.clicked.connect(self.load_sample)
        lay.addWidget(btn_sample)

        btn_clear = QPushButton("Clear All Data (Reset)", dlg); btn_clear.setProperty("class", "danger")
        btn_clear.clicked.connect(self.clear_all_data)
        lay.addWidget(btn_clear)

        dlg.exec()

    def clear_all_data(self):
        if QMessageBox.question(self, "Confirm Reset", "Are you sure you want to clear all data in SQLite?") == QMessageBox.StandardButton.Yes:
            db.clear_all()
            self.refresh_all_views()
            QMessageBox.information(self, "Cleared", "Database cleared!")

    def export_backup(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Backup JSON", "STUNT_Backup.json", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(db.get_all_data(), f, indent=2)
            QMessageBox.information(self, "Success", "Database exported successfully!")

    def import_backup(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Backup JSON", "", "JSON Files (*.json)")
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    parsed = json.load(f)
                if 'attendanceLogs' in parsed or 'subjects' in parsed:
                    db.clear_all()
                    for syl in parsed.get('syllabus', []): db.save_syllabus(syl)
                    for sg in parsed.get('savingsGoals', []): db.save_savings_goal(sg)
                    for g in parsed.get('grades', []): db.save_grade(g)
                    for t in parsed.get('tasks', []): db.save_task(t)
                    for sub in parsed.get('subjects', []): db.save_subject(sub)
                    for att in parsed.get('attendanceLogs', []): db.save_attendance(att)
                    for fin in parsed.get('finances', []): db.save_finance(fin)
                    for tt in parsed.get('timetable', []): db.save_timetable(tt)
                    for mem in parsed.get('memories', []): db.save_memory(mem)
                    for ms in parsed.get('milestones', []): db.save_milestone(ms)
                    self.refresh_all_views()
                    QMessageBox.information(self, "Success", "Database restored successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid backup file: {e}")

    def load_sample(self):
        db.load_sample_data()
        self.refresh_all_views()
        QMessageBox.information(self, "Success", "Sample data loaded!")

def main():
    app = QApplication(sys.argv)

    splash = StuntVideoSplash()
    splash.exec()

    window = StuntMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
