# src/storage.py
import json

from config import METADATA_DIR


def save_metadata(
        tracks: list[dict],
        filename: str = "track_metadata.json"
        )-> None:
    """
    Save track metadata to a JSON file in the metadata directory.
    Args:
        tracks (list[dict]): List of track metadata dictionaries
        filename (str): Name of the JSON file to save the metadata
    """
    metadata_path = METADATA_DIR / filename
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)

    
def load_metadata(filename: str = "track_metadata.json") -> list[dict]:
    """
    Load track metadata from a JSON file in the metadata directory.
    Args:
        filename (str): Name of the JSON file to load the metadata from
    Returns:
        list[dict]: List of track metadata dictionaries
    """
    metadata_path = METADATA_DIR / filename
    with open(metadata_path, "r", encoding="utf-8") as f:
        tracks = json.load(f)
    return tracks