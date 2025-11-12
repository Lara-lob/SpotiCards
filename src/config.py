# src/config.py
import json
from pathlib import Path
import sys

# Add project root to path to import from config package
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from config.settings import CONFIG_DIR, ASSETS_DIR, DATA_DIR


CONFIG_PATH = CONFIG_DIR / "design_config.json"


def load_designs() -> dict:
    """
    Load the full card design configuration file.
    Returns:
        dict: All designs from JSON
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Design configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_design(name: str) -> dict:
    """
    Load and normalize a specific card design configuration by name.
    """
    designs = load_designs()
    design = designs.get(name, designs["simple"])  # default to simple design

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