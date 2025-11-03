# src/config.py
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Base data directory
DATA_DIR = BASE_DIR / "data"

# Subdirectories
METADATA_DIR = DATA_DIR / "metadata"
CARDS_DIR = DATA_DIR / "cards"

# Ensure directories exist
for directory in [DATA_DIR, METADATA_DIR, CARDS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

CONFIG_DIR = BASE_DIR / "config"
CONFIG_PATH = CONFIG_DIR / "design_config.json"
ASSETS_DIR = BASE_DIR / "assets"


def load_designs() -> dict:
    """
    Load the full card design configuration file.
    Returns:
        dict: All designs from JSON
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Design configuration file not found: {DESIGN_CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_design(name: str) -> dict:
    """
    Load and normalize a specific card design configuration by name.
    """
    designs = load_designs()
    design = designs.get(name, designs["simple"]) # default to simple design

    # Merge with default to ensure all fields are present
    design = {
        "front": {**designs["simple"]["front"], **design.get("front", {})},
        "back": {**designs["simple"]["back"], **design.get("back", {})}
    }

    # convert entries into lists
    fields = ["background_color", "font_color"]
    for side in ["front", "back"]:
        for key in fields:
            value = design[side].get(key)
            if value is None:
                design[side][key] = []
            elif isinstance(value, str):
                design[side][key] = [value]
            elif isinstance(value, list):
                design[side][key] = value
            else:
                raise ValueError(f"Invalid type for {key} in {side} design: {type(value)}")
    return design

def resolve_asset_path(path_str: str | None) -> Path | None:
    if not path_str:
        return None
    p = Path(path_str)
    if not p.is_absolute():
        p = ASSETS_DIR / p
    return p