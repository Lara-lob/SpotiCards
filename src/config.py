# src/config.py
from Pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Base data directory
DATA_DIR = BASE_DIR / "data"

# Subdirectories
METADATA_DIR = DATA_DIR / "metadata"
CARDS_DIR = DATA_DIR / "cards"

# Ensure directories exist
for directory in [DATA_DIR, METADATA_DIR, CARDS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)