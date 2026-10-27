@echo off
title Stop CuriosReturns Autopilot
color 0C
cd /d "C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer"

echo ======================================================================
echo                 STOPPING CURIOUSRETURNS AUTOPILOT                     
echo ======================================================================
echo.
schtasks /delete /tn "CuriosReturns_Autopilot" /f >nul 2>&1
echo [OK] Background automated schedule has been paused.
echo No automatic videos will post until you run START_PERMANENT_AUTOPILOT.bat.
echo.
pause
