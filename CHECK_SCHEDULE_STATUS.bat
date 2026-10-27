@echo off
title CuriosReturns Schedule Status
color 0B
cd /d "C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer"
python scheduler.py --status
echo.
echo Press any key to refresh status...
pause >nul
goto :eof
