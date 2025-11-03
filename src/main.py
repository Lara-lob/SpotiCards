# src/main.py
import argparse
from spotify_api import get_playlist_info, get_playlist_tracks
from storage import save_metadata, load_metadata, get_playlist_data_dirs, save_card_image

from card_generator import generate_and_save_cards_for_playlist
from config import get_design, load_designs
from metadata_cleaner import clean_playlist_metadata



def parse_args():
    parser = argparse.ArgumentParser(description="Generate track cards for Spotify playlists.")
    parser.add_argument("--playlist", type=str, help="Spotify playlist URL or ID")
    parser.add_argument("--custom-name", type=str, help="Custom folder name for playlist")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing data without prompts")
    parser.add_argument("--design", type=str, choices=["simple", "colors", "vaporwave"], help="Card design option") # TODO: expand design options
    parser.add_argument("--skip-prompts", action="store_true", help="Skip interactive prompts and use defaults")
    return parser.parse_args()


def get_input_or_default(prompt, arg_value, default="", skip_prompts=False):
    if arg_value:
        return arg_value
    if skip_prompts:
        return default
    return input(prompt).strip()


def main():
    args = parse_args()
    skip_prompts = args.skip_prompts
    overwrite = True if skip_prompts else args.overwrite

    playlist_input = get_input_or_default("Enter playlist URL or ID: ", args.playlist, "3NpbDSpIze4spXHTJrR21q", skip_prompts)
    # fetch playlist information
    playlist_info = get_playlist_info(playlist_input)
    print(
        f"Playlist: {playlist_info['name']} "
        f"({playlist_info['num_tracks']} tracks) "
        f"by {playlist_info['owner']}")
    
    # set up output directories
    custom_name = get_input_or_default("Enter custom folder name: ", args.custom_name, "", skip_prompts)
    metadata_dir, cards_dir = get_playlist_data_dirs(
        custom_name, playlist_info['name'], playlist_info['id'], overwrite=overwrite)
    
    # choose design option TODO: include available designs dynamically
    design_option = get_input_or_default("Choose card design option: ", args.design, "simple", skip_prompts)
    designs = load_designs()
    if design_option not in designs:
        print(f"Design option '{design_option}' not found. Using 'simple' design.")
    design = get_design(design_option)

    # fetch playlist tracks
    raw_tracks = get_playlist_tracks(playlist_input)
    tracks = clean_playlist_metadata(raw_tracks)

    # save track metadata to JSON file
    save_metadata(tracks, dir=metadata_dir)

    # generate and save cards (front and back) for each track
    generate_and_save_cards_for_playlist(tracks, cards_dir, design=design)

if __name__ == "__main__":
    main()