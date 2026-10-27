@echo off
title Configure Auto-Influencer
color 0E
cd /d "%~dp0"

echo ======================================================================
echo             AUTO-INFLUENCER: QUICK CONFIGURATION WIZARD              
echo ======================================================================
echo.
echo Opening 'config.env' in Notepad...
echo You can paste your free Meta tokens or Gemini API key here.
echo Save and close Notepad when done!
echo.
notepad config.env
echo.
echo Configuration updated! You can now double click RUN_AUTOPILOT.bat
pause
