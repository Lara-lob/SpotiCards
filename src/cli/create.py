# src/cli/create.py
import argparse
from pathlib import Path

from ..core.spotify_client import get_playlist_info, get_playlist_tracks
from ..core.metadata import clean_playlist_metadata
from ..cards.storage import save_metadata, get_playlist_data_dirs
from ..cards.generator import generate_and_save_cards_for_playlist
from ..config import get_design, load_designs


def get_input_or_default(prompt, arg_value, default="", skip_prompts=False):
    if arg_value:
        return arg_value
    if skip_prompts:
        return default
    return input(prompt).strip()


def create_cards(args):
    """
    Main function for creating cards from a Spotify playlist.
    """
    skip_prompts = args.skip_prompts
    overwrite = True if skip_prompts else args.overwrite

    playlist_input = get_input_or_default(
        "Enter playlist URL or ID: ", 
        args.playlist, 
        "3NpbDSpIze4spXHTJrR21q", 
        skip_prompts
    )
    
    # fetch playlist information
    playlist_info = get_playlist_info(playlist_input)
    print(
        f"Playlist: {playlist_info['name']} "
        f"({playlist_info['num_tracks']} tracks) "
        f"by {playlist_info['owner']}"
    )

    # set up output directories
    custom_name = get_input_or_default(
        "Enter custom folder name (Press Enter to use playlist name): ",
        args.custom_name, 
        "", 
        skip_prompts
    )
    playlist_dir, cards_dir = get_playlist_data_dirs(
        custom_name, 
        playlist_info['name'], 
        playlist_info['id'], 
        overwrite=overwrite
    )
    
    # choose design option
    design_option = get_input_or_default(
        "Choose card design option\n"
        "(1) simple: black/white minimal \n"
        "(2) colors: colorful backgrounds\n"
        "(3) vaporwave: retro aesthetic with neon colors\n"
        "Enter choice (1-3) or design name: ", 
        args.design, 
        "simple", 
        skip_prompts
    )
    designs = load_designs()
    design_option = {
        "1": "simple",
        "2": "colors",
        "3": "vaporwave"
    }.get(design_option, design_option)
    
    if design_option not in designs:
        print(f"Design option '{design_option}' not found. Using 'simple' design.")
    design = get_design(design_option)

    # fetch playlist tracks
    raw_tracks = get_playlist_tracks(playlist_input)
    tracks = clean_playlist_metadata(raw_tracks)

    # save track metadata to JSON file
    save_metadata(tracks, dir=playlist_dir)

    # generate and save cards (front and back) for each track
    generate_and_save_cards_for_playlist(tracks, cards_dir, design=design)


def add_create_parser(subparsers):
    """
    Add the 'create' subcommand parser.
    """
    parser = subparsers.add_parser(
        'create',
        help='Generate track cards for Spotify playlists'
    )
    parser.add_argument("--playlist", type=str, help="Spotify playlist URL or ID")
    parser.add_argument("--custom-name", type=str, help="Custom folder name for playlist")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing data without prompts")
    parser.add_argument("--design", type=str, choices=["simple", "colors", "vaporwave"], help="Card design option")
    parser.add_argument("--skip-prompts", action="store_true", help="Skip interactive prompts and use defaults")
    parser.set_defaults(func=create_cards)