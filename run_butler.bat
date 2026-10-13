@echo off
REM Relaunches itself elevated (UAC prompt), then starts Butler in that console.
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"
python main.py %*
pause
