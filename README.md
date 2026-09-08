# STUNT — Student Tracker for Unified Navigation & Tasks 🚀

**STUNT** is a high-performance, 100% native Python desktop application designed for college and university students to track their entire academic degree journey (up to 5 years / 10 semesters), academic CGPA/SGPA, attendance bunk safety, financial budgeting, targeted savings goals, exam syllabus revisions, interactive flashcards, timetable scheduling, and campus memories.

![STUNT Banner](assets/RedandBlackGlitchcoreStuntLogo.png)

---

## 🌟 Key Features

### 🎓 Academic & CGPA Intelligence
* **CGPA / SGPA Intelligence & Target Predictor**:
  * Track credit hours and letter grades (`O=10`, `A+=9`, `A=8`, etc.) per semester.
  * Calculates SGPA per semester and overall cumulative CGPA.
  * Predicts the exact average SGPA required in remaining semesters to achieve your target graduation CGPA.
  * Interactive Matplotlib SGPA trend line graph.
  * **What-If CGPA Simulator**: Model expected SGPA in future semesters to forecast graduating CGPA accurately.

### 🏛️ Attendance & Bunk Safety Calculator
* **Custom Minimum Thresholds**: Set attendance targets (e.g. 75%, 80%, 85%).
* **Real-Time Bunk Safety Engine**:
  * 🟢 *SAFE: Can bunk X classes without dropping below threshold.*
  * 🔴 *CRITICAL: Must attend next Y lectures consecutively to recover!*
* **Editable Subject Menu**: Quick write-in or select subject dropdown for frictionless class logging.

### 📈 Dynamic Productivity & Activity Heatmap
* **Live 7-Day Activity Stream**: Dynamically monitors tasks completed, attendance logs, syllabus unit revisions, finances entered, and campus memories.
* **Color-Coded Heatmap**: Visual intensity highlights daily productivity streaks directly on the dashboard overview.

### 🏆 Gamified Student Badges & XP Progression
* **Live Achievement Engine**: Unlocks dynamic badges based on real database records:
  * 🥇 *Dean's List*: CGPA ≥ 9.0
  * 🟢 *Bunk Master*: Maintained safe attendance across all courses
  * 💰 *Savings Champion*: Fully funded at least 1 targeted savings goal
  * 🎯 *Task Achiever*: Completed 3+ academic tasks
  * 📚 *Syllabus Scholar*: Mastered 3+ syllabus units
  * ⏱️ *Focus Beast*: Logged Pomodoro focus sessions
* **Student XP & Level**: Earn XP points for every task completed, class attended, and focus block finished (e.g. *Level 3 Scholar • 450 XP*).

### ⏱️ Multi-Mode Pomodoro Focus Timer
* **3 Productivity Modes**:
  * **Focus Session**: 25 minutes
  * **Short Break**: 5 minutes
  * **Long Break**: 15 minutes
* **Session Counter & Automatic Progression**: Tracks completed focus sessions, awards bonus XP, and triggers smooth desktop break notifications.

### 🎴 Interactive Flashcard Revision Studio
* **Active Recall Study Tool**: Flip flashcards between Question and Answer mode.
* **Full Management**: Add new questions for any subject, toggle *Mastered* vs. *Learning* status, delete cards, or shuffle revision order.

### 📝 PYQ & Notes Resource Vault
* **Organized Course Material**: Attach PDFs, previous year question papers (PYQs), cheatsheets, and lecture notes categorized by subject and type.
* **1-Click Local Opener**: Instantly opens documents in your default viewer.

### 💰 Finance Ledger & Targeted Savings Goals
* **Income & Expense Tracking**: Categorized transactions with Matplotlib category donut charts and income vs. expense bar graphs.
* **Budget Limit Alerts**: Automated toast alerts when monthly expenses exceed your spending cap.
* **Targeted Wishlist & Savings Cards**: Save towards laptops, phones, trips, or certifications with progress bars and celebration popups upon reaching 100%.
* **Roommate Group Expense Splitter**: Split shared bills, Wi-Fi costs, and meals evenly with friends.

### 🤖 J.A.R.V.I.S. College Wingman & Academic Co-Pilot (`Ctrl+J`)
* **Warm, Loyal "Proper Friend" AI**: Talks like your trusted college buddy — keeping you motivated, tracking lecture times, and calling out risky bunks with witty advice.
* **Time-Aware Intelligence**: Checks the current time of day, active class, and minutes until your next lecture.
* **Natural Language Attendance Logging**: Just type or say *"Attended Finance today"* or *"Present in Business Economics"* — JARVIS logs the record immediately into SQLite, recalculates your attendance percentage, and updates the entire dashboard in real time!
* **Bunk Safeguard Engine**: Ask *"Can I bunk Economics?"* — JARVIS computes your exact safe bunk cushion or tells you how many consecutive lectures you need to attend to avoid debarment.
* **Speech Synthesis**: Real-time voice reading powered by Windows SAPI with 1-click toggle (`🔊 Voice: ON` / `🔇 Mute`).
* **Two-Way JARVIS Mark-XL Integration**: Connects directly with the central JARVIS Mark-XL system (`actions/stunt_bridge.py`) for voice/chat commands anywhere on your system.

### 📅 Upgraded Timetable & Schedule Intelligence
* **"Today's Live Schedule" Hero Card**: Dynamic card highlighting today's classes, current active lecture, or countdown to your next class.
* **1-Click Attendance from Timetable**: Mark `✅ Present`, `❌ Absent / Bunked`, or `⚠️ Cancelled` right from the live hero card or any table row without leaving your timetable!
* **Visual Day-by-Day Selector**: Filter lectures by day (`Monday` through `Saturday`) with real-time class counters on each tab.
* **Automatic Collision & Overlap Detector**: Instantly scans and warns you if two classes on the same day in the same semester have overlapping times (`⚠️ Schedule Conflicts Detected`).
* **1-Click Sample College Schedule**: Populate standard college degree schedules with a single click to get started immediately.
* **Smart Anti-Spam Alarms**: Background system tray notifications 15 minutes before scheduled lectures, deduplicated so you only get notified once per class per day.
* **.ics Calendar Export**: 1-click export to standard iCalendar format compatible with Google Calendar, Outlook, and Apple Calendar.

### 🖼️ Campus Memories Vault
* **High-Res Photo Gallery**: Store cherished campus photos and event memories in an offline vault.
* **Double-Click Previewer**: View memories in high resolution and manage photo records.

### 📄 Executive HTML/PDF Transcript Exporter
* **1-Click Academic & Financial Transcript**: Generates a clean, modern report card summarizing degree journey, CGPA breakdown, attendance metrics, savings goals, and tasks.
* **Print-Optimized**: Built-in `@media print` CSS ensures clean printing to PDF directly from any web browser.

### 🎨 Custom UI Themes
* Switch seamlessly between 4 built-in executive dark themes:
  * **Glitchcore Dark** (`#0a0b10`)
  * **Midnight Cyberpunk** (`#0d0914`)
  * **Emerald Tech** (`#06140e`)
  * **Solar Amber** (`#140e06`)

---

## ⌨️ Power-User Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl+1` | Overview Dashboard |
| `Ctrl+2` | Academic CGPA Ledger |
| `Ctrl+3` | Syllabus & Revision Matrix |
| `Ctrl+4` | Tasks & Pomodoro Focus |
| `Ctrl+5` | Attendance & Bunk Calculator |
| `Ctrl+6` | Finance & Savings Goals |
| `Ctrl+7` | Weekly Timetable |
| `Ctrl+8` | Campus Memories Vault |
| `Ctrl+9` | Academic Milestones |
| `Ctrl+T` | Quick Create Task / Goal |
| `Ctrl+A` | Quick Log Attendance |
| `Ctrl+J` | Open J.A.R.V.I.S. College Wingman |

---

## 🛠️ Technology Stack

* **GUI Framework**: PyQt6 (Qt 6)
* **Database**: SQLite3 (Local offline vault)
* **Data Visualization**: Matplotlib QtAgg (`FigureCanvasQTAgg`)
* **Audio / Speech**: Windows SAPI (`win32com.client`)
* **Multimedia**: PyQt6.QtMultimedia (`QMediaPlayer`, `QVideoWidget`)
* **System Tray**: PyQt6.QtWidgets (`QSystemTrayIcon`)
* **Build / Distribution**: PyInstaller

---

## 🚀 Quick Start & Installation

### Option 1: Run via Launcher
Double-click `STUNT_Launcher.bat` in the project folder or `STUNT.bat` on your Desktop!

### Option 2: Run from Source
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bhatnagarakul5-debug/S.T.U.N.T-Student-Tracker-for-Unified-Navigation-Tasks.git
   cd S.T.U.N.T-Student-Tracker-for-Unified-Navigation-Tasks
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Application**:
   ```bash
   python main.py
   ```

---

## 📜 License
Licensed under the [MIT License](LICENSE).  
Copyright © 2026 Akul. All Rights Reserved.
