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


# TODO: find original release date
def clean_track_metadata(track: dict, log: bool = True) -> dict | None:
    """
    Clean and standardize single track metadata to ensure required fields are present and correct.
    Args:
        track (dict): Track metadata dictionary
        log (bool): Whether to log invalid tracks
    Returns:
        dict | None: Validated track metadata or None if invalid
    """
    # Validate essential fields
    name = track.get("name")
    artists = track.get("artists")
    uri = track.get("spotify_uri")
    release_date = track.get("release_date", "")

    if not name or not artists or not uri:
        if log:
            print(f"Skipping track due to missing metadata: {name or 'Unknown'}")
        return None
    
    # Extract release year
    try:
        year = int(release_date[:4]) if release_date else None
    except ValueError:
        if log:
            print(f"Skipping track due to invalid release date: {name} -> {release_date}")
        return None
    
    # Build cleaned track metadata
    clean_track = {
            "name_original": track["name"],
            "name_cleaned": clean_title(track["name"], remove_version=False),
            "artists": ", ".join(track["artists"]),
            "album": track["album"],
            "release_year": year,
            "spotify_uri": track["spotify_uri"]
        }
    
    return clean_track


def clean_playlist_metadata(raw_tracks: list[dict]) -> list[dict]:
    """
    Clean and standardize track metadata for playlist.
    Args:
        raw_tracks (list[dict]): List of raw track metadata dictionaries
    Returns:
        list[dict]: List of cleaned track metadata dictionaries
    """
    clean_tracks = []
    for track in raw_tracks:
        clean_track = clean_track_metadata(track)
        clean_tracks.append(clean_track)
    print(f"Cleaned metadata for {len(clean_tracks)}/{len(raw_tracks)} tracks.")
    return clean_tracks