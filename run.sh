#!/bin/bash
# Valorant Stats Scraper - Terminal UI Launcher
# This script launches the interactive terminal application

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Valorant Stats Scraper - Terminal UI ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import textual" &> /dev/null; then
    echo "[INFO] Installing required packages..."
    pip install -r requirements.txt
fi

# Launch the app
echo "[INFO] Launching Valorant Stats Scraper..."
echo ""
python3 app.py
