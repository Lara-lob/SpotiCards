# src/core/data_loader.py
import json
from pathlib import Path
from typing import Optional


def get_available_playlists(data_dir: Path) -> list[str]:
    """
    List all available playlist folders in the data directory.
    
    Args:
        data_dir (Path): Base data directory containing playlist folders
        
    Returns:
        list[str]: List of playlist folder names
    """
    if not data_dir.exists():
        return []
    
    playlists = [
        d.name for d in data_dir.iterdir() 
        if d.is_dir() and (d / "metadata.json").exists()
    ]
    return sorted(playlists)


def load_playlist_metadata(playlist_folder: Path) -> Optional[list[dict]]:
    """
    Load track metadata from a playlist folder.
    
    Args:
        playlist_folder (Path): Path to playlist folder
        
    Returns:
        list[dict] | None: List of track metadata or None if not found
    """
    metadata_path = playlist_folder / "metadata.json"
    
    if not metadata_path.exists():
        return None
    
    with open(metadata_path, "r", encoding="utf-8") as f:
        tracks = json.load(f)
    
    return tracks