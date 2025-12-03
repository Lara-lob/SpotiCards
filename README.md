# SpotiCards
Generate digital song cards for each track in a Spotify playlist, including title, artist, original release year, and a scannable Spotify QR code.

## Prerequisites

- Python 3.10 or higher
- A Spotify account
- Spotify Developer credentials (see setup below)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Lara-lob/SpotiCards.git
cd SpotiCards
```

2. Install the package:
```bash
pip install -e .
```

## Spotify API Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the app name and description (can be anything)
5. Once created, note your **Client ID** and **Client Secret**
6. Click "Edit Settings" and add `http://localhost:8888/callback` to the Redirect URIs
7. Save the settings

## Configuration

Create a `.env` file in the project root directory with your Spotify credentials:
**Tip:** Copy `.env.example` to `.env` and fill in your credentials.

## Usage

On first run, your browser will open for Spotify authentication. After authorizing, you'll be redirected to a localhost URL - copy this entire URL and paste it back into the terminal.

### Basic Card Generation
### Interactive Mode 

Simply run:
```bash
spoticards create
```

You'll be prompted for:
- Playlist URL or ID
- Custom folder name (optional, press Enter to use playlist name)
- Card design choice (number or design name)

**First Run:** Your browser will open for Spotify authentication. After authorizing, you'll be redirected to a localhost URL - copy this entire URL and paste it back into the terminal.

### Command Line Mode

Generate cards with all options specified:
```bash
spoticards create --playlist playlist_URL_or_ID
```

### Design Options

Choose from different card designs:
```bash
spoticards create --design simple     # Black & white minimal (default)
spoticards create --design colors     # Colorful backgrounds
spoticards create --design vaporwave  # Retro aesthetic
```

### Additional Options
```bash
# Custom folder name
spoticards create --custom-name "My Playlist"

# Skip all prompts (use defaults)
spoticards create --skip-prompts

# Overwrite existing data without asking
spoticards create  --overwrite

# Generate printable double-sided A4 sheets
spoticards create --generate-printable
```

## Output

Generated cards are saved to `data/playlists/<playlist_name>/cards/`:
- `YYYY_Song_Title_front.png` - Front side with song info
- `YYYY_Song_Title_back.png` - Back side with QR code
- *optional* `printable_cards.pdf` - A4 sheets for easy printing (```--generate-printable``` argument)

Metadata is saved to `data/playlists/<playlist_name>/metadata.json`
