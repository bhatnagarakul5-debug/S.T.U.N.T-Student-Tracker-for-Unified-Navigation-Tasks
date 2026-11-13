# STUNT & J.A.R.V.I.S. Mark 58 — Privacy Policy & Data Sovereignty Charter

**Effective Date:** October 6, 2026  
**Version:** 3.0 (Comprehensive Sovereign Edition)  
**Lead Architect & Developer:** Akul Bhatnagar (NMIMS Mumbai, BBA International Business)  
**Target Systems:** STUNT Desktop Workstation (PyQt6), STUNT Mobile Companion, Web Showcase, and J.A.R.V.I.S. Mark 58 (Apex Core)  
**Legal Classification:** Sovereign Local-First Software • Zero-Telemetry Academic Architecture  

---

## 1. Executive Charter & Core Philosophy

Commercial university portals, campus utilities, and student management applications frequently commodify user attention, harvest location traces, bundle invasive analytics beacons, and trade student behavioral profiles with third-party brokers. 

**STUNT (Student Tracker for Unified Navigation & Tasks)** was conceived and engineered under an uncompromising opposing doctrine: **Absolute Data Sovereignty**.

STUNT is built on the tenet that your academic trajectory, grade point averages, class absences, financial splits, and personal voice assistant queries are strictly private, sacrosanct records that belong exclusively to you on your physical machine.

### The Six Immutable Sovereignty Tenets
1. **Zero Third-Party Telemetry:** STUNT contains zero trackers, zero tracking pixels, zero analytics SDKs (no Google Analytics, Mixpanel, Firebase, or Datadog), and zero advertising frameworks. The application never transmits heartbeat pings or usage telemetries.
2. **100% On-Device Storage by Default:** All operational databases, schemas, logs, and profile records live exclusively in an ACID-compliant local SQLite engine (`stunt_database.db`) on your physical hard drive.
3. **Localhost Socket Isolation:** All internal Inter-Process Communication (IPC) routines and bridge sockets bind strictly to the local loopback interface (`127.0.0.1` and `::1`). STUNT is invisible and unreachable across public or campus Wi-Fi networks.
4. **Anti-Shoulder Surfer Defense:** Built-in cryptographic and visual redaction protocols (`Ctrl+Shift+P`) instantly obscure sensitive financial figures and academic marks when studying in high-density campus libraries.
5. **No Model Training on Private Records:** Your notes, course syllabi, financial transactions, and assignment drafts are never stored on cloud servers and are never used to train or fine-tune public artificial intelligence models.
6. **Unconditional Right to Portability & Instant Erasure:** You retain complete, unmediated ownership of your records. You may export a human-readable JSON backup at any time or execute a permanent, one-click unrecoverable purge of all local databases.

---

## 2. Information Handled & Boundary Specifications

STUNT operates on the principle of **strict data minimization**. The system processes only the data categories you explicitly enter:

| Data Category | Specific Elements | Storage Location | Network Boundary |
| :--- | :--- | :--- | :--- |
| **Academic Records** | Course codes, subject titles, credit weightages, grade points, SGPA history, and target CGPA formulas. | Local SQLite (`grades` table) | 100% Offline / Never leaves device. |
| **Attendance & Bunks** | Class logs, timestamps, attendance status (`Present` / `Absent`), exact integer safe-bunk ratios. | Local SQLite (`attendance_logs` table) | 100% Offline / Computed locally via deterministic math. |
| **Timetable & Matrix** | Lecture halls, time slots, day allocations, and faculty titles. | Local SQLite (`timetable` table) | 100% Offline / Used for on-device clash detection. |
| **Personal Finances** | Expense items, allowance deposits, categorized budgets, and targeted savings goals. | Local SQLite (`finances`, `savings_goals`) | 100% Offline / No bank credentials or token storage. |
| **Roommate Bill Splits** | Expense amounts, headcount tallies, and per-person calculated shares. | Local Memory / Temporary state | Direct peer-to-peer UPI intent links (`upi://pay`). No financial intermediary. |
| **J.A.R.V.I.S. Mark 58 AI** | Academic queries (viva prep, DuPont formula synthesis, schedule lookups). | Local Loopback Socket (`127.0.0.1:IPC`) | Isolated IPC bridge (`actions/stunt_bridge.py`). No remote persistence. |

---

## 3. Cryptographic & Architectural Defenses

To safeguard student workstations in adversarial or public network environments (such as crowded university cafeterias or unsecured dorm Wi-Fi), STUNT and J.A.R.V.I.S. Mark 58 deploy active defensive layers:

### A. Localhost Loopback Isolation (`127.0.0.1`)
The communication bus linking STUNT to J.A.R.V.I.S. Mark 58 operates over a local IPC channel. Sockets refuse external binding requests and reject any incoming packet originating outside the host machine's loopback interface.

### B. Anti-Shoulder Surfer Protocol (`Ctrl+Shift+P`)
Campus environments expose laptop screens to visual snooping by peers, proctors, or strangers. STUNT features a dedicated hardware-accelerated privacy shroud:
- **Instant Hotkey Activation:** Pressing `Ctrl+Shift+P` toggles the privacy veil across the entire UI.
- **Deep Metric Redaction:** Real-time balances (`₹4,850.00`), SGPA indicators (`9.24`), and specific attendance counts are masked with `••••••` or obscured with frosted blur layers.
- **Visual Glitch Protection:** Status glows transition to a neutral, discrete indicator to prevent observers from guessing performance thresholds based on color cues.

### C. Canonical Path Traversal Defenses
All file handling operations (such as PDF academic report export, memory photo imports, and JSON backup loading) pass through a strict canonical path sanitizer. File paths containing directory traversal attacks (e.g., `../../`) or unauthorized system paths are automatically rejected.

### D. SQLite PRAGMA Integrity Checks
The local database engine enforces internal consistency and prevents corruption through periodic runtime integrity audits (`PRAGMA integrity_check`). Students can manually trigger an endpoint security scan from the Security Center (`Ctrl+P`) at any time.

---

## 4. Statutory & Regulatory Compliance

Although STUNT is non-commercial, open-source student software that collects zero central server data, it is purposefully engineered to comply with and exceed the world's strictest data privacy standards:

### A. Digital Personal Data Protection Act, 2023 (India — DPDP Act)
- **Section 4 & 6 (Lawful Processing & Explicit Consent):** Data is processed only when the student manually inputs it. Zero ambient data harvesting.
- **Section 8 (Data Security Safeguards):** All records remain confined to the student's authenticated operating system account under local file permission boundaries.
- **Section 12 (Right to Access, Correction & Erasure):** Students can inspect, modify, or erase every individual record through the native UI or directly via standard SQLite commands.

### B. General Data Protection Regulation (EU GDPR)
- **Article 25 (Data Protection by Design & by Default):** Privacy is not an opt-in toggle; offline local sovereignty is the foundational default state of STUNT.
- **Article 17 (Right to Erasure / Right to be Forgotten):** Selecting *"Purge Local Database"* in the Security Center executes an immediate, irreversible file deletion of `stunt_database.db`.
- **Article 20 (Right to Data Portability):** The *"Export Full Data (JSON)"* feature generates an unencrypted, standardized JSON file containing all academic, attendance, and financial records for effortless transfer.

### C. California Consumer Privacy Act (CCPA) / CPRA
- **Zero Sale or Sharing of Personal Data:** STUNT does not monetize, rent, transfer, or exchange student metrics with advertisers, corporate entities, or academic institutions.

---

## 5. Third-Party Integrations & Transparency

STUNT maintains radical transparency regarding external dependencies and tools:

1. **J.A.R.V.I.S. Mark 58 (Apex Core):**
   - J.A.R.V.I.S. Mark 58 is an independent sovereign AI assistant engineered by Akul Bhatnagar.
   - Integration operates exclusively through `actions/stunt_bridge.py`.
   - Voice synthesis uses the native operating system speech engine (Microsoft SAPI on Windows) without transmitting audio recordings to cloud speech brokers.
2. **PyQt6 & Desktop Window Manager (DWM):**
   - UI styling and hardware-accelerated Acrylic / Mica glassmorphism use native Windows DWM APIs via `ctypes`. No third-party electron bloatware, tracking cookies, or remote CSS dependencies are loaded.
3. **No External CDN Dependencies in Production:**
   - All fonts, icons, styling rules, and media assets are bundled directly within the local project directory and packaged inside `STUNT.exe`.

---

## 6. Plain-Language Student Translation

| What Commercial Student Apps Do | What STUNT Does |
| :--- | :--- |
| Require mandatory sign-up with phone numbers, emails, and OTPs. | **Zero sign-up required.** Runs immediately on your machine without an account. |
| Upload your timetable, grades, and location to remote cloud databases. | **100% on your laptop.** Stored in local SQLite (`stunt_database.db`). |
| Embed Google Analytics, Facebook Pixel, and advertisement banners. | **Zero analytics. Zero tracking beacons. Zero advertisements.** |
| Sell anonymized attendance and behavioral metrics to aggregators. | **Never sells or shares data.** The developer cannot see your records. |
| Lock your data inside closed proprietary formats. | **Full export.** Download your complete database as clean JSON at any time. |
| Retain deleted accounts in cloud backups for 90+ days. | **Instant wipe.** One click deletes your local database permanently. |

---

## 7. Developer Contact & Security Disclosure

STUNT is developed and maintained as an open-source academic workstation by:

* **Lead Architect:** Akul Bhatnagar  
* **Institution:** NMIMS Mumbai (BBA International Business)  
* **Official Codebase:** [S.T.U.N.T GitHub Repository](https://github.com/bhatnagarakul5-debug/S.T.U.N.T-Student-Tracker-for-Unified-Navigation-Tasks)  
* **AI Companion Codebase:** [JARVIS Mark 58 GitHub Repository](https://github.com/bhatnagarakul5-debug/JARVIS-MARK-LVIII)  
* **Responsible Disclosure:** For security audits, architectural questions, or vulnerability reports, please open an issue or security advisory on the official GitHub repository.

*“Your academics are your personal journey. Your data belongs to you.”*
