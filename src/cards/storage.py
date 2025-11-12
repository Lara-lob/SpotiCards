# src/cards/storage.py
import json
import shutil
from pathlib import Path
from PIL import Image

from ..config import DATA_DIR
from ..core.utils import sanitize_name


def get_playlist_data_dirs(
        custom_name: str, playlist_name: str, playlist_id: str, overwrite: bool = True
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
        tuple[Path, Path]: (playlist directory, cards directory)
    """
    folder_name = sanitize_name(custom_name) if custom_name else sanitize_name(playlist_name)
    if not folder_name:
        folder_name = playlist_id  # fallback if name is empty

    playlist_folder = DATA_DIR / "playlists" / folder_name
    cards_folder = playlist_folder / "cards"

    # Check for existing data and handle conflicts
    if playlist_folder.exists() and any(playlist_folder.iterdir()):
        print(f"Data for '{folder_name}' already exists.")
        while True:
            choice = 'O' if overwrite else \
            input("Choose an action - (O)verwrite, (R)ename, (C)ancel: ").strip().upper()
            if choice == 'O':
                if playlist_folder.exists():
                    shutil.rmtree(playlist_folder)
                print("Existing data deleted.")
                break
            elif choice == 'R':
                new_name = input("Enter a new name for the playlist folder: ").strip()
                folder_name = sanitize_name(new_name) if new_name else playlist_id
                playlist_folder = DATA_DIR / "playlists" / folder_name
                cards_folder = playlist_folder / "cards"
                if not playlist_folder.exists():
                    break
                else:
                    print(f"Folder '{folder_name}' also exists. Please choose another name.")
            elif choice == 'C':
                print("Operation cancelled by user.")
                exit(0)
            else:
                print("Invalid choice. Please enter O, R, or C.")

    # Ensure directories exist
    playlist_folder.mkdir(parents=True, exist_ok=True)
    cards_folder.mkdir(parents=True, exist_ok=True)

    return playlist_folder, cards_folder


def save_metadata(
        tracks: list[dict],
        dir: Path,
        filename: str = "metadata.json"
        ) -> None:
    """
    Save track metadata to a JSON file in the specified directory.
    
    Args:
        tracks (list[dict]): List of track metadata dictionaries
        dir (Path): Directory to save the metadata file
        filename (str): Name of the JSON file to save the metadata
    """
    metadata_path = dir / filename
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)
    print(f"Saved metadata for {len(tracks)} tracks to {metadata_path}")


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