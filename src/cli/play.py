# src/cli/play.py
import argparse


def play_game(args):
    """
    Main function for playing the timeline game.
    (Placeholder for future implementation)
    """
    print("Game functionality coming soon!")
    print(f"Folder: {args.folder if args.folder else 'Not specified'}")
    
    # TODO: Implement game logic
    # - Load playlist data from folder
    # - Initialize game state
    # - Start game loop


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