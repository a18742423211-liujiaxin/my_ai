@echo off
title AI Dialog App Launcher

echo.
echo ===============================================================
echo                   AI Dialog App Launcher
echo ===============================================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check dependencies
echo Checking Python dependencies...
python -c "import flask, requests, openai, dashscope" > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python dependencies missing!
    echo Please run: pip install flask requests openai dashscope
    pause
    exit /b 1
)

REM Check config file
echo Checking config file...
if not exist "config.py" (
    echo ERROR: config.py not found!
    echo Please ensure config.py exists with API keys configured
    pause
    exit /b 1
)

REM Check main app file
if not exist "app.py" (
    echo ERROR: app.py not found!
    pause
    exit /b 1
)

echo Environment check passed!
echo.
echo Starting AI Dialog App...
echo Access URL: http://localhost:5000
echo Press Ctrl+C to stop the app
echo.

REM Start the application
python app.py

echo.
echo App stopped
pause 