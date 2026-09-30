@echo off
title STUNT Official Showcase Website
cd /d "%~dp0"
echo Starting STUNT Official Showcase Web Portal on http://localhost:5000 ...
start "" "http://localhost:5000"
python -m http.server 5000
pause
