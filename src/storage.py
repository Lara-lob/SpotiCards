# src/storage.py
import json
import re
import shutil

from pathlib import Path
from PIL import Image
from typing import Tuple

from config import METADATA_DIR, CARDS_DIR



# Utility functions
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


# TODO: add option to add to existing output
def get_playlist_data_dirs(
        custom_name:str, playlist_name:str, playlist_id:str, overwrite: bool = True
        ) -> tuple[Path, Path]:
    """
    Determine output directories and check for existing data.
    Handles naming conflicts through user prompts.
    Args:
        custom_name (str): Custom name for the playlist
        playlist_name (str): Name of the playlist
        playlist_id (str): Spotify ID of the playlist
        overwrite (bool): Whether to overwrite existing data without prompts
    Returns:
        tuple[Path, Path]: (metadata directory, cards directory)
    """
    folder_name = sanitize_name(custom_name) if custom_name else sanitize_name(playlist_name)
    if not folder_name:
        folder_name = playlist_id  # fallback if name is empty

    metadata_folder = METADATA_DIR / folder_name
    cards_folder = CARDS_DIR / folder_name

    # Check for existing data and handle conflicts
    if metadata_folder.exists() and any(metadata_folder.iterdir()) or \
       cards_folder.exists() and any(cards_folder.iterdir()):
        print(f"Data for '{folder_name}' already exists.")
        while True:
            choice = 'O' if overwrite else \
            input("Choose an action - (O)verwrite, (R)ename, (C)ancel: ").strip().upper()
            if choice == 'O':
                if metadata_folder.exists():
                    shutil.rmtree(metadata_folder)
                if cards_folder.exists():
                    shutil.rmtree(cards_folder)
                print("Existing data deleted.")
                break
            elif choice == 'R':
                new_name = input("Enter a new name for the playlist folder: ").strip()
                folder_name = sanitize_name(new_name) if new_name else playlist_id
                metadata_folder = METADATA_DIR / folder_name
                cards_folder = CARDS_DIR / folder_name
                if not metadata_folder.exists() and not cards_folder.exists():
                    break
                else:
                    print(f"Folder '{folder_name}' also exists. Please choose another name.")
            elif choice == 'C':
                print("Operation cancelled by user.")
                exit(0)
            else:
                print("Invalid choice. Please enter O, R, or C.")

    # Ensure directories exist
    metadata_folder.mkdir(parents=True, exist_ok=True)
    cards_folder.mkdir(parents=True, exist_ok=True)

    return metadata_folder, cards_folder


# Saving and loading output
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


def save_card_image(img: Image.Image, output_dir: Path, filename: str) -> Path:
    """
    Save a Pillow Image object as a PNG file.

    Args:
        img (Image.Image): Pillow Image object to save
        output_dir (Path): Directory to save the image
        filename (str): Filename without extension

    Returns:
        Path object of the saved image
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / f"{filename}.png"
    img.save(save_path, format="PNG")

    return save_path


# TODO: add function to compare existing metadata and update if needed and remove duplicates