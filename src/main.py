# src/main.py
from spotify_api import get_playlist_info, get_playlist_tracks
from storage import save_metadata, load_metadata



def main():
    # get playlist input from user
    playlist_input = input("Enter Spotify playlist URL or ID: ")
    
    # fetch playlist information
    playlist_info = get_playlist_info(playlist_input)
    print(
        f"Playlist: {playlist_info['name']} "
        f"({playlist_info['num_tracks']} tracks) "
        f"by {playlist_info['owner']}")
    
    # fetch playlist tracks
    tracks = get_playlist_tracks(playlist_input)
    print(f"Fetched {len(tracks)} tracks from the playlist.")

    # save track metadata to JSON file
    save_metadata(tracks)


if __name__ == "__main__":
    main()