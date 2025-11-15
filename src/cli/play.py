# src/cli/play.py
from ..core.data_loader import get_available_playlists, load_playlist_metadata
from ..config import DATA_DIR



def play_game(args):
    """
    Main function for playing the timeline game.
    """
    if args.list:
        playlists = get_available_playlists(DATA_DIR / "playlists")
        if not playlists:
            print("No playlists found. Create one first with 'spoticards create'")
            return
        print("\nAvailable playlists:")
        for p in playlists:
            print(f"  - {p}")
        return
    
    # Get playlist folder
    if not args.folder:
        playlists = get_available_playlists(DATA_DIR / "playlists")
        if not playlists:
            print("No playlists found. Create one first with 'spoticards create'")
            return
        if len(playlists) == 1:
            folder = playlists[0]
            print(f"Using playlist: {folder}")
        else:
            print("Available playlists:")
            for p in playlists:
                print(f"  - {p}")
            folder = input("\nEnter playlist folder name: ").strip()
    else:
        folder = args.folder
    
    # Load playlist data
    playlist_path = DATA_DIR / "playlists" / folder
    if not playlist_path.exists():
        print(f"Playlist folder not found: {folder}")
        return
    
    tracks = load_playlist_metadata(playlist_path)
    if not tracks:
        print(f"No metadata found in {folder}")
        return
    
    print(f"Loaded {len(tracks)} tracks from '{folder}'")
    
    # Launch GUI
    from ..game.gui import main as launch_gui
    launch_gui(tracks, cards_dir=playlist_path / "cards")


def add_play_parser(subparsers):
    """
    Add the 'play' subcommand parser.
    """
    parser = subparsers.add_parser(
        'play',
        help='Play the timeline game with saved playlist cards'
    )
    parser.add_argument("--folder", type=str, help="Playlist folder name to play with")
    parser.add_argument("--list", action="store_true", help="List available playlists")
    parser.set_defaults(func=play_game)