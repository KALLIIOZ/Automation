"""
Configuration file for Valorant Stats Scraper
"""

# Directories
STATS_DIR = 'stats'
STATS_PREMIER_DIR = 'stats_premier'
PREDICTIONS_DIR = 'predict'

# File names
PLAYERS_FILE = 'nombres.txt'
PREDICTIONS_FILE = 'nombres_jugadoras.txt'

# API Configuration
API_BASE_URL = 'https://api.tracker.gg/api/v2/valorant'
TRACKER_REFERER = 'https://tracker.gg/'

# Default User Agent
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'

# API Headers
API_HEADERS = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': TRACKER_REFERER,
    'User-Agent': DEFAULT_USER_AGENT,
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
}

# Export settings
EXCEL_FILENAME = 'Valorant_Stats.xlsx'
EXPORT_SHEETS = {
    'Competitivo': 'stats',
    'Premier': 'stats_premier',
}

# Application settings
APP_TITLE = 'Valorant Stats Scraper'
APP_VERSION = '1.0'
DEBUG = False
