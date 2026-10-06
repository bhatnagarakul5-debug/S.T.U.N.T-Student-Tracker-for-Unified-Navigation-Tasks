# STUNT & J.A.R.V.I.S. Mark 58 — Privacy Policy & Data Sovereignty Charter
**Effective Date:** September 30, 2026  
**Platforms:** STUNT Campus OS (Windows, macOS, Mobile, Web) & J.A.R.V.I.S. Mark 58 (Apex Core)  
**Lead Developer:** Akul Bhatnagar  
**Classification:** Confidential & Sovereign Student Operating Framework  

---

## 1. Core Philosophy: Absolute Data Sovereignty

STUNT is engineered on the foundational principle of **Local-First, Sovereign Student Software**. Unlike commercial campus apps and university ERP portals that track student locations, monetize behavioral profiles, display ads, or sell data to third-party brokers:

- **Zero Advertising & Zero Telemetry:** STUNT transmits no analytics, tracking beacons, or behavioral telemetry to ad networks or data aggregators.
- **Local Storage by Default:** Your grades, attendance logs, timetables, syllabus notes, and financial ledger reside exclusively in your local SQLite database (`stunt_database.db`).
- **User-Owned Cloud Sync:** When cloud sync is active, records are encrypted end-to-end and stored in your private database partition under strict Row-Level Security (RLS). You can purge your cloud data at any time with one click.
- **No Model Training on Private Data:** Your course notes, assignment drafts, and academic transcripts are never used to train public commercial AI models.

---

## 2. Information Handled & Security Boundaries

### A. Academic & Attendance Data
- **Attendance Records:** Subject names, attendance percentages, dates, and bunk safety margins are computed locally using exact integer mathematics.
- **Timetable & Course Schedule:** Class timings, classroom numbers, and faculty details are stored on-device to enable offline conflict detection and countdown timers without internet access.
- **Grades & SGPA:** Credits, grade points, and target CGPA calculations are strictly private to your local session.

### B. Personal Finances & Roommate Bills
- **Transaction Ledger:** Allowance credits, expenses, and category totals are processed on-device.
- **Group Expense Splitter:** Roommate splits generate local calculations or direct peer-to-peer UPI deep-links (`upi://pay`). STUNT does not hold student funds, charge transaction fees, or act as an intermediary bank.

### C. J.A.R.V.I.S. Mark 58 Voice & AI Integration
- **Two-Way Sovereign Bridge:** J.A.R.V.I.S. Mark 58 communicates with STUNT through an isolated local Inter-Process Communication (IPC) bridge bound strictly to `127.0.0.1`.
- **Microphone & Voice Privacy:** Voice recognition routines are triggered only by explicit user invocation. Audio frames are never archived on persistent external surveillance servers.
- **Anti-Shoulder Surfer Protocol:** Optional privacy blur mode instantly conceals grades, attendance figures, and financial balances whenever an unauthorized observer is detected or upon pressing `Ctrl+Shift+P`.

---

## 3. Security Architecture & Threat Defense

To protect student workstations and mobile devices, STUNT and JARVIS Mark 58 implement multi-layer defensive safeguards:

1. **Localhost Socket Isolation:** All internal API and bridge endpoints bind exclusively to loopback addresses (`127.0.0.1` and `::1`), blocking remote discovery on shared university campus Wi-Fi networks.
2. **Canonical Path Traversal Shield:** File import/export routines strictly validate canonical file paths, preventing malicious path traversal outside your designated STUNT directory.
3. **Token Bucket Rate Limiting:** High-frequency API calls to language models are throttled locally to prevent runaway token expenditure.
4. **Tamper-Evident Event Logging:** Audit trails are recorded in local SQLite logs, enabling students to inspect every single database mutation.
5. **Instant Local Purge:** Deleting `stunt_database.db` or selecting *"Purge Local Data"* permanently erases all records from your workstation with zero residual traces.

---

## 4. Contact & Developer Transparency

STUNT was created by **Akul Bhatnagar** (NMIMS Mumbai BBA International Business) to solve real, everyday academic friction for students.

- **GitHub Repository:** [bhatnagarakul5-debug/S.T.U.N.T-Student-Tracker-for-Unified-Navigation-Tasks](https://github.com/bhatnagarakul5-debug/S.T.U.N.T-Student-Tracker-for-Unified-Navigation-Tasks)
- **JARVIS Mark 58 Repository:** [bhatnagarakul5-debug/JARVIS-MARK-LVIII](https://github.com/bhatnagarakul5-debug/JARVIS-MARK-LVIII)
- **Security Contact:** Akul Bhatnagar (Student Developer & System Principal)
