@echo off
title Generate Daily 3X Viral Batch
color 0A
cd /d "%~dp0"

echo ======================================================================
echo           GENERATE 3X DAILY VIRAL REEL BATCH (HIGH CONVERSION)       
echo ======================================================================
echo.
echo [*] Producing 3 high-retention reels across top money & viral niches...
echo [*] (Morning 8 AM, Lunch 1 PM, Evening 7 PM)
echo.

python main.py --count 3

echo.
echo ======================================================================
echo  All 3 videos ready! Check your outputs folder.
echo ======================================================================
pause
