# src/main.py
from spotify_api import get_playlist_info, get_playlist_tracks
from storage import save_metadata, load_metadata, get_playlist_data_dirs



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
    custom_name = input("Enter a custom name for the playlist folder (press Enter to use playlist name): ").strip()
    metadata_dir, cards_dir = get_playlist_data_dirs(
        custom_name, playlist_info['name'], playlist_info['id'])
    save_metadata(tracks, dir=metadata_dir)


if __name__ == "__main__":
    main()
    # example ID for testing: 3NpbDSpIze4spXHTJrR21q