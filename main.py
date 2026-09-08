"""
STUNT: Student Tracker for Unified Navigation & Tasks
100% Native PyQt6 Python Desktop Application (main.py)
"""

import sys
import os
import json
import base64
import math
import threading
from datetime import datetime, date, timedelta

import db

from PyQt6.QtCore import Qt, QTimer, QUrl, QSize, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QStackedWidget, QProgressBar, QFrame,
    QFileDialog, QMessageBox, QTabWidget, QListWidget, QListWidgetItem,
    QTextEdit, QGraphicsOpacityEffect, QScrollArea, QGridLayout, QFormLayout,
    QSystemTrayIcon, QSplitter
)
from PyQt6.QtGui import QIcon, QPixmap, QColor, QFont, QImage, QDesktopServices, QKeySequence, QShortcut
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

# Matplotlib Qt Integration
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Native Speech Synthesis Engine for Reading Copyright Aloud
def speak_text(text):
    def run_speech():
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except Exception:
            pass
    threading.Thread(target=run_speech, daemon=True).start()

def parse_time_to_minutes(time_str: str):
    if not time_str:
        return None
    time_str = time_str.strip().upper()
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M", "%I %p"):
        try:
            dt = datetime.strptime(time_str, fmt)
            return dt.hour * 60 + dt.minute
        except ValueError:
            pass
    return None

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

QSplitter::handle {{
    background-color: rgba(255, 255, 255, 0.12);
    border-radius: 3px;
}}

QSplitter::handle:hover {{
    background-color: {t['primary']};
}}

QSplitter::handle:vertical {{
    height: 8px;
    margin: 2px 0px;
}}

QSplitter::handle:horizontal {{
    width: 8px;
    margin: 0px 2px;
}}

QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background: #08090d;
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background: rgba(255, 255, 255, 0.2);
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background: {t['primary']};
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

# Native Video Opening Splash Window with Audio Speech Copyright Reader
class StuntVideoSplash(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STUNT Platform")
        self.setFixedSize(640, 520)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget(self)
        layout.addWidget(self.video_widget)

        copy_banner = QFrame(self)
        copy_banner.setFixedHeight(45)
        copy_banner.setStyleSheet("background: #08090d; border-top: 1px solid rgba(255,255,255,0.1);")
        c_lay = QHBoxLayout(copy_banner)
        c_lay.setContentsMargins(16, 0, 16, 0)

        lbl_copy = QLabel("© 2026 Akul. All Rights Reserved. STUNT Platform", copy_banner)
        lbl_copy.setStyleSheet("color: #10b981; font-weight: bold; font-size: 13px;")
        c_lay.addWidget(lbl_copy, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(copy_banner)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        video_path = os.path.join(os.path.dirname(__file__), 'assets', 'RedandBlackGlitchcoreStuntLogo.mp4')
        if os.path.exists(video_path):
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.play()

        speak_text("Copyright 2026 Akul. All Rights Reserved. STUNT Platform.")

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

# Dedicated Copyright Notice & Audio Speech Window
class CopyrightDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Official Copyright & Ownership Notice")
        self.setFixedWidth(460)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        hdr = QLabel("© Copyright & Legal Notice", self)
        hdr.setProperty("class", "h1")
        hdr.setStyleSheet("color: #10b981;")
        lay.addWidget(hdr, alignment=Qt.AlignmentFlag.AlignCenter)

        card = QFrame(self); card.setProperty("class", "card")
        c_lay = QVBoxLayout(card); c_lay.setSpacing(10)

        lbl_c1 = QLabel("Copyright © 2026 Akul.", self)
        lbl_c1.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        c_lay.addWidget(lbl_c1, alignment=Qt.AlignmentFlag.AlignCenter)

        lbl_c2 = QLabel("ALL RIGHTS RESERVED.", self)
        lbl_c2.setStyleSheet("font-size: 14px; font-weight: bold; color: #f43f5e;")
        c_lay.addWidget(lbl_c2, alignment=Qt.AlignmentFlag.AlignCenter)

        desc = QLabel(
            "This software application, STUNT (Student Tracker for Unified Navigation & Tasks), "
            "including all source code, algorithms, custom graphical user interfaces, assets, "
            "and design systems, is the exclusive intellectual property of Akul.\n\n"
            "No part of this application may be copied, reproduced, modified, republished, "
            "or distributed without explicit written authorization from the copyright holder.",
            self
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.5;")
        c_lay.addWidget(desc)

        lay.addWidget(card)

        btn_speak = QPushButton("🔊 Read Copyright Aloud", self)
        btn_speak.setProperty("class", "success")
        btn_speak.clicked.connect(self.read_aloud)
        lay.addWidget(btn_speak)

        btn_close = QPushButton("I Understand", self)
        btn_close.setProperty("class", "primary")
        btn_close.clicked.connect(self.accept)
        lay.addWidget(btn_close)

        self.read_aloud()

    def read_aloud(self):
        speak_text("Copyright 2026 Akul. All Rights Reserved. All intellectual property belongs exclusively to Akul.")

# Interactive Flashcard Viewer & Revision Studio Window
class FlashcardDialog(QDialog):
    def __init__(self, flashcards, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Syllabus Flashcards Revision Studio 🎴")
        self.setFixedSize(540, 420)
        self.flashcards = list(flashcards)
        self.idx = 0
        self.showing_answer = False

        lay = QVBoxLayout(self); lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(12)

        top_bar = QHBoxLayout()
        self.lbl_counter = QLabel(self); self.lbl_counter.setStyleSheet("color: #64748b; font-weight: bold;")
        top_bar.addWidget(self.lbl_counter)
        top_bar.addStretch()

        btn_add = QPushButton("➕ Add Flashcard", self); btn_add.setProperty("class", "success")
        btn_add.clicked.connect(self.open_add_dialog)
        top_bar.addWidget(btn_add)

        btn_shuffle = QPushButton("🔀 Shuffle", self)
        btn_shuffle.clicked.connect(self.shuffle_cards)
        top_bar.addWidget(btn_shuffle)

        self.btn_del = QPushButton("🗑️", self); self.btn_del.setProperty("class", "danger")
        self.btn_del.setToolTip("Delete current flashcard")
        self.btn_del.clicked.connect(self.delete_current_card)
        top_bar.addWidget(self.btn_del)
        lay.addLayout(top_bar)

        self.card_box = QFrame(self); self.card_box.setProperty("class", "card"); self.card_box.setMinimumHeight(200)
        cb_lay = QVBoxLayout(self.card_box)

        card_meta = QHBoxLayout()
        self.lbl_subject = QLabel(self); self.lbl_subject.setStyleSheet("color: #0ea5e9; font-weight: bold;")
        self.lbl_status = QLabel(self); self.lbl_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #f59e0b;")
        card_meta.addWidget(self.lbl_subject); card_meta.addStretch(); card_meta.addWidget(self.lbl_status)
        cb_lay.addLayout(card_meta)

        self.lbl_text = QLabel(self); self.lbl_text.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;"); self.lbl_text.setWordWrap(True)
        cb_lay.addWidget(self.lbl_text, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.card_box)

        nav_lay = QHBoxLayout()
        btn_prev = QPushButton("◀ Previous", self); btn_prev.clicked.connect(self.prev_card)
        self.btn_flip = QPushButton("🔄 Flip (Show Answer)", self); self.btn_flip.setProperty("class", "primary"); self.btn_flip.clicked.connect(self.flip_card)
        btn_next = QPushButton("Next ▶", self); btn_next.clicked.connect(self.next_card)
        nav_lay.addWidget(btn_prev); nav_lay.addWidget(self.btn_flip); nav_lay.addWidget(btn_next)
        lay.addLayout(nav_lay)

        bottom_actions = QHBoxLayout()
        self.btn_master = QPushButton("⭐ Toggle Mastered Status", self)
        self.btn_master.clicked.connect(self.toggle_mastered)
        bottom_actions.addWidget(self.btn_master)
        lay.addLayout(bottom_actions)

        self.render_card()

    def render_card(self):
        if not self.flashcards:
            self.lbl_counter.setText("0 / 0 Cards")
            self.lbl_subject.setText("No Flashcards")
            self.lbl_status.setText("")
            self.lbl_text.setText("No flashcards found.\nClick '➕ Add Flashcard' above to create revision questions!")
            self.lbl_text.setStyleSheet("font-size: 14px; color: #94a3b8;")
            self.btn_del.setEnabled(False)
            self.btn_master.setEnabled(False)
            return

        self.btn_del.setEnabled(True)
        self.btn_master.setEnabled(True)
        fc = self.flashcards[self.idx]
        status = fc.get('status', 'Learning')
        self.lbl_counter.setText(f"Card {self.idx + 1} of {len(self.flashcards)}")
        self.lbl_subject.setText(f"Subject: {fc.get('subjectName', 'General')}")
        self.lbl_status.setText(f"Status: {status}")
        self.lbl_status.setStyleSheet("color: #10b981; font-weight: bold;" if status == 'Mastered' else "color: #f59e0b; font-weight: bold;")

        if self.showing_answer:
            self.lbl_text.setText(f"ANSWER:\n\n{fc.get('answer', '')}")
            self.lbl_text.setStyleSheet("font-size: 15px; font-weight: bold; color: #10b981;")
            self.btn_flip.setText("🔄 Flip (Show Question)")
        else:
            self.lbl_text.setText(f"QUESTION:\n\n{fc.get('question', '')}")
            self.lbl_text.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff;")
            self.btn_flip.setText("🔄 Flip (Show Answer)")

    def flip_card(self):
        self.showing_answer = not self.showing_answer
        self.render_card()

    def prev_card(self):
        if self.flashcards:
            self.idx = (self.idx - 1) % len(self.flashcards)
            self.showing_answer = False
            self.render_card()

    def next_card(self):
        if self.flashcards:
            self.idx = (self.idx + 1) % len(self.flashcards)
            self.showing_answer = False
            self.render_card()

    def shuffle_cards(self):
        import random
        if self.flashcards:
            random.shuffle(self.flashcards)
            self.idx = 0
            self.showing_answer = False
            self.render_card()

    def toggle_mastered(self):
        if not self.flashcards:
            return
        fc = self.flashcards[self.idx]
        cur = fc.get('status', 'Learning')
        new_stat = 'Mastered' if cur != 'Mastered' else 'Learning'
        fc['status'] = new_stat
        db.save_flashcard(fc)
        self.render_card()
        if self.parent() and hasattr(self.parent(), 'refresh_all_views'):
            self.parent().refresh_all_views()

    def open_add_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Create New Flashcard")
        dlg.setFixedWidth(400)
        lay = QVBoxLayout(dlg)

        sub_combo = QComboBox(dlg)
        sub_combo.setEditable(True)
        if self.parent() and hasattr(self.parent(), 'data'):
            for s in self.parent().data.get('subjects', []):
                sub_combo.addItem(s['name'])
        if sub_combo.count() == 0:
            sub_combo.addItem("Computer Science")

        q_edit = QTextEdit(dlg)
        q_edit.setPlaceholderText("Enter Question / Concept Prompt...")
        q_edit.setFixedHeight(75)

        a_edit = QTextEdit(dlg)
        a_edit.setPlaceholderText("Enter Clear Answer / Definition...")
        a_edit.setFixedHeight(85)

        lay.addWidget(QLabel("Subject:", dlg)); lay.addWidget(sub_combo)
        lay.addWidget(QLabel("Question:", dlg)); lay.addWidget(q_edit)
        lay.addWidget(QLabel("Answer:", dlg)); lay.addWidget(a_edit)

        btn_save = QPushButton("Save Flashcard", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            sub_name = sub_combo.currentText().strip() or "General"
            q_text = q_edit.toPlainText().strip()
            a_text = a_edit.toPlainText().strip()
            if not q_text or not a_text:
                QMessageBox.warning(dlg, "Incomplete", "Please enter both a question and an answer.")
                return

            new_fc = {
                'id': f"fc-{int(datetime.now().timestamp())}",
                'subjectName': sub_name,
                'question': q_text,
                'answer': a_text,
                'status': 'Learning'
            }
            db.save_flashcard(new_fc)
            self.flashcards.append(new_fc)
            self.idx = len(self.flashcards) - 1
            self.showing_answer = False
            self.render_card()
            if self.parent() and hasattr(self.parent(), 'refresh_all_views'):
                self.parent().refresh_all_views()
            dlg.accept()

        btn_save.clicked.connect(save)
        dlg.exec()

    def delete_current_card(self):
        if not self.flashcards:
            return
        fc = self.flashcards[self.idx]
        if QMessageBox.question(self, "Delete Flashcard", f"Delete flashcard for '{fc.get('subjectName', 'card')}'?") == QMessageBox.StandardButton.Yes:
            db.delete_flashcard(fc['id'])
            del self.flashcards[self.idx]
            if self.idx >= len(self.flashcards):
                self.idx = max(0, len(self.flashcards) - 1)
            self.showing_answer = False
            self.render_card()
            if self.parent() and hasattr(self.parent(), 'refresh_all_views'):
                self.parent().refresh_all_views()

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

# Embedded JARVIS Wingman Companion Dialog
class JarvisWingmanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("J.A.R.V.I.S. • Akul's College Wingman & Academic Co-Pilot")
        self.resize(740, 660)
        self.setMinimumSize(620, 540)
        self.voice_enabled = True

        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(18, 18, 18, 18)
        main_lay.setSpacing(10)

        # Header Frame with AI Avatar & Voice Toggle
        hdr_frame = QFrame(self)
        hdr_frame.setStyleSheet("background: #10121d; border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 10px; padding: 6px;")
        hdr_lay = QHBoxLayout(hdr_frame)
        hdr_lay.setContentsMargins(12, 6, 12, 6)

        lbl_bot = QLabel("🤖", self)
        lbl_bot.setStyleSheet("font-size: 32px;")
        hdr_lay.addWidget(lbl_bot)

        title_lay = QVBoxLayout()
        title_lay.setSpacing(2)
        lbl_title = QLabel("J.A.R.V.I.S. Mark XLI • College Wingman", self)
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #38bdf8;")
        lbl_sub = QLabel("Connected to STUNT Database • Real-Time Schedule & Attendance Intelligence", self)
        lbl_sub.setStyleSheet("font-size: 11px; color: #94a3b8;")
        title_lay.addWidget(lbl_title)
        title_lay.addWidget(lbl_sub)
        hdr_lay.addLayout(title_lay)
        hdr_lay.addStretch()

        self.btn_voice_toggle = QPushButton("🔊 Voice: ON", self)
        self.btn_voice_toggle.setStyleSheet("background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #10b981; font-weight: bold; padding: 6px 12px; border-radius: 6px;")
        self.btn_voice_toggle.clicked.connect(self.toggle_voice)
        hdr_lay.addWidget(self.btn_voice_toggle)

        main_lay.addWidget(hdr_frame)

        # Live Context Pill Bar
        self.live_pill = QLabel(self)
        self.live_pill.setStyleSheet("background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.3); color: #7dd3fc; border-radius: 6px; padding: 6px 12px; font-size: 12px;")
        main_lay.addWidget(self.live_pill)

        # Chat Conversation Area
        self.chat_view = QTextEdit(self)
        self.chat_view.setReadOnly(True)
        self.chat_view.setStyleSheet("background: #090a10; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px; color: #f8fafc; font-size: 13px;")
        main_lay.addWidget(self.chat_view, stretch=1)

        # Quick Action Chips Bar
        chips_lay = QHBoxLayout()
        chips_lay.setSpacing(6)
        chips = [
            ("📅 Schedule", "What is my timetable today?"),
            ("⏳ Next Class", "What is my next lecture?"),
            ("✅ Mark Present", "Mark me present in my latest lecture"),
            ("🎯 Can I Bunk?", "Can I bunk any classes?"),
            ("📊 Attendance %", "How is my attendance overall?"),
            ("💡 Daily Briefing", "Give me a daily college briefing")
        ]
        for label, prompt in chips:
            btn = QPushButton(label, self)
            btn.setStyleSheet("background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4); color: #cbd5e1; border-radius: 14px; padding: 4px 10px; font-size: 11px;")
            btn.clicked.connect(lambda checked, p=prompt: self.send_prompt(p))
            chips_lay.addWidget(btn)
        chips_lay.addStretch()
        main_lay.addLayout(chips_lay)

        # Input Row
        in_lay = QHBoxLayout()
        in_lay.setSpacing(8)
        self.chat_input = QLineEdit(self)
        self.chat_input.setPlaceholderText("Ask JARVIS: 'Attended Finance today', 'Can I bunk Stats?', 'What class next?'...")
        self.chat_input.setStyleSheet("background: #141724; border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 8px; padding: 10px 14px; color: #ffffff; font-size: 13px;")
        self.chat_input.returnPressed.connect(self.handle_send)
        in_lay.addWidget(self.chat_input, stretch=1)

        btn_send = QPushButton("Send 🚀", self)
        btn_send.setProperty("class", "primary")
        btn_send.setStyleSheet("background: #6366f1; color: #ffffff; font-weight: bold; border-radius: 8px; padding: 10px 18px;")
        btn_send.clicked.connect(self.handle_send)
        in_lay.addWidget(btn_send)
        main_lay.addLayout(in_lay)

        self.update_live_context()
        self.initial_greeting()

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        if self.voice_enabled:
            self.btn_voice_toggle.setText("🔊 Voice: ON")
            self.btn_voice_toggle.setStyleSheet("background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #10b981; font-weight: bold; padding: 6px 12px; border-radius: 6px;")
        else:
            self.btn_voice_toggle.setText("🔇 Mute")
            self.btn_voice_toggle.setStyleSheet("background: rgba(244, 63, 94, 0.2); border: 1px solid #f43f5e; color: #f43f5e; font-weight: bold; padding: 6px 12px; border-radius: 6px;")

    def append_message(self, sender: str, text: str):
        if sender == "You":
            bubble = f"<div style='margin: 8px 0; text-align: right;'><span style='background: #1e2238; border: 1px solid #6366f1; color: #f8fafc; padding: 8px 14px; border-radius: 12px; display: inline-block;'><b>You:</b> {text}</span></div>"
        else:
            import re
            formatted_text = text.replace('\\n', '<br>').replace('\n', '<br>')
            formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_text)
            bubble = f"<div style='margin: 8px 0; text-align: left;'><span style='background: #111422; border: 1px solid rgba(14, 165, 233, 0.4); color: #cbd5e1; padding: 10px 14px; border-radius: 12px; display: inline-block; line-height: 1.5;'><b>🤖 JARVIS:</b><br>{formatted_text}</span></div>"
        
        self.chat_view.append(bubble)
        sb = self.chat_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    def update_live_context(self):
        now_dt = datetime.now()
        day_name = now_dt.strftime("%A")
        date_str = now_dt.strftime("%d %b %Y")
        time_str = now_dt.strftime("%I:%M %p")
        profile = self.parent_window.profile if self.parent_window else db.get_profile()
        course = profile.get('course', 'Degree')
        self.live_pill.setText(f"🕒 <b>{time_str}</b> • {day_name}, {date_str} • <b>{course}</b> • Target Attendance: <b>{profile.get('targetAttendancePct', 85):.0f}%</b>")

    def initial_greeting(self):
        profile = self.parent_window.profile if self.parent_window else db.get_profile()
        user_name = profile.get('name', 'Akul').split()[0]
        hour = datetime.now().hour
        day_name = datetime.now().strftime("%A")

        if 5 <= hour < 12:
            greet = f"Morning bro {user_name}! ☀️ Ready to tackle {day_name}?"
        elif 12 <= hour < 17:
            greet = f"Hey {user_name}! ⚡ Midday hustle time. Hope college isn't grinding you down!"
        elif 17 <= hour < 22:
            greet = f"Evening bro {user_name}! 🌆 Lectures wrapped up for today. Time to decompress or plan your moves."
        else:
            greet = f"Late night grind, {user_name}! 🌙 Don't burn through the midnight oil too hard, tomorrow's lectures await!"

        tt = self.parent_window.data.get('timetable', []) if self.parent_window else []
        today_slots = [s for s in tt if s.get('day', '').lower() == day_name.lower()]
        
        schedule_msg = ""
        if today_slots:
            schedule_msg = f"You've got <b>{len(today_slots)} lecture{'s' if len(today_slots) > 1 else ''}</b> today. First up: <b>{today_slots[0]['subject']}</b> at {today_slots[0]['start']}."
        else:
            schedule_msg = f"Zero lectures on your timetable for {day_name}. It's a free runway, bro!"

        subs = self.parent_window.data.get('subjects', []) if self.parent_window else []
        att_logs = self.parent_window.data.get('attendanceLogs', []) if self.parent_window else []
        danger_subs = []
        target = profile.get('targetAttendancePct', 85.0)
        for s in subs:
            s_logs = [l for l in att_logs if l.get('subjectId') == s.get('id')]
            if s_logs:
                presents = sum(1 for l in s_logs if l.get('status') == 'Present')
                pct = (presents / len(s_logs)) * 100.0
                if pct < target:
                    danger_subs.append((s.get('name'), pct))

        danger_msg = ""
        if danger_subs:
            sub_names = ", ".join([f"<b>{name}</b> ({p:.1f}%)" for name, p in danger_subs[:2]])
            danger_msg = f"<br>⚠️ <b>Heads up bro:</b> Attendance in {sub_names} is below your {target:.0f}% target. No more bunks there!"

        welcome_text = f"{greet}<br><br>{schedule_msg}{danger_msg}<br><br>I'm connected directly to your STUNT database. Tell me what you need — ask for your schedule, check safe bunks, or say <i>'attended Finance today'</i> to log attendance!"
        self.append_message("JARVIS", welcome_text)

        if self.voice_enabled:
            plain = f"{greet} {schedule_msg}".replace('<b>', '').replace('</b>', '')
            speak_text(plain)

    def send_prompt(self, text: str):
        self.chat_input.setText(text)
        self.handle_send()

    def handle_send(self):
        text = self.chat_input.text().strip()
        if not text:
            return
        self.chat_input.clear()
        self.append_message("You", text)
        self.update_live_context()

        reply = self.resolve_query(text)
        self.append_message("JARVIS", reply)

        if self.voice_enabled:
            import re
            plain = re.sub(r'<.*?>', '', reply).replace('*', '')
            speak_text(plain)

    def resolve_query(self, query: str) -> str:
        q = query.lower()
        now_dt = datetime.now()
        day_name = now_dt.strftime("%A")
        today_str = date.today().isoformat()
        profile = self.parent_window.profile if self.parent_window else db.get_profile()
        target_pct = profile.get('targetAttendancePct', 85.0)
        target_dec = target_pct / 100.0

        if self.parent_window:
            self.parent_window.data = db.get_all_data()
            data = self.parent_window.data
        else:
            data = db.get_all_data()

        subjects = data.get('subjects', [])
        timetable = data.get('timetable', [])
        att_logs = data.get('attendanceLogs', [])

        # 1. ATTENDANCE LOGGING
        is_att_log = any(w in q for w in ["attended", "present in", "mark present", "bunked", "absent in", "missed", "cancelled class", "class cancelled", "log attendance"])
        if is_att_log:
            status = "Present"
            if any(w in q for w in ["bunked", "absent", "missed", "skipped"]):
                status = "Absent"
            elif any(w in q for w in ["cancelled", "canceled"]):
                status = "Cancelled"

            matched_sub = None
            for s in subjects:
                if s['name'].lower() in q:
                    matched_sub = s
                    break
            
            if not matched_sub:
                for t in timetable:
                    if t['subject'].lower() in q:
                        matched_sub = {'name': t['subject'], 'id': None, 'sem': t.get('sem', 1)}
                        break

            sub_name = ""
            if matched_sub:
                sub_name = matched_sub['name']
            else:
                for kw in ["attended", "present in", "mark present in", "mark present", "bunked", "absent in", "missed", "cancelled"]:
                    if kw in q:
                        sub_name = q.split(kw)[-1].replace("today", "").replace("class", "").replace("lecture", "").strip().title()
                        break

            if not sub_name:
                today_slots = [s for s in timetable if s.get('day', '').lower() == day_name.lower()]
                if today_slots:
                    sub_name = today_slots[0]['subject']
                else:
                    return "Which subject did you attend or bunk, bro? Tell me like: <i>'Attended International Finance today'</i>."

            sub_obj = next((s for s in subjects if s['name'].lower() == sub_name.lower()), None)
            if not sub_obj:
                sub_id = f"sub-{int(now_dt.timestamp())}"
                sub_obj = {
                    'id': sub_id,
                    'sem': 1,
                    'name': sub_name,
                    'code': sub_name[:6].upper(),
                    'faculty': 'Faculty',
                    'targetPct': target_pct,
                    'color': '#6366f1'
                }
                db.save_subject(sub_obj)
            else:
                sub_id = sub_obj['id']

            att_id = f"att-{int(now_dt.timestamp())}"
            db.save_attendance({
                'id': att_id,
                'sem': sub_obj.get('sem', 1),
                'subjectId': sub_id,
                'subjectName': sub_obj['name'],
                'date': today_str,
                'status': status,
                'remarks': "Logged via JARVIS Wingman"
            })

            if self.parent_window:
                self.parent_window.refresh_all_views()
                self.parent_window.send_notification("Attendance Logged 📋", f"JARVIS recorded {status} for {sub_obj['name']}")

            all_logs = [l for l in db.get_attendance_logs() if l['subjectId'] == sub_id]
            tot = len(all_logs)
            prs = sum(1 for l in all_logs if l['status'] == 'Present')
            pct = (prs / tot * 100.0) if tot > 0 else 100.0
            safe = math.floor((prs - target_dec * tot) / target_dec) if target_dec > 0 else 0
            needed = math.ceil((target_dec * tot - prs) / (1.0 - target_dec)) if target_dec < 1.0 else 0

            if status == "Present":
                bunk_msg = f"You have <b>{safe} safe bunk(s)</b> in reserve." if safe > 0 else f"⚠️ Careful bro, zero safe bunks left! Keep attending."
                return f"Done bro! ✅ Marked you <b>Present</b> in <b>{sub_obj['name']}</b> for today ({today_str}).<br>Your attendance is now <b>{pct:.1f}%</b> ({prs}/{tot} lectures). {bunk_msg}"
            elif status == "Absent":
                advice = f"You still have <b>{safe} safe bunk(s)</b> remaining." if safe >= 0 else f"🚨 You dipped below your {target_pct:.0f}% target! You need to attend the next <b>{needed} classes straight</b> to recover!"
                return f"Got it, marked you <b>Absent / Bunked</b> ❌ in <b>{sub_obj['name']}</b> for today.<br>Attendance dropped to <b>{pct:.1f}%</b> ({prs}/{tot}). {advice}"
            else:
                return f"Logged <b>{sub_obj['name']}</b> as <b>Cancelled</b> ⚠️ for today. No penalty to your attendance!"

        # 2. BUNK CHECK
        if any(w in q for w in ["bunk", "safe bunk", "can i skip", "skip class", "should i go"]):
            if not subjects:
                return "You don't have any subjects logged in STUNT yet, bro! Add your timetable or subjects first and I'll calculate your exact safe bunks."

            matched_sub = next((s for s in subjects if s['name'].lower() in q), None)
            if matched_sub:
                s_logs = [l for l in att_logs if l.get('subjectId') == matched_sub['id']]
                tot = len(s_logs)
                prs = sum(1 for l in s_logs if l.get('status') == 'Present')
                pct = (prs / tot * 100.0) if tot > 0 else 100.0
                safe = math.floor((prs - target_dec * tot) / target_dec) if target_dec > 0 else 0
                needed = math.ceil((target_dec * tot - prs) / (1.0 - target_dec)) if target_dec < 1.0 else 0

                if safe > 0:
                    return f"Verdict on <b>{matched_sub['name']}</b>: You are at <b>{pct:.1f}%</b> ({prs}/{tot} attended).<br>✅ You have <b>{safe} safe bunk(s)</b> available! You can take a break if you really need to, but don't blow it all at once."
                elif safe == 0 and pct >= target_pct:
                    return f"Careful bro! In <b>{matched_sub['name']}</b> you're at <b>{pct:.1f}%</b> ({prs}/{tot}). You have <b>0 safe bunks</b>! If you miss today, you drop below {target_pct:.0f}%. Sit in class!"
                else:
                    return f"🚨 <b>DO NOT BUNK {matched_sub['name']}!</b><br>You're at <b>{pct:.1f}%</b> ({prs}/{tot}). You must attend the next <b>{needed} classes consecutively</b> to reach {target_pct:.0f}%! Grab your bag and go!"
            else:
                lines = ["<b>Here's your safe bunk breakdown across subjects:</b>"]
                for s in subjects:
                    s_logs = [l for l in att_logs if l.get('subjectId') == s.get('id')]
                    tot = len(s_logs)
                    prs = sum(1 for l in s_logs if l.get('status') == 'Present')
                    pct = (prs / tot * 100.0) if tot > 0 else 100.0
                    safe = math.floor((prs - target_dec * tot) / target_dec) if target_dec > 0 else 0
                    if safe > 0:
                        lines.append(f"• <b>{s['name']}</b>: {pct:.1f}% 🟢 (<b>{safe}</b> safe bunks)")
                    elif pct >= target_pct:
                        lines.append(f"• <b>{s['name']}</b>: {pct:.1f}% 🟡 (<b>0</b> safe bunks — on the edge)")
                    else:
                        needed = math.ceil((target_dec * tot - prs) / (1.0 - target_dec)) if target_dec < 1.0 else 0
                        lines.append(f"• <b>{s['name']}</b>: {pct:.1f}% 🔴 (Need <b>+{needed}</b> classes)")
                return "<br>".join(lines)

        # 3. SCHEDULE / TIMETABLE
        if any(w in q for w in ["schedule", "timetable", "class", "lecture", "today's"]):
            today_slots = [s for s in timetable if s.get('day', '').lower() == day_name.lower()]
            if not today_slots:
                return f"No lectures scheduled on your timetable for <b>{day_name}</b>, bro! If you have classes today, add them in the Timetable tab or click 'Load Sample Schedule'!"

            now_mins = now_dt.hour * 60 + now_dt.minute
            active_slot = None
            next_slot = None
            min_diff = 999999

            for s in today_slots:
                sm = parse_time_to_minutes(s.get('start', ''))
                em = parse_time_to_minutes(s.get('end', ''))
                if sm is None or em is None: continue
                if sm <= now_mins <= em:
                    active_slot = s
                    break
                diff = sm - now_mins
                if 0 < diff < min_diff:
                    min_diff = diff
                    next_slot = s

            schedule_list = []
            for s in today_slots:
                loc = f" (Room {s['location']})" if s.get('location') else ""
                inst = f" - {s['instructor']}" if s.get('instructor') else ""
                schedule_list.append(f"• <b>{s['subject']}</b>: {s['start']} to {s['end']}{loc}{inst}")

            header = f"<b>Today's Schedule ({day_name}, {len(today_slots)} lectures):</b><br>" + "<br>".join(schedule_list)
            if active_slot:
                header += f"<br><br>🔴 <b>You're currently in:</b> {active_slot['subject']} ({active_slot['start']} - {active_slot['end']})!"
            elif next_slot:
                header += f"<br><br>⏳ <b>Next up:</b> {next_slot['subject']} at {next_slot['start']} (in {min_diff} mins)!"
            else:
                header += "<br><br>✅ All lectures for today are finished!"
            return header

        # 4. DAILY BRIEFING
        if any(w in q for w in ["briefing", "summary", "how am i doing", "status", "overview"]):
            today_slots = [s for s in timetable if s.get('day', '').lower() == day_name.lower()]
            tasks = data.get('tasks', [])
            pending_tasks = [t for t in tasks if t.get('status') != 'Completed']
            tot_att = len(att_logs)
            prs_att = sum(1 for l in att_logs if l.get('status') == 'Present')
            overall_pct = (prs_att / tot_att * 100.0) if tot_att > 0 else 100.0

            brief = [
                f"<b>College 360° Briefing for {profile.get('name', 'Akul')}:</b>",
                f"🏫 <b>Campus</b>: {profile.get('college', 'NMIMS')} • {profile.get('course', 'BBA IB')}",
                f"📅 <b>Today ({day_name})</b>: {len(today_slots)} lectures scheduled.",
                f"📊 <b>Overall Attendance</b>: <b>{overall_pct:.1f}%</b> (Target: {target_pct:.0f}%)",
                f"🎯 <b>Tasks & Deadlines</b>: {len(pending_tasks)} pending assignments."
            ]
            if pending_tasks:
                brief.append(f"Urgent: <i>{pending_tasks[0]['title']}</i> (due {pending_tasks[0].get('dueDate', 'soon')})")
            brief.append("Keep the momentum going, bro! What would you like to tackle next?")
            return "<br>".join(brief)

        # 5. TASKS / ASSIGNMENTS
        if any(w in q for w in ["task", "todo", "assignment", "homework"]):
            tasks = data.get('tasks', [])
            pending_tasks = [t for t in tasks if t.get('status') != 'Completed']
            if not pending_tasks:
                return "Zero pending tasks on your board! You're completely caught up, bro. Take a well-deserved break or review your flashcards!"
            t_lines = ["<b>Your Pending Tasks & Deadlines:</b>"]
            for t in pending_tasks[:5]:
                t_lines.append(f"• <b>{t['title']}</b> [{t.get('priority', 'Normal')}] - Due {t.get('dueDate', 'No date')}")
            return "<br>".join(t_lines)

        # 6. FRIEND BANTER / DEFAULT
        greetings = ["hey", "hello", "hi", "sup", "what's up", "bro", "jarvis"]
        if any(q.startswith(g) for g in greetings) or len(q) < 10:
            return f"What's good, bro! I'm on duty. Ask me about your timetable, check if you can bunk a class, or tell me <i>'Attended [Subject] today'</i> to log your attendance!"
        
        return f"Got it bro! I'm tracking everything in STUNT. You can tell me to log attendance (e.g. <i>'Attended Finance today'</i>), check your schedule (<i>'What's my next lecture?'</i>), or calculate safe bunks (<i>'Can I bunk Economics?'</i>)."

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

        self.pomo_mode = "Focus"
        self.pomo_seconds = 25 * 60
        self.pomo_is_running = False
        self.pomo_sessions = 0
        self.pomo_timer = QTimer(self)
        self.pomo_timer.timeout.connect(self.pomo_tick)

        # Smart Lecture Alarm - deduplicated per class per day
        self.notified_lecture_alarms = set()
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
        today_date = date.today().strftime("%Y-%m-%d")
        now_time = datetime.now()
        for slot in self.data.get('timetable', []):
            if slot['day'] == today_str:
                try:
                    slot_t = datetime.strptime(slot['start'], "%I:%M %p").replace(year=now_time.year, month=now_time.month, day=now_time.day)
                    diff = (slot_t - now_time).total_seconds()
                    alarm_key = (slot['id'], today_date)
                    if 0 <= diff <= 900 and alarm_key not in self.notified_lecture_alarms: # Within 15 mins
                        self.notified_lecture_alarms.add(alarm_key)
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

        btn_copy = QPushButton("© Copyright Notice", self); btn_copy.setStyleSheet("background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981;")
        btn_copy.clicked.connect(self.open_copyright_dialog)
        topbar_layout.addWidget(btn_copy)

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

        btn_jarvis = QPushButton("🤖 JARVIS Wingman", self)
        btn_jarvis.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #0ea5e9); color: #ffffff; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_jarvis.clicked.connect(self.open_jarvis_wingman)
        topbar_layout.addWidget(btn_jarvis)

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

        # 4. Right Diagnostics Drawer with Gamified Badges
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

        # Gamified Student Achievement Badges Card
        card_badges = QFrame(self); card_badges.setProperty("class", "card")
        cb_lay = QVBoxLayout(card_badges)
        cb_lay.addWidget(QLabel("🏆 STUDENT BADGES & XP", self))
        self.lbl_xp = QLabel("Level 1 Scholar • 0 XP", self)
        self.lbl_xp.setStyleSheet("font-size: 12px; color: #10b981; font-weight: bold;")
        cb_lay.addWidget(self.lbl_xp)
        self.lbl_badges = QLabel("Calculating achievements...", self)
        self.lbl_badges.setStyleSheet("font-size: 11px; color: #f59e0b; font-weight: bold;")
        self.lbl_badges.setWordWrap(True)
        cb_lay.addWidget(self.lbl_badges)
        drawer_layout.addWidget(card_badges)

        card_copy = QFrame(self); card_copy.setProperty("class", "card")
        cc2_lay = QVBoxLayout(card_copy)
        cc2_lay.addWidget(QLabel("LEGAL COPYRIGHT", self))
        lbl_copy_drawer = QLabel("© 2026 Akul\nAll Rights Reserved.", self); lbl_copy_drawer.setStyleSheet("color: #10b981; font-weight: bold;")
        cc2_lay.addWidget(lbl_copy_drawer)
        drawer_layout.addWidget(card_copy)

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

        # Global Navigation Hotkeys (Ctrl+1 to Ctrl+9, Ctrl+T, Ctrl+A)
        for i in range(min(9, len(nav_items))):
            sc = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            sc.activated.connect(lambda checked=False, idx=i: self.switch_view(idx))

        sc_task = QShortcut(QKeySequence("Ctrl+T"), self)
        sc_task.activated.connect(lambda: self.open_task_dialog())

        sc_att = QShortcut(QKeySequence("Ctrl+A"), self)
        sc_att.activated.connect(lambda: self.open_attendance_dialog())

        sc_jarvis = QShortcut(QKeySequence("Ctrl+J"), self)
        sc_jarvis.activated.connect(self.open_jarvis_wingman)

        self.switch_view(0)
        self.refresh_all_views()

    def open_jarvis_wingman(self):
        if not hasattr(self, 'jarvis_dlg') or self.jarvis_dlg is None or not self.jarvis_dlg.isVisible():
            self.jarvis_dlg = JarvisWingmanDialog(self)
            self.jarvis_dlg.show()
        else:
            self.jarvis_dlg.activateWindow()
            self.jarvis_dlg.raise_()

    def open_copyright_dialog(self):
        dlg = CopyrightDialog(self)
        dlg.exec()

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

    # 1. DASHBOARD VIEW (with Study Activity Heatmap Grid & ScrollArea)
    def init_dashboard_view(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        content = QWidget()
        lay = QVBoxLayout(content); lay.setContentsMargins(24, 24, 24, 24); lay.setSpacing(20)

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

        # 7-Day Activity Stream Heatmap Grid
        heat_card = QFrame(self); heat_card.setProperty("class", "card"); hc_lay = QVBoxLayout(heat_card)
        hc_lay.addWidget(QLabel("📈 7-DAY PRODUCTIVITY & STUDY ACTIVITY HEATMAP", self))

        self.heat_grid_lay = QHBoxLayout()
        hc_lay.addLayout(self.heat_grid_lay)
        lay.addWidget(heat_card)

        lay.addStretch()
        scroll.setWidget(content)
        self.views_stack.addWidget(scroll)

    # 2. CGPA & GRADE INTELLIGENCE VIEW (with Draggable Size Ratio Splitter)
    def init_cgpa_view(self):
        view = QWidget(self); main_lay = QVBoxLayout(view); main_lay.setContentsMargins(24, 24, 24, 24); main_lay.setSpacing(12)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("CGPA / SGPA Intelligence & Grade Ledger", self))
        hdr_lay.addStretch()
        btn_add_g = QPushButton("+ Log Subject Grade", self); btn_add_g.setProperty("class", "primary"); btn_add_g.clicked.connect(self.open_grade_dialog)
        hdr_lay.addWidget(btn_add_g)
        main_lay.addLayout(hdr_lay)

        splitter = QSplitter(Qt.Orientation.Vertical, self)

        # Top Panel: CGPA Card + What-If Simulator Card
        top_w = QWidget()
        top_lay = QVBoxLayout(top_w); top_lay.setContentsMargins(0, 0, 0, 0); top_lay.setSpacing(12)

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
        top_lay.addWidget(cgpa_card)

        sim_card = QFrame(self); sim_card.setProperty("class", "card"); sc_lay = QHBoxLayout(sim_card)
        sc_lay.addWidget(QLabel("📊 <b>What-If Simulator</b>: If expected SGPA in next semester is", self))
        self.sim_sgpa_in = QLineEdit(self); self.sim_sgpa_in.setFixedWidth(70); self.sim_sgpa_in.setText("9.0")
        sc_lay.addWidget(self.sim_sgpa_in)

        btn_sim = QPushButton("Calculate Simulated CGPA", self); btn_sim.setProperty("class", "primary")
        btn_sim.clicked.connect(self.run_whatif_simulation)
        sc_lay.addWidget(btn_sim)

        self.lbl_sim_res = QLabel("Simulated Result: --", self); self.lbl_sim_res.setStyleSheet("font-weight: bold; color: #10b981;")
        sc_lay.addWidget(self.lbl_sim_res)
        sc_lay.addStretch()
        top_lay.addWidget(sim_card)

        splitter.addWidget(top_w)

        # Bottom Panel: Grades Ledger Table Container
        bot_w = QWidget()
        bot_lay = QVBoxLayout(bot_w); bot_lay.setContentsMargins(0, 0, 0, 0); bot_lay.setSpacing(6)
        bot_lay.addWidget(QLabel("📜 GRADES & SGPA LEDGER (Drag horizontal bar above to adjust size ratio)", self))

        self.grades_table = QTableWidget(self)
        self.grades_table.setColumnCount(6)
        self.grades_table.setHorizontalHeaderLabels(["Semester", "Subject Code", "Subject Name", "Credits", "Grade Points", "Actions"])
        self.grades_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bot_lay.addWidget(self.grades_table)

        splitter.addWidget(bot_w)
        splitter.setSizes([320, 480])

        main_lay.addWidget(splitter)
        self.views_stack.addWidget(view)

    def run_whatif_simulation(self):
        try:
            exp_sgpa = float(self.sim_sgpa_in.text())
            if not (0.0 <= exp_sgpa <= 10.0):
                QMessageBox.warning(self, "Invalid Input", "SGPA must be between 0.0 and 10.0.")
                return
            grades = self.data.get('grades', [])
            total_pts = sum(g['credits'] * g['gradePoints'] for g in grades)
            total_creds = sum(g['credits'] for g in grades)
            cur_cgpa = (total_pts / total_creds) if total_creds > 0 else 0.0

            sems_with_grades = sorted(list(set(g['sem'] for g in grades)))
            done_sems = len(sems_with_grades)
            if done_sems == 0:
                sim_cgpa = exp_sgpa
                next_sem = 1
            else:
                sim_cgpa = ((cur_cgpa * done_sems) + exp_sgpa) / (done_sems + 1)
                next_sem = max(sems_with_grades) + 1

            self.lbl_sim_res.setText(f"Simulated CGPA after Sem {next_sem}: {sim_cgpa:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a valid SGPA number between 0 and 10.")

    # 3. SYLLABUS & REVISION MATRIX VIEW (with Draggable Size Ratio Splitter)
    def init_syllabus_view(self):
        view = QWidget(self); main_lay = QVBoxLayout(view); main_lay.setContentsMargins(24, 24, 24, 24); main_lay.setSpacing(12)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Exam Syllabus & Revision Matrix", self))
        hdr_lay.addStretch()

        btn_fc = QPushButton("🎴 Launch Revision Flashcards", self); btn_fc.setProperty("class", "success"); btn_fc.clicked.connect(self.open_flashcards_modal)
        hdr_lay.addWidget(btn_fc)

        btn_add_note = QPushButton("📝 + Add PYQ / PDF Note", self); btn_add_note.clicked.connect(self.open_subject_note_dialog)
        hdr_lay.addWidget(btn_add_note)

        btn_add_unit = QPushButton("📚 + Add Syllabus Unit", self); btn_add_unit.setProperty("class", "primary"); btn_add_unit.clicked.connect(self.open_syllabus_dialog)
        hdr_lay.addWidget(btn_add_unit)
        main_lay.addLayout(hdr_lay)

        prog_card = QFrame(self); prog_card.setProperty("class", "card"); pc_lay = QVBoxLayout(prog_card)
        self.lbl_syl_summary = QLabel("Syllabus Revision Progress: 0 of 0 Units Completed (0%)", self); self.lbl_syl_summary.setStyleSheet("font-weight: bold; color: #ffffff;")
        pc_lay.addWidget(self.lbl_syl_summary)
        self.syl_progress_bar = QProgressBar(self); self.syl_progress_bar.setFixedHeight(8)
        pc_lay.addWidget(self.syl_progress_bar)
        main_lay.addWidget(prog_card)

        splitter = QSplitter(Qt.Orientation.Vertical, self)

        # Top Panel: PYQ Notes Vault
        top_w = QWidget()
        top_lay = QVBoxLayout(top_w); top_lay.setContentsMargins(0, 0, 0, 0); top_lay.setSpacing(6)
        notes_hdr = QLabel("📝 PYQ & PDF NOTES RESOURCE VAULT (Drag bar below to adjust size ratio)", self); notes_hdr.setProperty("class", "h3")
        top_lay.addWidget(notes_hdr)

        self.notes_table = QTableWidget(self)
        self.notes_table.setColumnCount(5)
        self.notes_table.setHorizontalHeaderLabels(["Subject", "Document Title", "Type", "Date", "Actions"])
        self.notes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        top_lay.addWidget(self.notes_table)
        splitter.addWidget(top_w)

        # Bottom Panel: Syllabus Table
        bot_w = QWidget()
        bot_lay = QVBoxLayout(bot_w); bot_lay.setContentsMargins(0, 0, 0, 0); bot_lay.setSpacing(6)
        syl_hdr = QLabel("📚 EXAM SYLLABUS & REVISION UNITS TABLE", self); syl_hdr.setProperty("class", "h3")
        bot_lay.addWidget(syl_hdr)

        self.syl_table = QTableWidget(self)
        self.syl_table.setColumnCount(5)
        self.syl_table.setHorizontalHeaderLabels(["Subject", "Unit / Topic Title", "Revision Status", "Notes", "Actions"])
        self.syl_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bot_lay.addWidget(self.syl_table)
        splitter.addWidget(bot_w)

        splitter.setSizes([220, 450])
        main_lay.addWidget(splitter)
        self.views_stack.addWidget(view)

    def open_flashcards_modal(self):
        fcs = self.data.get('flashcards', [])
        dlg = FlashcardDialog(fcs, self)
        dlg.exec()

    def open_subject_note_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF / Note File", "", "All Documents (*.pdf *.png *.jpg *.txt *.docx);;All Files (*)")
        if not file_path:
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Add Note / PYQ to Vault")
        dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)

        sub_combo = QComboBox(dlg)
        sub_combo.setEditable(True)
        for s in self.data.get('subjects', []):
            sub_combo.addItem(f"{s['name']} ({s['code']})", s['name'])
        if sub_combo.count() == 0:
            sub_combo.addItem("General Academics", "General Academics")

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        title_in = QLineEdit(dlg)
        title_in.setText(base_name)

        doc_type_combo = QComboBox(dlg)
        doc_type_combo.addItems(["PDF", "PYQ", "Notes", "Assignment", "Cheatsheet", "Lab Manual"])

        lay.addWidget(QLabel("Target Subject:", dlg))
        lay.addWidget(sub_combo)
        lay.addWidget(QLabel("Document Title / Topic:", dlg))
        lay.addWidget(title_in)
        lay.addWidget(QLabel("Resource Type:", dlg))
        lay.addWidget(doc_type_combo)

        lbl_path = QLabel(f"File: {os.path.basename(file_path)}", dlg)
        lbl_path.setStyleSheet("color: #64748b; font-size: 11px;")
        lay.addWidget(lbl_path)

        btn_save = QPushButton("Save to Vault 📁", dlg)
        btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            sub_name = sub_combo.currentText().strip()
            if "(" in sub_name and ")" in sub_name:
                sub_name = sub_name.split("(")[0].strip()
            title = title_in.text().strip() or os.path.basename(file_path)
            ftype = doc_type_combo.currentText()

            db.save_subject_note({
                'id': f"sn-{int(datetime.now().timestamp())}",
                'subjectName': sub_name or "General Academics",
                'title': title,
                'fileType': ftype,
                'filePath': file_path,
                'date': date.today().strftime("%Y-%m-%d")
            })
            dlg.accept()
            self.refresh_all_views()
            self.send_notification("Document Added 📝", f"Saved '{title}' under {sub_name}")

        btn_save.clicked.connect(save)
        dlg.exec()

    # 4. TASKS & POMODORO VIEW (with Draggable Size Ratio Splitter)
    def init_tasks_view(self):
        view = QWidget(self); main_lay = QVBoxLayout(view); main_lay.setContentsMargins(24, 24, 24, 24); main_lay.setSpacing(12)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Task Tracker & Pomodoro Focus Timer", self))
        hdr_lay.addStretch()
        btn_new_task = QPushButton("+ Create Goal / Task", self); btn_new_task.setProperty("class", "primary"); btn_new_task.clicked.connect(lambda: self.open_task_dialog())
        hdr_lay.addWidget(btn_new_task)
        main_lay.addLayout(hdr_lay)

        splitter = QSplitter(Qt.Orientation.Vertical, self)

        # Top Panel: Task Progress & Pomodoro Focus
        top_w = QWidget()
        top_split = QHBoxLayout(top_w); top_split.setContentsMargins(0, 0, 0, 0); top_split.setSpacing(16)

        prog_card = QFrame(self); prog_card.setProperty("class", "card"); pc_lay = QVBoxLayout(prog_card)
        self.lbl_task_summary = QLabel("Task Completion Progress: 0 of 0 Tasks Completed (0%)", self); self.lbl_task_summary.setStyleSheet("font-weight: bold; color: #ffffff;")
        pc_lay.addWidget(self.lbl_task_summary)
        self.task_progress_bar = QProgressBar(self); self.task_progress_bar.setFixedHeight(8)
        pc_lay.addWidget(self.task_progress_bar)
        top_split.addWidget(prog_card, stretch=2)

        pomo_card = QFrame(self); pomo_card.setProperty("class", "card"); po_lay = QVBoxLayout(pomo_card)
        pomo_hdr = QHBoxLayout()
        pomo_hdr.addWidget(QLabel("⏱️ POMODORO FOCUS TIMER", self))
        pomo_hdr.addStretch()
        self.lbl_pomo_sessions = QLabel("Completed: 0 sessions", self)
        self.lbl_pomo_sessions.setStyleSheet("font-size: 11px; color: #10b981; font-weight: bold;")
        pomo_hdr.addWidget(self.lbl_pomo_sessions)
        po_lay.addLayout(pomo_hdr)

        self.lbl_pomo_clock = QLabel("25:00", self); self.lbl_pomo_clock.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        po_lay.addWidget(self.lbl_pomo_clock, alignment=Qt.AlignmentFlag.AlignCenter)

        modes_lay = QHBoxLayout()
        btn_m_focus = QPushButton("Focus (25m)", self); btn_m_focus.setStyleSheet("font-size: 11px; padding: 4px;")
        btn_m_focus.clicked.connect(lambda: self.set_pomo_mode("Focus"))
        btn_m_short = QPushButton("Short Break (5m)", self); btn_m_short.setStyleSheet("font-size: 11px; padding: 4px;")
        btn_m_short.clicked.connect(lambda: self.set_pomo_mode("Short Break"))
        btn_m_long = QPushButton("Long Break (15m)", self); btn_m_long.setStyleSheet("font-size: 11px; padding: 4px;")
        btn_m_long.clicked.connect(lambda: self.set_pomo_mode("Long Break"))
        modes_lay.addWidget(btn_m_focus); modes_lay.addWidget(btn_m_short); modes_lay.addWidget(btn_m_long)
        po_lay.addLayout(modes_lay)

        pomo_btn_lay = QHBoxLayout()
        self.btn_pomo_toggle = QPushButton("Start Focus", self); self.btn_pomo_toggle.setProperty("class", "success"); self.btn_pomo_toggle.clicked.connect(self.toggle_pomo)
        btn_pomo_reset = QPushButton("Reset", self); btn_pomo_reset.clicked.connect(self.reset_pomo)
        pomo_btn_lay.addWidget(self.btn_pomo_toggle); pomo_btn_lay.addWidget(btn_pomo_reset)
        po_lay.addLayout(pomo_btn_lay)
        top_split.addWidget(pomo_card, stretch=1)

        splitter.addWidget(top_w)

        # Bottom Panel: Tasks Table
        bot_w = QWidget()
        bot_lay = QVBoxLayout(bot_w); bot_lay.setContentsMargins(0, 0, 0, 0); bot_lay.setSpacing(6)
        bot_lay.addWidget(QLabel("📋 TASK LIST & ACADEMIC GOALS (Drag divider above to adjust size ratio)", self))

        self.tasks_table = QTableWidget(self)
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["Title", "Category", "Due Date", "Priority", "Status", "Description", "Actions"])
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bot_lay.addWidget(self.tasks_table)

        splitter.addWidget(bot_w)
        splitter.setSizes([180, 520])

        main_lay.addWidget(splitter)
        self.views_stack.addWidget(view)

    def set_pomo_mode(self, mode):
        self.pomo_mode = mode
        self.reset_pomo()

    def toggle_pomo(self):
        if self.pomo_is_running:
            self.pomo_timer.stop(); self.pomo_is_running = False; self.btn_pomo_toggle.setText(f"Resume {self.pomo_mode}")
        else:
            self.pomo_timer.start(1000); self.pomo_is_running = True; self.btn_pomo_toggle.setText("Pause")

    def reset_pomo(self):
        self.pomo_timer.stop(); self.pomo_is_running = False
        if self.pomo_mode == "Focus":
            self.pomo_seconds = 25 * 60
            self.lbl_pomo_clock.setText("25:00")
            self.lbl_pomo_clock.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        elif self.pomo_mode == "Short Break":
            self.pomo_seconds = 5 * 60
            self.lbl_pomo_clock.setText("05:00")
            self.lbl_pomo_clock.setStyleSheet("font-size: 26px; font-weight: bold; color: #0ea5e9;")
        else: # Long Break
            self.pomo_seconds = 15 * 60
            self.lbl_pomo_clock.setText("15:00")
            self.lbl_pomo_clock.setStyleSheet("font-size: 26px; font-weight: bold; color: #f59e0b;")
        self.btn_pomo_toggle.setText(f"Start {self.pomo_mode}")

    def pomo_tick(self):
        if self.pomo_seconds > 0:
            self.pomo_seconds -= 1
            mins = self.pomo_seconds // 60; secs = self.pomo_seconds % 60
            self.lbl_pomo_clock.setText(f"{mins:02d}:{secs:02d}")
        else:
            self.pomo_timer.stop()
            self.pomo_is_running = False
            if self.pomo_mode == "Focus":
                self.pomo_sessions += 1
                if hasattr(self, 'lbl_pomo_sessions'):
                    self.lbl_pomo_sessions.setText(f"Completed: {self.pomo_sessions} sessions")
                self.send_notification("Focus Session Done! 🍅", "Great 25-minute focus session! Take a 5-minute break (+30 XP).")
                self.set_pomo_mode("Short Break")
            elif self.pomo_mode == "Short Break":
                self.send_notification("Break Ended! 🔔", "Break time is up. Ready for another focus session?")
                self.set_pomo_mode("Focus")
            else:
                self.send_notification("Long Break Ended! 🔔", "Long break is complete. Time to get back in the zone!")
                self.set_pomo_mode("Focus")
            self.refresh_badges_and_xp()

    # 5. ATTENDANCE & BUNK SAFETY CALCULATOR VIEW (with Draggable Size Ratio Splitter)
    def init_attendance_view(self):
        view = QWidget(self); main_lay = QVBoxLayout(view); main_lay.setContentsMargins(24, 24, 24, 24); main_lay.setSpacing(12)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Attendance Tracker & Bunk Safety Calculator", self))
        hdr_lay.addStretch()

        self.att_sem_combo = QComboBox(self)
        for i in range(1, 11): self.att_sem_combo.addItem(f"Semester {i}", i)
        self.att_sem_combo.currentIndexChanged.connect(self.refresh_attendance_table)
        hdr_lay.addWidget(self.att_sem_combo)

        btn_add_sub = QPushButton("+ Add Subject", self); btn_add_sub.clicked.connect(self.open_subject_dialog)
        hdr_lay.addWidget(btn_add_sub)
        main_lay.addLayout(hdr_lay)

        splitter = QSplitter(Qt.Orientation.Vertical, self)

        # Top Panel: Subject Cards Container
        top_w = QWidget()
        top_lay = QVBoxLayout(top_w); top_lay.setContentsMargins(0, 0, 0, 0); top_lay.setSpacing(6)
        top_lay.addWidget(QLabel("🏛️ SUBJECT ATTENDANCE & BUNK SAFETY CARDS (Drag bar below to adjust size ratio)", self))

        self.sub_cards_area = QWidget(self)
        self.sub_cards_lay = QGridLayout(self.sub_cards_area)
        top_lay.addWidget(self.sub_cards_area)
        splitter.addWidget(top_w)

        # Bottom Panel: Attendance History Table
        bot_w = QWidget()
        bot_lay = QVBoxLayout(bot_w); bot_lay.setContentsMargins(0, 0, 0, 0); bot_lay.setSpacing(6)

        self.att_search = QLineEdit(self); self.att_search.setPlaceholderText("Search subject or date..."); self.att_search.textChanged.connect(self.refresh_attendance_table)
        bot_lay.addWidget(self.att_search)

        self.att_table = QTableWidget(self)
        self.att_table.setColumnCount(6)
        self.att_table.setHorizontalHeaderLabels(["Date", "Semester", "Subject", "Status", "Remarks", "Actions"])
        self.att_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bot_lay.addWidget(self.att_table)

        splitter.addWidget(bot_w)
        splitter.setSizes([260, 440])

        main_lay.addWidget(splitter)
        self.views_stack.addWidget(view)

    # 6. FINANCE & TARGETED SAVINGS VIEW (with Draggable Splitter & Smooth ScrollArea)
    def init_finance_view(self):
        view = QWidget(self); main_lay = QVBoxLayout(view); main_lay.setContentsMargins(24, 24, 24, 24); main_lay.setSpacing(12)

        hdr_lay = QHBoxLayout()
        hdr_lay.addWidget(QLabel("Finance Ledger & Targeted Savings Goals", self))
        hdr_lay.addStretch()

        btn_split = QPushButton("🧾 + Split Bill / Expense", self); btn_split.clicked.connect(self.open_group_expense_dialog)
        hdr_lay.addWidget(btn_split)

        btn_add_sg = QPushButton("🎯 + New Savings Goal", self); btn_add_sg.setProperty("class", "success"); btn_add_sg.clicked.connect(self.open_savings_goal_dialog)
        hdr_lay.addWidget(btn_add_sg)

        btn_rec_allow = QPushButton("+ Receive Allowance", self); btn_rec_allow.clicked.connect(lambda: self.open_finance_dialog("Income"))
        hdr_lay.addWidget(btn_rec_allow)

        btn_log_exp = QPushButton("+ Log Expense", self); btn_log_exp.setProperty("class", "primary"); btn_log_exp.clicked.connect(lambda: self.open_finance_dialog("Expense"))
        hdr_lay.addWidget(btn_log_exp)

        main_lay.addLayout(hdr_lay)

        splitter = QSplitter(Qt.Orientation.Vertical, self)

        # Top Panel: Scrollable Container for Expense Splitter, Savings Goals, Graphs
        top_scroll = QScrollArea(self)
        top_scroll.setWidgetResizable(True)
        top_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        top_content = QWidget()
        tc_lay = QVBoxLayout(top_content); tc_lay.setContentsMargins(0, 0, 0, 0); tc_lay.setSpacing(12)

        # Roommate Group Expense Splitter Card
        ge_card = QFrame(self); ge_card.setProperty("class", "card"); gec_lay = QVBoxLayout(ge_card)
        gec_lay.addWidget(QLabel("🧾 ROOMMATE & GROUP EXPENSE SPLITTER", self))

        self.ge_table = QTableWidget(self)
        self.ge_table.setColumnCount(6)
        self.ge_table.setHorizontalHeaderLabels(["Date", "Title / Bill", "Total Bill", "Paid By", "Share Per Person", "Actions"])
        self.ge_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ge_table.setFixedHeight(110)
        gec_lay.addWidget(self.ge_table)
        tc_lay.addWidget(ge_card)

        sg_header = QLabel("🎯 TARGETED SAVINGS GOALS & WISHLIST", self); sg_header.setProperty("class", "h3")
        tc_lay.addWidget(sg_header)

        self.savings_cards_area = QWidget(self)
        self.savings_cards_lay = QGridLayout(self.savings_cards_area)
        tc_lay.addWidget(self.savings_cards_area)

        graph_card = QFrame(self); graph_card.setProperty("class", "card")
        gc_lay = QVBoxLayout(graph_card); gc_lay.setContentsMargins(10, 10, 10, 10)

        self.finance_canvas = FinanceChartCanvas(self, width=9, height=2.8, dpi=100)
        gc_lay.addWidget(self.finance_canvas)
        tc_lay.addWidget(graph_card)

        top_scroll.setWidget(top_content)
        splitter.addWidget(top_scroll)

        # Bottom Panel: Transaction Ledger Table
        bot_w = QWidget()
        bot_lay = QVBoxLayout(bot_w); bot_lay.setContentsMargins(0, 0, 0, 0); bot_lay.setSpacing(6)
        bot_lay.addWidget(QLabel("💰 TRANSACTION LEDGER (Drag divider above to adjust size ratio)", self))

        self.fin_search = QLineEdit(self); self.fin_search.setPlaceholderText("Search transaction description or category..."); self.fin_search.textChanged.connect(self.refresh_finance_table)
        bot_lay.addWidget(self.fin_search)

        self.fin_table = QTableWidget(self)
        self.fin_table.setColumnCount(6)
        self.fin_table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Description", "Amount (₹)", "Actions"])
        self.fin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bot_lay.addWidget(self.fin_table)

        splitter.addWidget(bot_w)
        splitter.setSizes([380, 420])

        main_lay.addWidget(splitter)
        self.views_stack.addWidget(view)

    def open_group_expense_dialog(self):
        dlg = QDialog(self); dlg.setWindowTitle("Split Bill / Group Expense"); dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)

        title_in = QLineEdit(dlg); title_in.setPlaceholderText("e.g. Hostel Wi-Fi, Trip, Dinner")
        tot_in = QLineEdit(dlg); tot_in.setPlaceholderText("Total Bill Amount (₹)")
        paid_in = QLineEdit(dlg); paid_in.setText("Akul")
        count_in = QLineEdit(dlg); count_in.setText("3")

        lay.addWidget(QLabel("Bill Title:", dlg)); lay.addWidget(title_in)
        lay.addWidget(QLabel("Total Amount (₹):", dlg)); lay.addWidget(tot_in)
        lay.addWidget(QLabel("Paid By:", dlg)); lay.addWidget(paid_in)
        lay.addWidget(QLabel("Total People Splitting:", dlg)); lay.addWidget(count_in)

        btn_save = QPushButton("Calculate & Save Split", dlg); btn_save.setProperty("class", "primary")
        lay.addWidget(btn_save)

        def save():
            try:
                tot = float(tot_in.text())
                cnt = int(count_in.text())
                share = tot / max(1, cnt)

                db.save_group_expense({
                    'id': f"ge-{int(datetime.now().timestamp())}",
                    'title': title_in.text(),
                    'totalAmount': tot,
                    'paidBy': paid_in.text(),
                    'peopleCount': cnt,
                    'sharePerPerson': share,
                    'date': date.today().strftime("%Y-%m-%d"),
                    'notes': f"Split between {cnt} people"
                })
                dlg.accept()
                self.refresh_all_views()
            except ValueError:
                pass

        btn_save.clicked.connect(save)
        dlg.exec()

    # 7. TIMETABLE VIEW (Upgraded with Live Today Hero Card, Day Filters, Conflict Detection, 1-Click Attendance)
    def init_timetable_view(self):
        view = QWidget(self); lay = QVBoxLayout(view); lay.setContentsMargins(24, 24, 24, 24); lay.setSpacing(14)

        # 1. Top Controls Bar
        hdr_lay = QHBoxLayout()
        lbl_tt = QLabel("Weekly Lecture Timetable & Schedule Intelligence", self)
        lbl_tt.setProperty("class", "h2")
        hdr_lay.addWidget(lbl_tt)
        hdr_lay.addStretch()

        self.tt_sem_filter = QComboBox(self)
        self.tt_sem_filter.addItem("All Semesters", 0)
        for i in range(1, 11):
            self.tt_sem_filter.addItem(f"Semester {i}", i)
        self.tt_sem_filter.currentIndexChanged.connect(self.refresh_timetable_table)
        hdr_lay.addWidget(self.tt_sem_filter)

        btn_sample = QPushButton("⚡ Load Sample Schedule", self)
        btn_sample.setStyleSheet("background: rgba(99, 102, 241, 0.2); border: 1px solid #6366f1; color: #818cf8; font-weight: bold; border-radius: 6px; padding: 6px 12px;")
        btn_sample.clicked.connect(self.load_sample_schedule)
        hdr_lay.addWidget(btn_sample)

        btn_ics = QPushButton("📅 Export .ics Calendar", self)
        btn_ics.setProperty("class", "success")
        btn_ics.clicked.connect(self.export_ics_calendar)
        hdr_lay.addWidget(btn_ics)

        btn_add_slot = QPushButton("+ Add Class Slot", self)
        btn_add_slot.clicked.connect(self.open_timetable_dialog)
        hdr_lay.addWidget(btn_add_slot)
        lay.addLayout(hdr_lay)

        # 2. Today's Live Lecture Schedule Hero Card
        self.tt_live_card = QFrame(self)
        self.tt_live_card.setProperty("class", "hero-card")
        self.tt_live_card.setStyleSheet("background: #111422; border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 14px;")
        live_lay = QVBoxLayout(self.tt_live_card)
        live_lay.setContentsMargins(14, 12, 14, 12)
        live_lay.setSpacing(8)

        live_top = QHBoxLayout()
        self.tt_live_title = QLabel("📅 Today's Live Lecture Schedule", self)
        self.tt_live_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff;")
        live_top.addWidget(self.tt_live_title)
        live_top.addStretch()

        self.tt_live_badge = QLabel("🟢 Live Schedule", self)
        self.tt_live_badge.setStyleSheet("background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #10b981; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 12px;")
        live_top.addWidget(self.tt_live_badge)
        live_lay.addLayout(live_top)

        self.tt_live_active_info = QLabel("Loading schedule...", self)
        self.tt_live_active_info.setStyleSheet("font-size: 13px; color: #cbd5e1; line-height: 1.4;")
        live_lay.addWidget(self.tt_live_active_info)

        # 1-Click Attendance Buttons row
        self.tt_live_actions_widget = QWidget(self)
        btn_row = QHBoxLayout(self.tt_live_actions_widget)
        btn_row.setContentsMargins(0, 4, 0, 0)
        btn_row.setSpacing(8)

        lbl_quick = QLabel("Quick Attendance for Active Class:", self)
        lbl_quick.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: bold;")
        btn_row.addWidget(lbl_quick)

        self.btn_live_present = QPushButton("✅ Mark Present Today", self)
        self.btn_live_present.setStyleSheet("background: rgba(16, 185, 129, 0.25); border: 1px solid #10b981; color: #34d399; font-weight: bold; padding: 6px 14px; border-radius: 6px;")
        self.btn_live_present.clicked.connect(lambda: self.quick_log_active_lecture("Present"))
        btn_row.addWidget(self.btn_live_present)

        self.btn_live_absent = QPushButton("❌ Mark Absent / Bunked", self)
        self.btn_live_absent.setStyleSheet("background: rgba(244, 63, 94, 0.25); border: 1px solid #f43f5e; color: #fb7185; font-weight: bold; padding: 6px 14px; border-radius: 6px;")
        self.btn_live_absent.clicked.connect(lambda: self.quick_log_active_lecture("Absent"))
        btn_row.addWidget(self.btn_live_absent)

        self.btn_live_cancelled = QPushButton("⚠️ Class Cancelled", self)
        self.btn_live_cancelled.setStyleSheet("background: rgba(245, 158, 11, 0.25); border: 1px solid #f59e0b; color: #fcd34d; font-weight: bold; padding: 6px 14px; border-radius: 6px;")
        self.btn_live_cancelled.clicked.connect(lambda: self.quick_log_active_lecture("Cancelled"))
        btn_row.addWidget(self.btn_live_cancelled)

        btn_row.addStretch()
        live_lay.addWidget(self.tt_live_actions_widget)

        # Container for today's multiple classes mini cards
        self.tt_today_classes_container = QWidget(self)
        self.tt_today_classes_lay = QHBoxLayout(self.tt_today_classes_container)
        self.tt_today_classes_lay.setContentsMargins(0, 4, 0, 0)
        self.tt_today_classes_lay.setSpacing(8)
        live_lay.addWidget(self.tt_today_classes_container)

        lay.addWidget(self.tt_live_card)

        # 3. Conflict / Overlap Alert Banner
        self.tt_conflict_banner = QFrame(self)
        self.tt_conflict_banner.setStyleSheet("background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 8px; padding: 8px 14px;")
        conf_lay = QHBoxLayout(self.tt_conflict_banner)
        conf_lay.setContentsMargins(8, 4, 8, 4)
        self.tt_conflict_label = QLabel(self)
        self.tt_conflict_label.setStyleSheet("color: #fbbf24; font-weight: bold; font-size: 12px;")
        conf_lay.addWidget(self.tt_conflict_label)
        conf_lay.addStretch()
        self.tt_conflict_banner.setVisible(False)
        lay.addWidget(self.tt_conflict_banner)

        # 4. Day Selector Filter Tabs
        day_bar = QHBoxLayout()
        day_bar.setSpacing(6)
        self.tt_selected_day = "All"
        self.tt_day_btns = {}
        day_list = ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for d in day_list:
            btn = QPushButton(d, self)
            btn.setStyleSheet("background: #141724; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 6px 14px; color: #cbd5e1; font-weight: bold;")
            btn.clicked.connect(lambda checked, day=d: self.filter_timetable_by_day(day))
            self.tt_day_btns[d] = btn
            day_bar.addWidget(btn)
        day_bar.addStretch()
        lay.addLayout(day_bar)

        # 5. Timetable Ledger Table
        self.tt_table = QTableWidget(self)
        self.tt_table.setColumnCount(7)
        self.tt_table.setHorizontalHeaderLabels(["Day / Sem", "Time Slot", "Subject", "Location / Room", "Instructor", "Conflict Status", "Actions"])
        self.tt_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.tt_table, stretch=1)

        self.views_stack.addWidget(view)

    def export_ics_calendar(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Timetable .ics Calendar", "STUNT_Timetable.ics", "iCalendar Files (*.ics);;All Files (*)")
        if file_path:
            ics_lines = [
                "BEGIN:VCALENDAR",
                "VERSION:2.0",
                "PRODID:-//STUNT Platform//NONSGML Timetable Calendar//EN"
            ]
            for slot in self.data['timetable']:
                ics_lines.extend([
                    "BEGIN:VEVENT",
                    f"SUMMARY:{slot['subject']} ({slot['location']})",
                    f"DESCRIPTION:Instructor: {slot['instructor']} | Day: {slot['day']} | Sem {slot.get('sem', 1)}",
                    f"LOCATION:{slot['location']}",
                    "END:VEVENT"
                ])
            ics_lines.append("END:VCALENDAR")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(ics_lines))
            QMessageBox.information(self, "ICS Calendar Exported", f".ics file exported to {file_path}!\nYou can double-click it to open in Google Calendar, Apple Calendar, or Outlook.")

    # 8. MEMORIES VIEW (with Double-Click High-Res Preview & Deletion)
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
        self.mem_list.itemDoubleClicked.connect(self.view_memory_dialog)
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

        self.refresh_notes_table()
        self.refresh_group_expenses_table()
        self.refresh_syllabus_table()
        self.refresh_savings_goals_cards()
        self.refresh_grades_table()
        self.refresh_tasks_table()
        self.refresh_attendance_table()
        self.refresh_finance_table()
        self.refresh_timetable_table()
        self.refresh_memories_grid()
        self.refresh_milestones_table()
        self.refresh_heatmap()
        self.refresh_badges_and_xp()

        self.finance_canvas.update_charts(self.data['finances'])

    # DYNAMIC 7-DAY PRODUCTIVITY HEATMAP
    def refresh_heatmap(self):
        if not hasattr(self, 'heat_grid_lay'):
            return

        while self.heat_grid_lay.count():
            item = self.heat_grid_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        today = date.today()
        dates_to_check = [today - timedelta(days=i) for i in range(6, -1, -1)]

        for d in dates_to_check:
            d_str = d.strftime("%Y-%m-%d")
            att_c = sum(1 for l in self.data.get('attendanceLogs', []) if l.get('date') == d_str)
            tasks_c = sum(1 for t in self.data.get('tasks', []) if t.get('dueDate') == d_str and t.get('status') == 'Completed')
            fin_c = sum(1 for f in self.data.get('finances', []) if f.get('date') == d_str)
            mem_c = sum(1 for m in self.data.get('memories', []) if m.get('date') == d_str)
            ms_c = sum(1 for ms in self.data.get('milestones', []) if ms.get('date') == d_str)
            tot_acts = att_c + tasks_c + fin_c + mem_c + ms_c

            day_box = QFrame(self)
            day_box.setFixedSize(72, 54)

            if tot_acts == 0:
                day_box.setStyleSheet("background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px;")
                val_text = "Idle"
                val_color = "#64748b"
            elif tot_acts <= 2:
                day_box.setStyleSheet("background: rgba(99, 102, 241, 0.25); border: 1px solid rgba(99, 102, 241, 0.5); border-radius: 6px;")
                val_text = f"{tot_acts} Log{'s' if tot_acts > 1 else ''}"
                val_color = "#818cf8"
            else:
                day_box.setStyleSheet("background: rgba(16, 185, 129, 0.25); border: 1px solid rgba(16, 185, 129, 0.6); border-radius: 6px;")
                val_text = f"{tot_acts} Active"
                val_color = "#10b981"

            db_lay = QVBoxLayout(day_box)
            db_lay.setContentsMargins(4, 4, 4, 4)
            db_lay.setSpacing(2)

            day_name = d.strftime("%a %d")
            lbl = QLabel(day_name, day_box)
            lbl.setStyleSheet("font-size: 10px; color: #cbd5e1;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            val = QLabel(val_text, day_box)
            val.setStyleSheet(f"font-weight: bold; color: {val_color}; font-size: 11px;")
            val.setAlignment(Qt.AlignmentFlag.AlignCenter)

            db_lay.addWidget(lbl)
            db_lay.addWidget(val)
            self.heat_grid_lay.addWidget(day_box)

    # DYNAMIC STUDENT BADGES & XP PROGRESSION
    def refresh_badges_and_xp(self):
        grades = self.data.get('grades', [])
        total_pts = sum(g['credits'] * g['gradePoints'] for g in grades)
        total_creds = sum(g['credits'] for g in grades)
        cgpa = (total_pts / total_creds) if total_creds > 0 else 0.00

        logs = self.data.get('attendanceLogs', [])
        p_count = sum(1 for l in logs if l['status'] == 'Present')
        att_pct = (p_count / len(logs) * 100.0) if logs else 0.0

        tasks = self.data.get('tasks', [])
        tasks_done = sum(1 for t in tasks if t['status'] == 'Completed')

        syl = self.data.get('syllabus', [])
        syl_done = sum(1 for item in syl if item['status'] == 'Completed')

        savings = self.data.get('savingsGoals', [])
        savings_mastered = sum(1 for sg in savings if sg['currentSaved'] >= sg['targetAmount'] and sg['targetAmount'] > 0)

        # Gamified Student XP
        xp = (tasks_done * 25) + (len(logs) * 10) + (syl_done * 20) + (self.pomo_sessions * 30) + (savings_mastered * 50)
        level = 1 + (xp // 100)

        if hasattr(self, 'lbl_xp'):
            self.lbl_xp.setText(f"Level {level} Scholar • {xp} XP")

        unlocked = []
        if cgpa >= 9.0 and total_creds > 0:
            unlocked.append("🥇 Dean's List")
        elif total_creds > 0:
            unlocked.append(f"🎓 Honor Track ({cgpa:.2f}/9.0)")

        target_att = self.profile.get('targetAttendancePct', 75.0)
        if att_pct >= target_att and len(logs) > 0:
            unlocked.append("🟢 Bunk Master")
        elif len(logs) > 0:
            unlocked.append("⚠️ Att Warning")

        if savings_mastered > 0:
            unlocked.append("💰 Savings Champion")

        if tasks_done >= 3:
            unlocked.append("🎯 Task Achiever")

        if syl_done >= 3:
            unlocked.append("📚 Syllabus Scholar")

        if self.pomo_sessions >= 1:
            unlocked.append("⏱️ Focus Beast")

        if not unlocked:
            unlocked = ["🌱 Fresher Rookie"]

        if hasattr(self, 'lbl_badges'):
            self.lbl_badges.setText(" • ".join(unlocked))

    # REFRESH NOTES TABLE
    def refresh_notes_table(self):
        notes = self.data.get('subjectNotes', [])
        self.notes_table.setRowCount(len(notes))
        for row, sn in enumerate(notes):
            self.notes_table.setItem(row, 0, QTableWidgetItem(sn['subjectName']))
            self.notes_table.setItem(row, 1, QTableWidgetItem(sn['title']))
            self.notes_table.setItem(row, 2, QTableWidgetItem(sn['fileType']))
            self.notes_table.setItem(row, 3, QTableWidgetItem(sn['date']))

            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget); act_lay.setContentsMargins(0, 0, 0, 0); act_lay.setSpacing(4)

            btn_open = QPushButton("Open File 📂", self); btn_open.setProperty("class", "primary")
            btn_open.clicked.connect(lambda checked, path=sn['filePath']: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))
            act_lay.addWidget(btn_open)

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, snid=sn['id']: self.delete_note(snid))
            act_lay.addWidget(btn_del)

            self.notes_table.setCellWidget(row, 4, act_widget)

    def delete_note(self, snid):
        db.delete_subject_note(snid)
        self.refresh_all_views()

    # REFRESH GROUP EXPENSES TABLE
    def refresh_group_expenses_table(self):
        ges = self.data.get('groupExpenses', [])
        self.ge_table.setRowCount(len(ges))
        for row, ge in enumerate(ges):
            self.ge_table.setItem(row, 0, QTableWidgetItem(ge['date']))
            self.ge_table.setItem(row, 1, QTableWidgetItem(ge['title']))
            self.ge_table.setItem(row, 2, QTableWidgetItem(f"₹{ge['totalAmount']:,.0f}"))
            self.ge_table.setItem(row, 3, QTableWidgetItem(ge['paidBy']))
            self.ge_table.setItem(row, 4, QTableWidgetItem(f"₹{ge['sharePerPerson']:,.0f} ({ge['peopleCount']} ppl)"))

            btn_del = QPushButton("Delete", self); btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, geid=ge['id']: self.delete_ge(geid))
            self.ge_table.setCellWidget(row, 5, btn_del)

    def delete_ge(self, geid):
        db.delete_group_expense(geid)
        self.refresh_all_views()

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

    # FORMATTED PDF / HTML REPORT EXPORTER
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

            logs = self.data.get('attendanceLogs', [])
            p_count = sum(1 for l in logs if l['status'] == 'Present')
            att_pct = (p_count / len(logs) * 100.0) if logs else 0.0

            tasks = self.data.get('tasks', [])
            done_tasks = sum(1 for t in tasks if t['status'] == 'Completed')
            syl = self.data.get('syllabus', [])
            done_syl = sum(1 for s in syl if s['status'] == 'Completed')

            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>STUNT Official Academic & Financial Transcript</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #0a0b10;
            color: #f8fafc;
            padding: 36px;
            margin: 0;
            line-height: 1.5;
        }}
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #6366f1;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        h1 {{ margin: 0; color: #6366f1; font-size: 26px; }}
        .badge-pill {{
            background: rgba(99, 102, 241, 0.2);
            color: #818cf8;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            border: 1px solid rgba(99, 102, 241, 0.4);
        }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
        .card {{
            background: #141622;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .card h2 {{
            margin-top: 0;
            font-size: 16px;
            color: #0ea5e9;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            padding-bottom: 8px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 13px;
        }}
        th, td {{
            border: 1px solid rgba(255,255,255,0.08);
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background: #1e2235;
            color: #93c5fd;
            font-weight: 600;
        }}
        tr:nth-child(even) {{ background: rgba(255,255,255,0.02); }}
        .highlight {{ color: #10b981; font-weight: bold; }}
        .danger {{ color: #f43f5e; font-weight: bold; }}
        .footer {{
            margin-top: 36px;
            padding-top: 16px;
            border-top: 1px solid rgba(255,255,255,0.08);
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #64748b;
        }}
        @media print {{
            body {{
                background-color: #ffffff !important;
                color: #0f172a !important;
                padding: 15mm !important;
            }}
            .card {{
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                box-shadow: none !important;
            }}
            th {{
                background: #f1f5f9 !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
            }}
            td {{
                border: 1px solid #cbd5e1 !important;
                color: #334155 !important;
            }}
            .header-bar {{
                border-bottom: 2px solid #334155 !important;
            }}
            h1 {{ color: #0f172a !important; }}
            .card h2 {{ color: #1e293b !important; border-bottom: 1px solid #cbd5e1 !important; }}
            .highlight {{ color: #059669 !important; }}
            .danger {{ color: #dc2626 !important; }}
        }}
    </style>
</head>
<body>
    <div class="header-bar">
        <div>
            <h1>STUNT — Academic & Financial Degree Transcript</h1>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Student Tracker for Unified Navigation & Tasks</div>
        </div>
        <div class="badge-pill">OFFICIAL STUDENT RECORD</div>
    </div>

    <div class="grid-2">
        <div class="card">
            <h2>🎓 Student Academic Profile</h2>
            <p><b>Name:</b> {p.get('name')}</p>
            <p><b>College / University:</b> {p.get('college')}</p>
            <p><b>Degree & Course:</b> {p.get('course')} ({p.get('batch')})</p>
            <p><b>Journey Timeline:</b> {p.get('startDate')} to {p.get('endDate')} ({p.get('totalSemesters')} Semesters)</p>
        </div>

        <div class="card">
            <h2>📊 Performance & Metrics Summary</h2>
            <p><b>Cumulative CGPA:</b> <span class="highlight">{cgpa:.2f} / 10.0</span> (Target: {p.get('targetCgpa')})</p>
            <p><b>Overall Attendance:</b> <span class="{'highlight' if att_pct >= p.get('targetAttendancePct', 75.0) else 'danger'}">{att_pct:.1f}%</span> (Min: {p.get('targetAttendancePct', 75.0)}%)</p>
            <p><b>Syllabus Units Completed:</b> {done_syl} / {len(syl)} units ({(done_syl/len(syl)*100 if syl else 0):.0f}%)</p>
            <p><b>Net Wallet Balance:</b> <span class="highlight">₹{inc - exp:,.0f}</span> (Cap: ₹{p.get('monthlyBudgetCap'):,.0f})</p>
        </div>
    </div>

    <div class="card" style="margin-bottom: 24px;">
        <h2>📜 Subject Grades & SGPA Ledger</h2>
        <table>
            <tr><th>Semester</th><th>Code</th><th>Subject Name</th><th>Credits</th><th>Grade Points</th></tr>
            {''.join(f"<tr><td>Sem {g['sem']}</td><td>{g['subjectCode']}</td><td>{g['subjectName']}</td><td>{g['credits']}</td><td>{g['gradePoints']}</td></tr>" for g in grades) if grades else "<tr><td colspan='5'>No grades logged yet.</td></tr>"}
        </table>
    </div>

    <div class="grid-2">
        <div class="card">
            <h2>🎯 Targeted Savings Goals</h2>
            <table>
                <tr><th>Goal</th><th>Target</th><th>Saved</th><th>Status</th></tr>
                {''.join(f"<tr><td>{sg['title']}</td><td>₹{sg['targetAmount']:,.0f}</td><td>₹{sg['currentSaved']:,.0f}</td><td>{min(100.0, sg['currentSaved']/max(1.0, sg['targetAmount'])*100):.0f}%</td></tr>" for sg in self.data.get('savingsGoals', [])) if self.data.get('savingsGoals') else "<tr><td colspan='4'>No savings goals logged.</td></tr>"}
            </table>
        </div>

        <div class="card">
            <h2>✅ Academic Goals & Tasks Overview</h2>
            <p>Total Tasks Logged: <b>{len(tasks)}</b> | Completed: <b class="highlight">{done_tasks}</b></p>
            <table>
                <tr><th>Task</th><th>Due Date</th><th>Priority</th><th>Status</th></tr>
                {''.join(f"<tr><td>{t['title']}</td><td>{t['dueDate']}</td><td>{t['priority']}</td><td>{t['status']}</td></tr>" for t in tasks[:6]) if tasks else "<tr><td colspan='4'>No tasks logged.</td></tr>"}
            </table>
        </div>
    </div>

    <div class="footer">
        <div>Generated via STUNT Desktop Platform • Report Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
        <div>© 2026 Akul. All Rights Reserved.</div>
    </div>
</body>
</html>
"""
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            QMessageBox.information(self, "Export Complete", f"Academic Transcript exported to {file_path}!\nYou can open and print it (Ctrl+P) directly from your web browser.")

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

    def filter_timetable_by_day(self, day_name):
        self.tt_selected_day = day_name.split()[0] if day_name != "All Days" else "All"
        self.refresh_timetable_table()

    def check_timetable_conflicts(self, slots):
        conflicts = []
        from collections import defaultdict
        groups = defaultdict(list)
        for s in slots:
            groups[(s.get('sem', 1), s.get('day', '').strip().lower())].append(s)
        
        for (sem, day), group in groups.items():
            n = len(group)
            for i in range(n):
                for j in range(i + 1, n):
                    s1, s2 = group[i], group[j]
                    m1_start = parse_time_to_minutes(s1.get('start', ''))
                    m1_end = parse_time_to_minutes(s1.get('end', ''))
                    m2_start = parse_time_to_minutes(s2.get('start', ''))
                    m2_end = parse_time_to_minutes(s2.get('end', ''))
                    if m1_start is not None and m1_end is not None and m2_start is not None and m2_end is not None:
                        if m1_start < m2_end and m2_start < m1_end:
                            conflicts.append((s1['id'], s2['id'], s1['subject'], s2['subject'], day.title(), sem))
        return conflicts

    # TIMETABLE TABLE (Upgraded with Live Today Hero Card, Day Filters, Conflict Detection, 1-Click Attendance)
    def refresh_timetable_table(self):
        all_tt = self.data.get('timetable', [])
        now_dt = datetime.now()
        day_name = now_dt.strftime("%A")
        date_str = now_dt.strftime("%d %B %Y")
        now_mins = now_dt.hour * 60 + now_dt.minute

        # 1. Evaluate Conflicts across all slots
        conflicts = self.check_timetable_conflicts(all_tt)
        conflict_ids = set()
        conflict_msgs = []
        for c in conflicts:
            conflict_ids.add(c[0])
            conflict_ids.add(c[1])
            conflict_msgs.append(f"{c[4]} Sem {c[5]}: '{c[2]}' overlaps with '{c[3]}'")

        if conflict_msgs and hasattr(self, 'tt_conflict_banner'):
            self.tt_conflict_label.setText(f"⚠️ Schedule Conflicts ({len(conflicts)} detected): " + " • ".join(conflict_msgs[:3]))
            self.tt_conflict_banner.setVisible(True)
        elif hasattr(self, 'tt_conflict_banner'):
            self.tt_conflict_banner.setVisible(False)

        # 2. Update Day Selector Tab Labels with Class Counts
        if hasattr(self, 'tt_day_btns'):
            for d, btn in self.tt_day_btns.items():
                if d == "All Days":
                    cnt = len(all_tt)
                    label = f"All Days ({cnt})"
                    active = (getattr(self, 'tt_selected_day', 'All') == "All")
                else:
                    cnt = sum(1 for s in all_tt if s.get('day', '').lower() == d.lower())
                    is_today = (d.lower() == day_name.lower())
                    star = " ⭐" if is_today else ""
                    label = f"{d} ({cnt}){star}"
                    active = (getattr(self, 'tt_selected_day', 'All').lower() == d.lower())
                
                btn.setText(label)
                if active:
                    btn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #0ea5e9); border: 1px solid #6366f1; color: #ffffff; font-weight: bold; border-radius: 8px; padding: 6px 14px;")
                else:
                    btn.setStyleSheet("background: #141724; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 6px 14px; color: #cbd5e1; font-weight: normal;")

        # 3. Update Today's Live Lecture Hero Card
        today_slots = [s for s in all_tt if s.get('day', '').lower() == day_name.lower()]
        if hasattr(self, 'tt_live_title'):
            self.tt_live_title.setText(f"📅 Today is {day_name}, {date_str} • Schedule Live Telemetry")

        active_slot = None
        next_slot = None
        min_diff = 999999

        for s in today_slots:
            sm = parse_time_to_minutes(s.get('start', ''))
            em = parse_time_to_minutes(s.get('end', ''))
            if sm is None or em is None: continue
            if sm <= now_mins <= em:
                active_slot = s
                break
            diff = sm - now_mins
            if 0 < diff < min_diff:
                min_diff = diff
                next_slot = s

        self.current_active_or_next_slot = active_slot or next_slot or (today_slots[0] if today_slots else None)

        if hasattr(self, 'tt_live_badge') and hasattr(self, 'tt_live_active_info'):
            if active_slot:
                em = parse_time_to_minutes(active_slot.get('end', ''))
                rem = (em - now_mins) if em else 0
                self.tt_live_badge.setText("🔴 CURRENTLY IN CLASS")
                self.tt_live_badge.setStyleSheet("background: rgba(239, 68, 68, 0.25); border: 1px solid #ef4444; color: #f87171; font-weight: bold; padding: 4px 12px; border-radius: 12px;")
                self.tt_live_active_info.setText(
                    f"<b style='font-size: 15px; color: #f8fafc;'>{active_slot['subject']}</b> "
                    f"<span style='color: #38bdf8;'>({active_slot['start']} - {active_slot['end']})</span> • "
                    f"Room: <b>{active_slot.get('location', 'N/A')}</b> • Faculty: <b>{active_slot.get('instructor', 'N/A')}</b><br>"
                    f"<span style='color: #10b981;'>⏳ Remaining time in class: approx {rem} minutes.</span>"
                )
                self.tt_live_actions_widget.setVisible(True)
            elif next_slot:
                hours = min_diff // 60
                mins = min_diff % 60
                countdown_str = f"{hours}h {mins}m" if hours > 0 else f"{mins} mins"
                self.tt_live_badge.setText(f"⏳ UPCOMING IN {countdown_str.upper()}")
                self.tt_live_badge.setStyleSheet("background: rgba(245, 158, 11, 0.25); border: 1px solid #f59e0b; color: #fbbf24; font-weight: bold; padding: 4px 12px; border-radius: 12px;")
                self.tt_live_active_info.setText(
                    f"<b style='font-size: 15px; color: #f8fafc;'>Next: {next_slot['subject']}</b> "
                    f"<span style='color: #38bdf8;'>at {next_slot['start']}</span> • "
                    f"Room: <b>{next_slot.get('location', 'N/A')}</b> • Faculty: <b>{next_slot.get('instructor', 'N/A')}</b><br>"
                    f"<span style='color: #94a3b8;'>Starts in {countdown_str}. Pack your bag or head to the room!</span>"
                )
                self.tt_live_actions_widget.setVisible(True)
            elif today_slots:
                self.tt_live_badge.setText("✅ LECTURES WRAPPED UP")
                self.tt_live_badge.setStyleSheet("background: rgba(16, 185, 129, 0.25); border: 1px solid #10b981; color: #34d399; font-weight: bold; padding: 4px 12px; border-radius: 12px;")
                self.tt_live_active_info.setText(
                    f"All {len(today_slots)} lectures for {day_name} have completed! Great hustle today, Akul.<br>"
                    f"Review today's notes or log attendance if you haven't yet."
                )
                self.tt_live_actions_widget.setVisible(True)
            else:
                self.tt_live_badge.setText("🏖️ NO CLASSES SCHEDULED")
                self.tt_live_badge.setStyleSheet("background: rgba(148, 163, 184, 0.2); border: 1px solid #64748b; color: #94a3b8; font-weight: bold; padding: 4px 12px; border-radius: 12px;")
                self.tt_live_active_info.setText(
                    f"Zero lectures on your timetable for {day_name}. It's a free runway, bro! Catch up on syllabus or relax.<br>"
                    f"If you have classes, click <i>'+ Add Class Slot'</i> or <i>'⚡ Load Sample Schedule'</i> above."
                )
                self.tt_live_actions_widget.setVisible(False)

        # Mini chips for all today's classes
        if hasattr(self, 'tt_today_classes_lay'):
            while self.tt_today_classes_lay.count():
                child = self.tt_today_classes_lay.takeAt(0)
                if child.widget(): child.widget().deleteLater()

            if today_slots:
                lbl_all_today = QLabel(f"Today's Classes ({len(today_slots)}):", self)
                lbl_all_today.setStyleSheet("font-size: 11px; color: #94a3b8; font-weight: bold;")
                self.tt_today_classes_lay.addWidget(lbl_all_today)

                for slot in today_slots:
                    chip = QFrame(self)
                    chip.setStyleSheet("background: #171a2b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 4px 8px;")
                    c_lay = QHBoxLayout(chip)
                    c_lay.setContentsMargins(6, 2, 6, 2)
                    c_lay.setSpacing(6)
                    c_lbl = QLabel(f"<b>{slot['subject']}</b> ({slot['start']})", chip)
                    c_lbl.setStyleSheet("font-size: 11px; color: #e2e8f0;")
                    c_lay.addWidget(c_lbl)

                    btn_p = QPushButton("✔", chip)
                    btn_p.setToolTip(f"Mark Present in {slot['subject']}")
                    btn_p.setStyleSheet("background: #10b981; color: #ffffff; border-radius: 4px; font-weight: bold; padding: 2px 6px;")
                    btn_p.clicked.connect(lambda checked, s=slot: self.quick_log_slot_attendance(s, "Present"))
                    c_lay.addWidget(btn_p)

                    btn_a = QPushButton("✖", chip)
                    btn_a.setToolTip(f"Mark Absent in {slot['subject']}")
                    btn_a.setStyleSheet("background: #f43f5e; color: #ffffff; border-radius: 4px; font-weight: bold; padding: 2px 6px;")
                    btn_a.clicked.connect(lambda checked, s=slot: self.quick_log_slot_attendance(s, "Absent"))
                    c_lay.addWidget(btn_a)

                    self.tt_today_classes_lay.addWidget(chip)
                self.tt_today_classes_lay.addStretch()

        # 4. Filter and Render Table
        tt = all_tt
        filter_sem = self.tt_sem_filter.currentData() if hasattr(self, 'tt_sem_filter') else 0
        if filter_sem > 0:
            tt = [t for t in tt if t.get('sem', 1) == filter_sem]

        if hasattr(self, 'tt_selected_day') and self.tt_selected_day != "All":
            tt = [t for t in tt if t.get('day', '').lower() == self.tt_selected_day.lower()]

        self.tt_table.setRowCount(len(tt))
        for row, t in enumerate(tt):
            self.tt_table.setItem(row, 0, QTableWidgetItem(f"{t['day']} (Sem {t.get('sem', 1)})"))
            self.tt_table.setItem(row, 1, QTableWidgetItem(f"{t['start']} - {t['end']}"))
            self.tt_table.setItem(row, 2, QTableWidgetItem(t['subject']))
            self.tt_table.setItem(row, 3, QTableWidgetItem(t['location']))
            self.tt_table.setItem(row, 4, QTableWidgetItem(t['instructor']))

            # Conflict indicator
            is_conflict = t['id'] in conflict_ids
            status_item = QTableWidgetItem("⚠️ Overlap" if is_conflict else "🟢 Clear")
            if is_conflict:
                status_item.setForeground(QColor("#f59e0b"))
            else:
                status_item.setForeground(QColor("#10b981"))
            self.tt_table.setItem(row, 5, status_item)

            # Actions: [📋 Mark Att] [Edit] [Delete]
            act_widget = QWidget(self)
            act_lay = QHBoxLayout(act_widget)
            act_lay.setContentsMargins(0, 0, 0, 0)
            act_lay.setSpacing(4)

            btn_att = QPushButton("📋 Mark Att", self)
            btn_att.setStyleSheet("background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #34d399; padding: 3px 8px; border-radius: 4px; font-size: 11px;")
            btn_att.clicked.connect(lambda checked, item=t: self.quick_log_slot_attendance(item, "Present"))
            act_lay.addWidget(btn_att)

            btn_edit = QPushButton("Edit", self)
            btn_edit.clicked.connect(lambda checked, item=t: self.open_timetable_dialog(item))
            act_lay.addWidget(btn_edit)

            btn_del = QPushButton("Delete", self)
            btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda checked, tid=t['id']: self.delete_tt(tid))
            act_lay.addWidget(btn_del)

            self.tt_table.setCellWidget(row, 6, act_widget)

    def quick_log_active_lecture(self, status="Present"):
        if hasattr(self, 'current_active_or_next_slot') and self.current_active_or_next_slot:
            self.quick_log_slot_attendance(self.current_active_or_next_slot, status)
        else:
            QMessageBox.information(self, "No Active Class", "No active or upcoming class to log attendance for right now.")

    def quick_log_slot_attendance(self, slot, status="Present"):
        today_str = date.today().isoformat()
        sub_name = slot.get('subject', '').strip()
        if not sub_name:
            return
        sem = slot.get('sem', 1)

        sub_obj = next((s for s in self.data['subjects'] if s['name'].lower() == sub_name.lower()), None)
        if not sub_obj:
            sub_id = f"sub-{int(datetime.now().timestamp())}"
            sub_obj = {
                'id': sub_id,
                'sem': sem,
                'name': sub_name,
                'code': sub_name[:6].upper(),
                'faculty': slot.get('instructor', 'Faculty'),
                'targetPct': self.profile.get('targetAttendancePct', 85.0),
                'color': '#6366f1'
            }
            db.save_subject(sub_obj)
        else:
            sub_id = sub_obj['id']

        att_id = f"att-{int(datetime.now().timestamp())}"
        db.save_attendance({
            'id': att_id,
            'sem': sem,
            'subjectId': sub_id,
            'subjectName': sub_name,
            'date': today_str,
            'status': status,
            'remarks': f"1-Click Timetable Log ({slot.get('start', '')} - {slot.get('end', '')})"
        })
        self.refresh_all_views()
        self.send_notification("Attendance Recorded 📋", f"{status} logged for {sub_name} on {today_str}")
        QMessageBox.information(self, "Attendance Logged", f"Logged {status} for '{sub_name}' on {today_str}!")

    def load_sample_schedule(self):
        reply = QMessageBox.question(
            self, "Load Sample Schedule",
            "Would you like to populate standard NMIMS BBA IB Semester 1 lecture slots into your timetable?\n"
            "(Existing custom slots will be preserved)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            sample_slots = [
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM", "subject": "International Business", "location": "Room 302", "instructor": "Prof. Sharma", "sem": 1},
                {"day": "Monday", "start": "11:00 AM", "end": "12:30 PM", "subject": "Financial Accounting", "location": "Room 304", "instructor": "Prof. Mehta", "sem": 1},
                {"day": "Tuesday", "start": "09:30 AM", "end": "11:00 AM", "subject": "Business Economics", "location": "Room 201", "instructor": "Dr. Verma", "sem": 1},
                {"day": "Tuesday", "start": "11:30 AM", "end": "01:00 PM", "subject": "Business Statistics", "location": "Lab 2", "instructor": "Prof. Gupta", "sem": 1},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM", "subject": "International Business", "location": "Room 302", "instructor": "Prof. Sharma", "sem": 1},
                {"day": "Wednesday", "start": "11:00 AM", "end": "12:30 PM", "subject": "Financial Accounting", "location": "Room 304", "instructor": "Prof. Mehta", "sem": 1},
                {"day": "Thursday", "start": "09:30 AM", "end": "11:00 AM", "subject": "Business Economics", "location": "Room 201", "instructor": "Dr. Verma", "sem": 1},
                {"day": "Thursday", "start": "11:30 AM", "end": "01:00 PM", "subject": "Business Statistics", "location": "Lab 2", "instructor": "Prof. Gupta", "sem": 1},
                {"day": "Friday", "start": "10:00 AM", "end": "12:00 PM", "subject": "Corporate Communication", "location": "Auditorium 1", "instructor": "Prof. Roy", "sem": 1},
            ]
            import time
            for idx, s in enumerate(sample_slots):
                s['id'] = f"tt-sample-{int(time.time())}-{idx}"
                db.save_timetable(s)
            self.refresh_all_views()
            QMessageBox.information(self, "Sample Schedule Loaded", "Loaded 9 standard lecture slots into your Timetable!")


    def delete_tt(self, tid):
        if QMessageBox.question(self, "Confirm Delete", "Delete slot?") == QMessageBox.StandardButton.Yes:
            db.delete_timetable(tid)
            self.refresh_all_views()

    def refresh_memories_grid(self):
        self.mem_list.clear()
        for m in self.data['memories']:
            item = QListWidgetItem(f"{m['title']}\n({m['date']})")
            item.setData(Qt.ItemDataRole.UserRole, m)
            if m['src'].startswith('data:image'):
                try:
                    header, encoded = m['src'].split(",", 1)
                    data = base64.b64decode(encoded)
                    img = QImage()
                    img.loadFromData(data)
                    item.setIcon(QIcon(QPixmap.fromImage(img)))
                except Exception:
                    pass
            elif os.path.exists(m['src']):
                item.setIcon(QIcon(m['src']))
            self.mem_list.addItem(item)

    def view_memory_dialog(self, item):
        m = item.data(Qt.ItemDataRole.UserRole)
        if not m:
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Campus Memory: {m.get('title')}")
        dlg.setFixedSize(620, 520)
        lay = QVBoxLayout(dlg)

        img_lbl = QLabel(dlg)
        img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if m['src'].startswith('data:image'):
            try:
                header, encoded = m['src'].split(",", 1)
                data = base64.b64decode(encoded)
                pix = QPixmap()
                pix.loadFromData(data)
                img_lbl.setPixmap(pix.scaled(580, 420, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except Exception:
                img_lbl.setText("Unable to render image preview")
        elif os.path.exists(m['src']):
            pix = QPixmap(m['src'])
            img_lbl.setPixmap(pix.scaled(580, 420, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            img_lbl.setText("Image file not found")
        lay.addWidget(img_lbl)

        meta_lay = QHBoxLayout()
        meta_lay.addWidget(QLabel(f"<b>{m.get('title')}</b> • {m.get('date')} ({m.get('tag', 'Campus')})", dlg))
        meta_lay.addStretch()

        btn_del = QPushButton("Delete Memory 🗑️", dlg)
        btn_del.setProperty("class", "danger")
        def delete_this():
            if QMessageBox.question(dlg, "Delete Memory", f"Delete memory '{m.get('title')}'?") == QMessageBox.StandardButton.Yes:
                db.delete_memory(m['id'])
                dlg.accept()
                self.refresh_all_views()
        btn_del.clicked.connect(delete_this)
        meta_lay.addWidget(btn_del)
        lay.addLayout(meta_lay)

        dlg.exec()

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

        sem_combo = QComboBox(dlg)
        for i in range(1, 11):
            sem_combo.addItem(f"Semester {i}", i)
        if edit_item:
            s_idx = sem_combo.findData(edit_item.get('sem', 1))
            if s_idx != -1: sem_combo.setCurrentIndex(s_idx)

        day_combo = QComboBox(dlg); day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        if edit_item:
            d_idx = day_combo.findText(edit_item['day'])
            if d_idx != -1: day_combo.setCurrentIndex(d_idx)

        sub_in = QLineEdit(dlg); sub_in.setText(edit_item['subject'] if edit_item else "")
        start_in = QLineEdit(dlg); start_in.setText(edit_item['start'] if edit_item else "09:00 AM")
        end_in = QLineEdit(dlg); end_in.setText(edit_item['end'] if edit_item else "10:30 AM")
        loc_in = QLineEdit(dlg); loc_in.setText(edit_item['location'] if edit_item else "")
        inst_in = QLineEdit(dlg); inst_in.setText(edit_item['instructor'] if edit_item else "")

        lay.addWidget(QLabel("Semester:", dlg)); lay.addWidget(sem_combo)
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
                    'sem': sem_combo.currentData() or 1,
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

        btn_copy_aud = QPushButton("🔊 Read Copyright Notice Aloud", dlg); btn_copy_aud.setStyleSheet("background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981;")
        btn_copy_aud.clicked.connect(self.open_copyright_dialog)
        lay.addWidget(btn_copy_aud)

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
                    for ge in parsed.get('groupExpenses', []): db.save_group_expense(ge)
                    for fc in parsed.get('flashcards', []): db.save_flashcard(fc)
                    for sn in parsed.get('subjectNotes', []): db.save_subject_note(sn)
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
