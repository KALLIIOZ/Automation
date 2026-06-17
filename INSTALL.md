# 🚀 Installation Guide - Valorant Stats Scraper TUI

## Prerequisites
- **Python 3.9 or higher**
- **pip** (Python package manager)

## Step 1: Install Python

### Windows
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

### macOS
```bash
brew install python3
```

### Linux
```bash
sudo apt-get install python3 python3-pip
```

## Step 2: Install Dependencies

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install textual rich requests beautifulsoup4 pandas openpyxl
```

## Step 3: Configure Players

Edit `nombres.txt` and add your players in the format:
```
PlayerName#PlayerID
```

Example:
```
Lord Bane#Sith
Professional Player#RANK1
```

## Step 4: Run the Application

### Windows
Double-click `run.bat` or run in terminal:
```bash
python app.py
```

### macOS/Linux
Make the script executable:
```bash
chmod +x run.sh
./run.sh
```

Or directly:
```bash
python3 app.py
```

## 🎮 Using the Application

Once launched, you'll see an interactive terminal interface with:
- **Left sidebar**: Menu with available options
- **Center panel**: Live logs and output
- **Top**: Header with title and time
- **Bottom**: Footer with help commands

### Available Commands

| Button | Function |
|--------|----------|
| ▶ Fetch Stats | Fetch competitive statistics |
| ▶ Fetch Premier | Fetch Premier division stats |
| ▶ Export to Excel | Export all data to Excel |
| ▶ View Results | Show summary of results |
| ▶ Clear Logs | Clear the log viewer |
| ✕ Exit | Exit the application |

### Keyboard Shortcuts

- **Q** - Quit the application
- **Tab** - Navigate between menu items
- **Enter** - Press the selected button

## 📁 Output Files

After running the app, you'll find:
- `stats/` - Competitive statistics (JSON files)
- `stats_premier/` - Premier statistics (JSON files)
- `Valorant_Stats.xlsx` - Exported Excel file

## ⚠️ Troubleshooting

### Python not found
Make sure Python is added to PATH. On Windows, reinstall Python and check "Add Python to PATH".

### Missing textual module
Run: `pip install textual`

### API errors
- Check your internet connection
- Verify player names are correct in `nombres.txt`
- The API might be temporarily unavailable

### Permission denied on run.sh
Run: `chmod +x run.sh`

## 📞 Support

For issues or questions, check the main README.md file.
