@echo off
title AI Dialog App

echo.
echo Starting AI Dialog App...
echo Access URL: http://localhost:5000
echo Press Ctrl+C to stop the app
echo.

REM Start the app in background and open browser
start /b python app.py

REM Wait a moment for the server to start
timeout /t 3 /nobreak > nul

REM Open browser
start http://localhost:5000

REM Keep the window open
echo.
echo Browser opened automatically!
echo Press any key to stop the app...
pause > nul

REM Try to stop the Python process
taskkill /f /im python.exe > nul 2>&1 