# src/cli/main.py
import argparse
from .create import add_create_parser
from .play import add_play_parser


def main():
    """
    Main CLI entry point with subcommands.
    """
    parser = argparse.ArgumentParser(
        prog='spoticards',
        description='Generate and play with Spotify playlist cards'
    )
    
    subparsers = parser.add_subparsers(
        title='commands',
        description='Available commands',
        dest='command',
        required=True
    )
    
    # Add subcommand parsers
    add_create_parser(subparsers)
    add_play_parser(subparsers)
    
    # Parse arguments and call appropriate function
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()