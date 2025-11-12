# config/settings.py
from pathlib import Path

# Base directory (project root)
BASE_DIR = Path(__file__).parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Assets directory
ASSETS_DIR = BASE_DIR / "assets"

# Config directory
CONFIG_DIR = BASE_DIR / "config"