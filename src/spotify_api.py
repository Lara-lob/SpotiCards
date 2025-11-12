# src/spotify_api.py
import os
import re

from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


# load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")



def extract_playlist_id(input_str: str) -> str:
    """
    Extract Spotify playlist ID from URL or return the ID if already provided.
    Args:
        input_str (str): Spotify playlist URL or ID
    Returns:
        str: Spotify playlist ID
    """
    match = re.search(r"playlist/([a-zA-Z0-9]+)", input_str)
    if match:
        return match.group(1)
    return input_str

def authenticate_spotify() -> Spotify:
    """
    Authenticate and return a Spotify client instance.
    Returns:
        Spotify: Authenticated Spotify client
    """
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-read-private"
    ))
    return sp

def get_playlist_info(input_str: str) -> dict:
    """
    Fetch playlist information from Spotify API.
    Args:
        input_str (str): The URL or ID of the Spotify playlist
    Returns:
        dict: Playlist information {name, owner, num_tracks, id}
    """
    # extract playlist ID
    playlist_id = extract_playlist_id(input_str)

    # initialize Spotify client with OAuth
    sp = authenticate_spotify()

    # fetch playlist information
    playlist = sp.playlist(playlist_id)
    playlist_info = {
        "name": playlist["name"],
        "owner": playlist["owner"]["display_name"],
        "num_tracks": playlist["tracks"]["total"],
        "id": playlist["id"]
    }
    return playlist_info

def get_playlist_tracks(input_str: str) -> list[dict]:
    """
    Fetch tracks from a Spotify playlist.
    Args:
        input_str (str): The URL or ID of the Spotify playlist
    Returns:
        list[dict]: List of track information {name, artist(s), album, release_date, spotify_uri}
    """
    # extract playlist ID
    playlist_id = extract_playlist_id(input_str)

    # initialize Spotify client with OAuth
    sp = authenticate_spotify()

    tracks = []
    offset = 0
    limit = 100  # max Spotify allows per request

    while True:
        response = sp.playlist_items(playlist_id, offset=offset, limit=limit)
        for item in response["items"]:
            track = item["track"]
            track_info = {
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "spotify_uri": track["uri"]
            }
            tracks.append(track_info)
        if response["next"] is None:
            break
        offset += limit
    
    return tracks

def get_earliest_release_spotify(track: dict) -> dict:
    """
    Search for earliest release date on Spotify.
    Args:
        track (dict): Track metadata dictionary
    Returns:
        dict: Track metadata with potentially updated release date
              and flag 'validate_release' set to True if conflicting dates found
    """
    # extract track details
    name = track.get("name_cleaned", track.get("name_original", ""))
    artist_str = track.get("artists", "")
    artist = artist_str.split(",")[0].strip() if artist_str else ""
    release_year = track.get("release_year")    
    
    # set flag to False initially
    track['validate_release'] = False

    # search Spotify for track
    sp = authenticate_spotify()

    query = f'track:{name} artist:{artist}'
    try:
        results = sp.search(q=query, type='track', limit=20)
    except Exception as e:
        print(f"Spotify search failed for '{name}' by '{artist}': {e}")
        track['validate_release'] = True
        return track
    
    # extract release years
    years = set()
    for item in results.get("tracks", {}).get("items", []):
        date = item["album"].get("release_date")
        if not date:
            continue

        match = re.match(r"(\d{4})", date)
        if match:
            years.add(int(match.group(1)))

    if not years:
        track['validate_release'] = True
        return track
    
    # determine earliest year
    earliest_year = min(years)
    if release_year and earliest_year != release_year:
        track['validate_release'] = True
        track['original_release_year'] = release_year
        track['release_year'] = earliest_year
    
    return track