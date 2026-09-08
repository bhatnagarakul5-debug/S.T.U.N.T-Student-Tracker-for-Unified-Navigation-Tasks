"""
STUNT: Student Tracker for Unified Navigation & Tasks
SQLite Local Database Manager (db.py)
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'stunt_database.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 0. Profile & Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT,
            college TEXT,
            course TEXT,
            batch TEXT,
            startDate TEXT,
            endDate TEXT,
            totalSemesters INTEGER,
            targetAttendancePct REAL,
            monthlyBudgetCap REAL,
            targetCgpa REAL,
            themeName TEXT,
            avatar TEXT
        )
    ''')

    # Migration / ensure columns
    cursor.execute('PRAGMA table_info(profile)')
    cols = [row[1] for row in cursor.fetchall()]
    if 'themeName' not in cols:
        cursor.execute("ALTER TABLE profile ADD COLUMN themeName TEXT DEFAULT 'Glitchcore Dark'")

    # Default profile if empty
    cursor.execute('SELECT COUNT(*) FROM profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (id, name, college, course, batch, startDate, endDate, totalSemesters, targetAttendancePct, monthlyBudgetCap, targetCgpa, themeName, avatar)
            VALUES (1, 'Akul', 'College / University', 'B.Tech Computer Science', '2026 – 2031', '2026-08-01', '2031-07-31', 10, 75.0, 5000.0, 8.5, 'Glitchcore Dark', 'assets/RedandBlackGlitchcoreStuntLogo.png')
        ''')

    # 1. Syllabus Topics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS syllabus (
            id TEXT PRIMARY KEY,
            subjectId TEXT,
            subjectName TEXT,
            unitName TEXT,
            status TEXT,
            notes TEXT
        )
    ''')

    # 2. Savings Goals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS savings_goals (
            id TEXT PRIMARY KEY,
            title TEXT,
            targetAmount REAL,
            currentSaved REAL,
            targetDate TEXT,
            category TEXT,
            notes TEXT
        )
    ''')

    # 3. Grades & SGPA Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id TEXT PRIMARY KEY,
            sem INTEGER,
            subjectCode TEXT,
            subjectName TEXT,
            credits INTEGER,
            gradePoints INTEGER
        )
    ''')

    # 4. Tasks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT,
            category TEXT,
            dueDate TEXT,
            dueTime TEXT,
            priority TEXT,
            status TEXT,
            desc TEXT
        )
    ''')

    # 5. Subjects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY,
            sem INTEGER,
            name TEXT,
            code TEXT,
            faculty TEXT,
            targetPct REAL,
            color TEXT
        )
    ''')

    # 6. Attendance Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id TEXT PRIMARY KEY,
            sem INTEGER,
            subjectId TEXT,
            subjectName TEXT,
            date TEXT,
            status TEXT,
            remarks TEXT
        )
    ''')

    # 7. Finances Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id TEXT PRIMARY KEY,
            type TEXT,
            category TEXT,
            amount REAL,
            desc TEXT,
            date TEXT
        )
    ''')

    # 8. Timetable Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id TEXT PRIMARY KEY,
            sem INTEGER,
            day TEXT,
            subject TEXT,
            start TEXT,
            end TEXT,
            location TEXT,
            instructor TEXT
        )
    ''')

    # 9. Memories Vault Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            tag TEXT,
            src TEXT
        )
    ''')

    # 10. Milestones Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id TEXT PRIMARY KEY,
            category TEXT,
            title TEXT,
            date TEXT,
            desc TEXT
        )
    ''')

    # 11. Group Expenses Table (Splitwise style)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_expenses (
            id TEXT PRIMARY KEY,
            title TEXT,
            totalAmount REAL,
            paidBy TEXT,
            peopleCount INTEGER,
            sharePerPerson REAL,
            date TEXT,
            notes TEXT
        )
    ''')

    # 12. Flashcards Table (Revision Cards)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id TEXT PRIMARY KEY,
            subjectName TEXT,
            question TEXT,
            answer TEXT,
            status TEXT
        )
    ''')

    # 13. Subject PYQ & PDF Notes Vault Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_notes (
            id TEXT PRIMARY KEY,
            subjectName TEXT,
            title TEXT,
            fileType TEXT,
            filePath TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_profile():
    conn = get_connection()
    row = conn.execute('SELECT * FROM profile WHERE id = 1').fetchone()
    conn.close()
    if row: return dict(row)
    return {
        'name': 'Akul',
        'college': 'College / University',
        'course': 'Course / Degree',
        'batch': '2026 – 2031',
        'startDate': '2026-08-01',
        'endDate': '2031-07-31',
        'totalSemesters': 10,
        'targetAttendancePct': 75.0,
        'monthlyBudgetCap': 5000.0,
        'targetCgpa': 8.5,
        'themeName': 'Glitchcore Dark',
        'avatar': 'assets/RedandBlackGlitchcoreStuntLogo.png'
    }

def save_profile(prof_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO profile (id, name, college, course, batch, startDate, endDate, totalSemesters, targetAttendancePct, monthlyBudgetCap, targetCgpa, themeName, avatar)
        VALUES (1, :name, :college, :course, :batch, :startDate, :endDate, :totalSemesters, :targetAttendancePct, :monthlyBudgetCap, :targetCgpa, :themeName, :avatar)
    ''', prof_dict)
    conn.commit()
    conn.close()

def get_all_data():
    conn = get_connection()
    cursor = conn.cursor()

    profile = get_profile()
    syllabus = [dict(row) for row in cursor.execute('SELECT * FROM syllabus').fetchall()]
    savings_goals = [dict(row) for row in cursor.execute('SELECT * FROM savings_goals ORDER BY targetDate ASC').fetchall()]
    grades = [dict(row) for row in cursor.execute('SELECT * FROM grades ORDER BY sem ASC').fetchall()]
    tasks = [dict(row) for row in cursor.execute('SELECT * FROM tasks ORDER BY dueDate ASC').fetchall()]
    subjects = [dict(row) for row in cursor.execute('SELECT * FROM subjects').fetchall()]
    attendance_logs = [dict(row) for row in cursor.execute('SELECT * FROM attendance_logs ORDER BY date DESC').fetchall()]
    finances = [dict(row) for row in cursor.execute('SELECT * FROM finances ORDER BY date DESC').fetchall()]
    timetable = [dict(row) for row in cursor.execute('SELECT * FROM timetable').fetchall()]
    memories = [dict(row) for row in cursor.execute('SELECT * FROM memories ORDER BY date DESC').fetchall()]
    milestones = [dict(row) for row in cursor.execute('SELECT * FROM milestones ORDER BY date ASC').fetchall()]
    group_expenses = [dict(row) for row in cursor.execute('SELECT * FROM group_expenses ORDER BY date DESC').fetchall()]
    flashcards = [dict(row) for row in cursor.execute('SELECT * FROM flashcards').fetchall()]
    subject_notes = [dict(row) for row in cursor.execute('SELECT * FROM subject_notes ORDER BY date DESC').fetchall()]

    conn.close()
    return {
        'profile': profile,
        'syllabus': syllabus,
        'savingsGoals': savings_goals,
        'grades': grades,
        'tasks': tasks,
        'subjects': subjects,
        'attendanceLogs': attendance_logs,
        'finances': finances,
        'timetable': timetable,
        'memories': memories,
        'milestones': milestones,
        'groupExpenses': group_expenses,
        'flashcards': flashcards,
        'subjectNotes': subject_notes
    }

def save_syllabus(syl_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO syllabus (id, subjectId, subjectName, unitName, status, notes)
        VALUES (:id, :subjectId, :subjectName, :unitName, :status, :notes)
    ''', syl_dict)
    conn.commit()
    conn.close()

def delete_syllabus(syl_id):
    conn = get_connection()
    conn.execute('DELETE FROM syllabus WHERE id = ?', (syl_id,))
    conn.commit()
    conn.close()

def save_savings_goal(sg_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO savings_goals (id, title, targetAmount, currentSaved, targetDate, category, notes)
        VALUES (:id, :title, :targetAmount, :currentSaved, :targetDate, :category, :notes)
    ''', sg_dict)
    conn.commit()
    conn.close()

def delete_savings_goal(sg_id):
    conn = get_connection()
    conn.execute('DELETE FROM savings_goals WHERE id = ?', (sg_id,))
    conn.commit()
    conn.close()

def save_grade(grade_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO grades (id, sem, subjectCode, subjectName, credits, gradePoints)
        VALUES (:id, :sem, :subjectCode, :subjectName, :credits, :gradePoints)
    ''', grade_dict)
    conn.commit()
    conn.close()

def delete_grade(grade_id):
    conn = get_connection()
    conn.execute('DELETE FROM grades WHERE id = ?', (grade_id,))
    conn.commit()
    conn.close()

def save_task(task_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO tasks (id, title, category, dueDate, dueTime, priority, status, desc)
        VALUES (:id, :title, :category, :dueDate, :dueTime, :priority, :status, :desc)
    ''', task_dict)
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def save_subject(sub_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO subjects (id, sem, name, code, faculty, targetPct, color)
        VALUES (:id, :sem, :name, :code, :faculty, :targetPct, :color)
    ''', sub_dict)
    conn.commit()
    conn.close()

def delete_subject(sub_id):
    conn = get_connection()
    conn.execute('DELETE FROM subjects WHERE id = ?', (sub_id,))
    conn.commit()
    conn.close()

def save_attendance(att_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO attendance_logs (id, sem, subjectId, subjectName, date, status, remarks)
        VALUES (:id, :sem, :subjectId, :subjectName, :date, :status, :remarks)
    ''', att_dict)
    conn.commit()
    conn.close()

def delete_attendance(att_id):
    conn = get_connection()
    conn.execute('DELETE FROM attendance_logs WHERE id = ?', (att_id,))
    conn.commit()
    conn.close()

def get_attendance_logs(subject_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if subject_id:
        cursor.execute("SELECT * FROM attendance_logs WHERE subjectId = ?", (subject_id,))
    else:
        cursor.execute("SELECT * FROM attendance_logs ORDER BY date DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_timetable(day=None):
    conn = get_connection()
    cursor = conn.cursor()
    if day:
        cursor.execute("SELECT * FROM timetable WHERE LOWER(day) = LOWER(?) ORDER BY start", (day,))
    else:
        cursor.execute("SELECT * FROM timetable ORDER BY sem, day, start")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def save_finance(fin_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO finances (id, type, category, amount, desc, date)
        VALUES (:id, :type, :category, :amount, :desc, :date)
    ''', fin_dict)
    conn.commit()
    conn.close()

def delete_finance(fin_id):
    conn = get_connection()
    conn.execute('DELETE FROM finances WHERE id = ?', (fin_id,))
    conn.commit()
    conn.close()

def save_timetable(tt_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO timetable (id, sem, day, subject, start, end, location, instructor)
        VALUES (:id, :sem, :day, :subject, :start, :end, :location, :instructor)
    ''', tt_dict)
    conn.commit()
    conn.close()

def delete_timetable(tt_id):
    conn = get_connection()
    conn.execute('DELETE FROM timetable WHERE id = ?', (tt_id,))
    conn.commit()
    conn.close()

def save_memory(mem_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO memories (id, title, date, tag, src)
        VALUES (:id, :title, :date, :tag, :src)
    ''', mem_dict)
    conn.commit()
    conn.close()

def delete_memory(mem_id):
    conn = get_connection()
    conn.execute('DELETE FROM memories WHERE id = ?', (mem_id,))
    conn.commit()
    conn.close()

def save_milestone(ms_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO milestones (id, category, title, date, desc)
        VALUES (:id, :category, :title, :date, :desc)
    ''', ms_dict)
    conn.commit()
    conn.close()

def delete_milestone(ms_id):
    conn = get_connection()
    conn.execute('DELETE FROM milestones WHERE id = ?', (ms_id,))
    conn.commit()
    conn.close()

# New Offline Helpers: Group Expenses, Flashcards, Subject Notes
def save_group_expense(ge_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO group_expenses (id, title, totalAmount, paidBy, peopleCount, sharePerPerson, date, notes)
        VALUES (:id, :title, :totalAmount, :paidBy, :peopleCount, :sharePerPerson, :date, :notes)
    ''', ge_dict)
    conn.commit()
    conn.close()

def delete_group_expense(ge_id):
    conn = get_connection()
    conn.execute('DELETE FROM group_expenses WHERE id = ?', (ge_id,))
    conn.commit()
    conn.close()

def save_flashcard(fc_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO flashcards (id, subjectName, question, answer, status)
        VALUES (:id, :subjectName, :question, :answer, :status)
    ''', fc_dict)
    conn.commit()
    conn.close()

def delete_flashcard(fc_id):
    conn = get_connection()
    conn.execute('DELETE FROM flashcards WHERE id = ?', (fc_id,))
    conn.commit()
    conn.close()

def save_subject_note(sn_dict):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO subject_notes (id, subjectName, title, fileType, filePath, date)
        VALUES (:id, :subjectName, :title, :fileType, :filePath, :date)
    ''', sn_dict)
    conn.commit()
    conn.close()

def delete_subject_note(sn_id):
    conn = get_connection()
    conn.execute('DELETE FROM subject_notes WHERE id = ?', (sn_id,))
    conn.commit()
    conn.close()

def clear_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM syllabus')
    cursor.execute('DELETE FROM savings_goals')
    cursor.execute('DELETE FROM grades')
    cursor.execute('DELETE FROM tasks')
    cursor.execute('DELETE FROM subjects')
    cursor.execute('DELETE FROM attendance_logs')
    cursor.execute('DELETE FROM finances')
    cursor.execute('DELETE FROM timetable')
    cursor.execute('DELETE FROM memories')
    cursor.execute('DELETE FROM milestones')
    cursor.execute('DELETE FROM group_expenses')
    cursor.execute('DELETE FROM flashcards')
    cursor.execute('DELETE FROM subject_notes')
    conn.commit()
    conn.close()

def load_sample_data():
    clear_all()
    sample = {
        'syllabus': [
            {'id': 'syl-1', 'subjectId': 'sub-1', 'subjectName': 'Computer Programming & C', 'unitName': 'Unit 1: Pointers & Dynamic Allocation', 'status': 'Completed', 'notes': 'Pointers, malloc, free'},
            {'id': 'syl-2', 'subjectId': 'sub-1', 'subjectName': 'Computer Programming & C', 'unitName': 'Unit 2: Structs & File I/O', 'status': 'In Progress', 'notes': 'Structures, unions, file pointers'},
            {'id': 'syl-3', 'subjectId': 'sub-2', 'subjectName': 'Engineering Mathematics I', 'unitName': 'Unit 1: Differential Calculus', 'status': 'Completed', 'notes': 'Limits & Continuity'}
        ],
        'savingsGoals': [
            {'id': 'sg-1', 'title': 'New Gaming Laptop', 'targetAmount': 60000.0, 'currentSaved': 22000.0, 'targetDate': '2026-12-31', 'category': 'Electronics', 'notes': 'Saving for ASUS ROG / Legion'},
            {'id': 'sg-2', 'title': 'Mechanical Keyboard & Desk Setup', 'targetAmount': 5000.0, 'currentSaved': 3500.0, 'targetDate': '2026-09-15', 'category': 'Tech Accessory', 'notes': 'Keychron wireless keyboard'}
        ],
        'grades': [
            {'id': 'gr-1', 'sem': 1, 'subjectCode': 'CS101', 'subjectName': 'Computer Programming & C', 'credits': 4, 'gradePoints': 10},
            {'id': 'gr-2', 'sem': 1, 'subjectCode': 'MA101', 'subjectName': 'Engineering Mathematics I', 'credits': 4, 'gradePoints': 9},
            {'id': 'gr-3', 'sem': 1, 'subjectCode': 'PH101', 'subjectName': 'Engineering Physics & Lab', 'credits': 3, 'gradePoints': 8}
        ],
        'tasks': [
            {'id': 'task-1', 'title': 'Complete C Programming Assignment 1', 'category': 'Assignment', 'dueDate': '2026-08-05', 'dueTime': '11:59 PM', 'priority': 'High', 'status': 'Pending', 'desc': 'Solve pointers and struct exercises.'},
            {'id': 'task-2', 'title': 'Calculus Mid-Term Exam Prep', 'category': 'Exam Prep', 'dueDate': '2026-08-10', 'dueTime': '10:00 AM', 'priority': 'High', 'status': 'In Progress', 'desc': 'Review differentiation chapters 1-4.'}
        ],
        'subjects': [
            {'id': 'sub-1', 'sem': 1, 'name': 'Computer Programming & C', 'code': 'CS101', 'faculty': 'Dr. R. K. Vance', 'targetPct': 75.0, 'color': '#6366f1'},
            {'id': 'sub-2', 'sem': 1, 'name': 'Engineering Mathematics I', 'code': 'MA101', 'faculty': 'Prof. S. N. Bose', 'targetPct': 75.0, 'color': '#0ea5e9'},
            {'id': 'sub-3', 'sem': 1, 'name': 'Engineering Physics & Lab', 'code': 'PH101', 'faculty': 'Dr. M. Curie', 'targetPct': 75.0, 'color': '#f43f5e'},
            {'id': 'sub-4', 'sem': 1, 'name': 'Basic Electrical Engg', 'code': 'EE101', 'faculty': 'Prof. N. Tesla', 'targetPct': 75.0, 'color': '#f59e0b'}
        ],
        'attendanceLogs': [
            {'id': 'att-1', 'sem': 1, 'subjectId': 'sub-1', 'subjectName': 'Computer Programming & C', 'date': '2026-08-01', 'status': 'Present', 'remarks': 'Orientation & C Lab'},
            {'id': 'att-2', 'sem': 1, 'subjectId': 'sub-2', 'subjectName': 'Engineering Mathematics I', 'date': '2026-08-01', 'status': 'Present', 'remarks': 'Calculus Intro'}
        ],
        'finances': [
            {'id': 'fin-1', 'type': 'Income', 'category': 'Monthly Allowance', 'amount': 8000, 'desc': 'Monthly Pocket Money Received', 'date': '2026-08-01'},
            {'id': 'fin-2', 'type': 'Expense', 'category': 'Food & Dining', 'amount': 350, 'desc': 'Canteen Welcome Treat', 'date': '2026-08-01'}
        ],
        'timetable': [
            {'id': 'tt-1', 'sem': 1, 'day': 'Monday', 'subject': 'Computer Programming & C', 'start': '09:00 AM', 'end': '10:30 AM', 'location': 'CS Lab 201', 'instructor': 'Dr. R. K. Vance'},
            {'id': 'tt-2', 'sem': 1, 'day': 'Monday', 'subject': 'Engineering Mathematics I', 'start': '10:45 AM', 'end': '12:15 PM', 'location': 'Lecture Hall 104', 'instructor': 'Prof. S. N. Bose'}
        ],
        'memories': [
            {'id': 'mem-1', 'title': 'First Day at College Campus', 'date': '2026-08-01', 'tag': 'Campus', 'src': 'assets/RedandBlackGlitchcoreStuntLogo.png'}
        ],
        'milestones': [
            {'id': 'ms-1', 'category': 'Fest', 'title': 'College Orientation & Semester 1 Kickoff', 'date': '2026-08-01', 'desc': 'Started 5-Year College Journey (2026-2031) under STUNT Platform!'}
        ],
        'flashcards': [
            {'id': 'fc-1', 'subjectName': 'Computer Programming & C', 'question': 'What is the difference between malloc() and calloc()?', 'answer': 'malloc() allocates uninitialized memory block, while calloc() allocates and initializes memory to zero.', 'status': 'Mastered'}
        ],
        'groupExpenses': [
            {'id': 'ge-1', 'title': 'Hostel Room Wi-Fi Bill', 'totalAmount': 1200.0, 'paidBy': 'Akul', 'peopleCount': 3, 'sharePerPerson': 400.0, 'date': '2026-08-01', 'notes': 'Shared between Akul, Rohan, and Alex'}
        ],
        'subjectNotes': [
            {'id': 'sn-1', 'subjectName': 'Computer Programming & C', 'title': 'C Programming Mid-Term PYQs (2024-2025)', 'fileType': 'PDF', 'filePath': 'assets/RedandBlackGlitchcoreStuntLogo.png', 'date': '2026-08-01'}
        ]
    }
    for syl in sample['syllabus']: save_syllabus(syl)
    for sg in sample['savingsGoals']: save_savings_goal(sg)
    for g in sample['grades']: save_grade(g)
    for t in sample['tasks']: save_task(t)
    for sub in sample['subjects']: save_subject(sub)
    for att in sample['attendanceLogs']: save_attendance(att)
    for fin in sample['finances']: save_finance(fin)
    for tt in sample['timetable']: save_timetable(tt)
    for mem in sample['memories']: save_memory(mem)
    for ms in sample['milestones']: save_milestone(ms)
    for ge in sample['groupExpenses']: save_group_expense(ge)
    for fc in sample['flashcards']: save_flashcard(fc)
    for sn in sample['subjectNotes']: save_subject_note(sn)

if __name__ == '__main__':
    init_db()
    print('SQLite database initialized at', DB_PATH)
