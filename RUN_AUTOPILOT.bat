@echo off
title Auto-Influencer Autopilot
color 0B
cd /d "%~dp0"

echo ======================================================================
echo           AI INFLUENCER AUTOPILOT - 1-CLICK GENERATOR AND POSTER        
echo ======================================================================
echo.
echo [*] Checking Python environment...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo [ERROR] Python is not found in your PATH!
    echo Please install Python 3.10+ and check 'Add Python to PATH'.
    pause
    exit /b 1
)

echo [*] Launching automated pipeline...
echo.
python main.py

echo.
echo ======================================================================
echo  Finished! Check the newly created video in your outputs folder.
echo ======================================================================
pause
