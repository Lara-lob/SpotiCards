# src/storage.py
import json
import re
from pathlib import Path

from config import METADATA_DIR, CARDS_DIR



def sanitize_name(name: str) -> str:
    """
    Sanitize a string to be safe for use as a path.
    Args:
        name (str): Original name string
    Returns:
        str: Sanitized name string
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    return sanitized.strip()[:100]


def get_playlist_data_dirs(custom_name: str, playlist_name: str, playlist_id: str) -> tuple[Path, Path]:
    """
    Get and create the metadata and cards directory paths for a given playlist.
    Args:
        custom_name (str): Custom name for the playlist
        playlist_name (str): Name of the playlist
        playlist_id (str): Spotify ID of the playlist
    Returns:
        tuple[Path, Path]: (metadata_dir, cards_dir) paths
    """
    folder_name = sanitize_name(custom_name) if custom_name else sanitize_name(playlist_name)
    if not folder_name:
        folder_name = playlist_id  # fallback if name is empty

    metadata_folder = METADATA_DIR / folder_name
    cards_folder = CARDS_DIR / folder_name

    # Ensure directories exist
    metadata_folder.mkdir(parents=True, exist_ok=True)
    cards_folder.mkdir(parents=True, exist_ok=True)

    return metadata_folder, cards_folder


def save_metadata(
        tracks: list[dict],
        dir: Path = METADATA_DIR,
        filename: str = "track_metadata.json"
        ) -> None:
    """
    Save track metadata to a JSON file in the metadata directory.
    Args:
        tracks (list[dict]): List of track metadata dictionaries
        dir (Path): Directory to save the metadata file
        filename (str): Name of the JSON file to save the metadata
    """
    metadata_path = dir / filename
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)
    print(f"Saved metadata for {len(tracks)} tracks to {metadata_path}")

    
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