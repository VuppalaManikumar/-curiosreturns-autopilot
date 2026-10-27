@echo off
title Post Next Scheduled Slot Immediately
color 0E
cd /d "C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer"

echo ======================================================================
echo             FORCE TRIGGER NEXT SCHEDULED VIDEO IMMEDIATELY            
echo ======================================================================
echo.
python scheduler.py --force-next
echo.
pause
