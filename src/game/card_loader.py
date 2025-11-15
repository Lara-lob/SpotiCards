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

def card_image_exists(card, side, cards_dir) -> bool:
    path = get_card_image_path(card, side, cards_dir)
    return path is not None and path.exists()
    
def validate_playlist_cards(tracks: list[dict], cards_dir: Path) -> list[dict]:
    """
    Check which cards are missing images.
    
    Returns:
        List of tracks with missing card images
    """
    missing = []
    for track in tracks:
        if not card_image_exists(track, "front", cards_dir) or \
           not card_image_exists(track, "back", cards_dir):
            missing.append(track)
    # TODO: add validation method (remove missing tracks, quit game?)
    return missing