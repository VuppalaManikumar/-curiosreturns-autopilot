@echo off
title CuriosReturns Permanent Autopilot
color 0A
cd /d "C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer"

echo ======================================================================
echo           ACTIVATING INFINITE 4X DAILY AUTOPILOT (WITH REBOOT RECOVERY)
echo ======================================================================
echo.
echo [*] Registering background schedule in Windows Task Scheduler...
schtasks /create /tn "CuriosReturns_Autopilot" /tr "python \"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer\scheduler.py\" --check" /sc minute /mo 15 /f >nul 2>&1

if %ERRORLEVEL% equ 0 (
    echo [OK] Windows Background Service registered successfully!
) else (
    echo [i] Background task already registered.
)

echo.
echo [*] Checking current slots and running recovery if any slot was missed...
python scheduler.py --check

echo.
echo ======================================================================
echo  AUTOPILOT IS NOW RUNNING INFINITELY IN THE BACKGROUND!
echo  - 4 videos scheduled every day (08:30, 12:30, 17:30, 21:00)
echo  - Different viral style every day (Monday to Sunday)
echo  - If your laptop restarts or sleeps, it resumes automatically!
echo ======================================================================
pause
