# src/card_generator.py
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from typing import Tuple

from storage import save_card_image



def generate_qr_code(data: str, size: int = 300, border: int = 4,
                      error_correction=ERROR_CORRECT_H) -> Image.Image:
    """
    Generate a QR code for the given Spotify URI/URL.
    Args:
        data (str): Spotify URI or URL to encode in the QR code
        size (int): Size of the QR code image (pixels)
        border (int): Border size around the QR code
        error_correction: Error correction level for the QR code
    Returns:
        Image.Image: Generated QR code image
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=10,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img = img.resize((size, size), Image.NEAREST)

    return img


def generate_card_front(
        track: dict, card_size: int = 800, design_option: str = "simple"
        ) -> Image.Image:
    """
    Generate the front side of a song card.
    
    Args:
        track (dict): Track metadata dictionary
        card_size (int): Size of the card image (pixels)
        design_option (str): Design option for the card front
    Returns:
        Image.Image: Generated card front image
    """
    # default for now TODO: create design options
    # create base image
    img = Image.new("RGBA", (card_size, card_size), "white")
    draw = ImageDraw.Draw(img)

    # load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", size=int(card_size*0.08))
        year_font = ImageFont.truetype("arial.ttf", size=int(card_size*0.35))
        artists_font = ImageFont.truetype("arial.ttf", size=int(card_size*0.06))
    except:
        title_font = ImageFont.load_default(size=int(card_size*0.08))
        year_font = ImageFont.load_default(size=int(card_size*0.35))
        artists_font = ImageFont.load_default(size=int(card_size*0.06))

    # draw text elements
    name = track.get("name_cleaned", track.get("name_original", "Unknown Title"))
    bbox = draw.textbbox((0, 0), name, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_x = (card_size - title_w) / 2
    title_y = card_size * 0.05
    draw.text((title_x, title_y), name, fill="black", font=title_font)
    
    year = str(track.get("release_year", ""))
    draw.text(
        (card_size / 2, card_size / 2),
        year,
        fill="black",
        font=year_font,
        anchor="mm"  
    )

    artists = track.get("artists", "Unknown Artist")
    bbox = draw.textbbox((0, 0), artists, font=artists_font)
    artists_w = bbox[2] - bbox[0]  
    artists_x = (card_size - artists_w) / 2
    artists_y = card_size * 0.85
    draw.text((artists_x, artists_y), artists, fill="black", font=artists_font)

    return img


def generate_card_back(
        track: dict, card_size: int = 800, qr_ratio: float = 0.5, qr_border_ratio: float = 0.01,
        design_option: str = "simple"
        ) -> Image.Image:
    """
    Generate the back side of a song card.
    
    Args:
        track (dict): Track metadata dictionary
        card_size (int): Size of the card image (pixels)
        qr_ratio (float): Ratio of QR code size to card size
        qr_border_ratio (float): Ratio of QR code border size to card size
        design_option (str): Design option for the card back
    Returns:
        Image.Image: Generated card back image
    """
    # create base image
    img = Image.new("RGBA", (card_size, card_size), "black")

    # generate QR code
    spotify_uri = track.get("spotify_uri", "")
    qr_size = int(card_size * qr_ratio)
    qr_img = generate_qr_code(spotify_uri, size=qr_size, border=0)

    # add white border around QR code
    border_size = int(card_size * qr_border_ratio)
    qr_with_border = Image.new("RGBA", (qr_size + 2 * border_size, qr_size + 2 * border_size), "white")
    qr_with_border.paste(qr_img, (border_size, border_size))

    # paste QR code onto card back
    qr_x = (card_size - qr_with_border.width) // 2
    qr_y = (card_size - qr_with_border.height) // 2
    img.paste(qr_with_border, (qr_x, qr_y))

    return img


def generate_and_save_cards_for_track(
        track: dict, output_dir: Path, design_option: str = "simple"
        ) -> Tuple[Image.Image, Image.Image]:
    """
    Generate and save both front and back card images for a given track.
    
    Args:
        track (dict): Track metadata dictionary
        design_option (str): Design option for the cards
    Returns:
        Tuple[Image.Image, Image.Image]: Generated card front and back images
    """
    year = track["release_year"]
    cleaned_name = track["name_cleaned"]
    filename_base = f"{year}_{cleaned_name}".replace(" ", "_")
    
    front_img = generate_card_front(track, design_option=design_option)
    back_img = generate_card_back(track, design_option=design_option)

    save_card_image(front_img, output_dir, f"{filename_base}_front")
    save_card_image(back_img, output_dir, f"{filename_base}_back")
    
    return front_img, back_img


def generate_and_save_cards_for_playlist(
        tracks: list[dict], output_dir: Path, design_option: str = "simple"
        ) -> None:
    for track in tracks:
        generate_and_save_cards_for_track(track, output_dir, design_option)

    print(f"Generated cards saved to {output_dir}.")