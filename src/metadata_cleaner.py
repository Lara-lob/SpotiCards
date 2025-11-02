# src/metadata_cleaner.py
from datetime import datetime
import re



def clean_title(name: str, remove_version: bool = False) -> str:
    """
    Clean and standardize track title.
    Args:
        title (str): Original track title
        remove_version (bool): Whether to remove version info like "Acoustic", "Live"
    Returns:
        str: Cleaned track title
    """
    # Remove "feat." or "featuring" or "with (...)"
    name = re.sub(r"\s*[\(\[]?(feat\.|featuring|with)\s+[^\)\]]*[\)\]]?", "", name, flags=re.IGNORECASE)

    # Remove remaster/digital master patterns like:
    # - " - 2018 Remaster"
    # - " - Remastered 2018"
    # - " - 2024 Digital Master"
    # - " - 2011 Remastered Version"
    name = re.sub(r"\s*-\s*\d{4}\s*(Remaster(ed)?( Version)?|Digital Master(ed)?)", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*-\s*(Remaster(ed)?( Version)?|Digital Master(ed)?)\s*\d{0,4}", "", name, flags=re.IGNORECASE)

    # Optional: remove " - Live" or " - Acoustic"
    if remove_version:
        name = re.sub(r"\s*-\s*(Live|Acoustic|Mono|Stereo Mix).*", "", name, flags=re.IGNORECASE)

    # Clean up stray punctuation and whitespace
    name = re.sub(r"\s+[-–]+\s*$", "", name).strip()
    return name

def clean_track_metadata(raw_tracks: list[dict]) -> list[dict]:
    """
    Clean and standardize track metadata.
    Args:
        raw_tracks (list[dict]): List of raw track metadata dictionaries
    Returns:
        list[dict]: List of cleaned track metadata dictionaries
    """
    cleaned_tracks = []
    for track in raw_tracks:
        date = track.get("release_date", "")
        try:
            year = int(date[:4]) if date else None
        except ValueError:
            year = None

        cleaned_track = {
            "name_original": track["name"],
            "name_cleaned": clean_title(track["name"], remove_version=False),
            "artists": ", ".join(track["artists"]),
            "album": track["album"],
            "release_year": year,
            "spotify_uri": track["spotify_uri"]
        }
        cleaned_tracks.append(cleaned_track)
    return cleaned_tracks