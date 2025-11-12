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


def _deep_merge(base: dict, override: dict) -> dict:
    """
    Deep merge two dictionaries, with override taking precedence.
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _validate_and_warn(design_name: str, design: dict, defaults: dict, path: str = "") -> None:
    """
    Validate design structure and warn about missing fields.
    Args:
        design_name: Name of the design being validated
        design: Current design dict
        defaults: Default design dict for comparison
        path: Current path in nested structure (for error messages)
    """
    for key, default_value in defaults.items():
        current_path = f"{path}.{key}" if path else key
        
        if key not in design:
            print(f"⚠️  Missing '{current_path}' in design '{design_name}', using default")
        elif isinstance(default_value, dict) and isinstance(design[key], dict):
            # Recursively validate nested dicts
            _validate_and_warn(design_name, design[key], default_value, current_path)


def get_design(name: str, validate: bool = False) -> dict:
    """
    Load and normalize a specific card design configuration by name.
    Args:
        name: Name of the design to load
        validate: Whether to validate and warn about missing fields
    Returns:
        dict: Complete design configuration with defaults applied
    """
    designs = load_designs()
    
    # Get the simple design as default
    defaults = designs.get("simple")
    if not defaults:
        raise ValueError("'simple' design must be defined as the default")
    
    # Get requested design or fallback to simple
    if name not in designs:
        print(f"⚠️  Design '{name}' not found, using 'simple' design")
        return defaults
    
    design = designs[name]
    
    # Validate before merging (optional)
    if validate and name != "simple":
        for side in ["front", "back"]:
            if side in design:
                _validate_and_warn(name, design.get(side, {}), defaults[side], side)
    
    # Deep merge with defaults
    result = {
        "front": _deep_merge(defaults["front"], design.get("front", {})),
        "back": _deep_merge(defaults["back"], design.get("back", {}))
    }
    
    return result


def resolve_asset_path(path_str: str | None) -> Path | None:
    """
    Resolve asset path relative to ASSETS_DIR if not absolute.
    Args:
        path_str: Path string or None
    Returns:
        Resolved Path object or None
    """
    if not path_str:
        return None
    p = Path(path_str)
    if not p.is_absolute():
        p = ASSETS_DIR / p
    return p