@echo off
title STUNT: Student Tracker for Unified Navigation & Tasks
cd /d "%~dp0"
echo Launching STUNT Desktop Application...

where pythonw >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start "" pythonw main.py
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        python main.py
    ) else (
        echo [ERROR] Python is not found on PATH. Please install Python 3.10+ from python.org!
        pause
    )
)
