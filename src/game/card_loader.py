# src/game/card_loader.py
from pathlib import Path



def get_card_image_path(card: dict, side: str, cards_dir:Path) -> Path | None:
    """
    Resolve the file path for a card image based on card metadata and side.
    Args:
        card (dict): Card metadata dictionary
        side (str): "front" or "back"
        cards_dir (Path): Base directory where card images are stored
    Returns:
        Path | None: Resolved file path or None if not found
    """
    year = card["release_year"]
    name = card["name_cleaned"]
    filename = f"{year}_{name}".replace(" ", "_")
    path = cards_dir / f"{filename}_{side}.png"
    
    if not path.exists():
        print(f"Card image not found at {path}")
        return None
    
    return path

