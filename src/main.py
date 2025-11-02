# src/main.py
from spotify_api import get_playlist_info, get_playlist_tracks
from storage import save_metadata, load_metadata, get_playlist_data_dirs, save_card_image

from card_generator import generate_card_front, generate_card_back
from metadata_cleaner import clean_playlist_metadata



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
    raw_tracks = get_playlist_tracks(playlist_input)
    tracks = clean_playlist_metadata(raw_tracks)

    # save track metadata to JSON file
    custom_name = input("Enter a custom name for the playlist folder (press Enter to use playlist name): ").strip()
    metadata_dir, cards_dir = get_playlist_data_dirs(
        custom_name, playlist_info['name'], playlist_info['id'])
    save_metadata(tracks, dir=metadata_dir)

    # generate and save cards (front and back) for each track
    for track in tracks:
        year = track["release_year"]
        cleaned_name = track["name_cleaned"]
        filename_base = f"{year}_{cleaned_name}".replace(" ", "_")

        front_img = generate_card_front(track)
        back_img = generate_card_back(track)

        save_card_image(front_img, cards_dir, f"{filename_base}_front")
        save_card_image(back_img, cards_dir, f"{filename_base}_back")

    print(f"Generated cards saved to {cards_dir}.")

if __name__ == "__main__":
    main()
    # example ID for testing: 3NpbDSpIze4spXHTJrR21q