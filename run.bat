@echo off
REM Valorant Stats Scraper - Terminal UI Launcher
REM This script launches the interactive terminal application

echo.
echo ╔════════════════════════════════════════╗
echo ║   Valorant Stats Scraper - Terminal UI ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import textual" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required packages...
    pip install -r requirements.txt
)

REM Launch the app
echo [INFO] Launching Valorant Stats Scraper...
echo.
python app.py

pause
