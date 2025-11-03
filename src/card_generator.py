# src/card_generator.py
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from random import choice
import textwrap
from typing import Tuple

from config import resolve_asset_path
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


def draw_wrapped_text(draw, text, font, max_width, center_x, center_y, fill):
    """
    Draw wrapped, centered text on an image.
    The entire text block (all lines) is centered around (center_x, center_y).
    """
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    line_height = font.size * 1.2
    total_height = line_height * len(lines)

    y = center_y - total_height / 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = center_x - line_width / 2  # center each line horizontally
        draw.text((x, y), line, fill=fill, font=font)
        y += line_height


def generate_card_front(
        track: dict, design: dict, card_size: int = 800
        ) -> Image.Image:
    """
    Generate the front side of a song card.
    
    Args:
        track (dict): Track metadata dictionary
        design (dict): Design configuration for the card front
        card_size (int): Size of the card image (pixels)
    Returns:
        Image.Image: Generated card front image
    """
    # get design values
    design = design.get("front", {})
    background_color = choice(design.get("background_color", ["#FFFFFF"]))
    bg_image_path = resolve_asset_path(design.get("background_images"))
    font_color = choice(design.get("font_color", ["#000000"]))
    font_path = design.get("font")
    font = resolve_asset_path(font_path) if font_path else None

    # create base image
    img = Image.new("RGBA", (card_size, card_size), background_color)
    draw = ImageDraw.Draw(img)

    # add background image (optional)
    if bg_image_path:
        try:
            if bg_image_path.is_dir():
                bg_images = list(bg_image_path.glob("*"))
                bg_image_path = choice(bg_images)
            bg_img = Image.open(bg_image_path).convert("RGBA")
            bg_img = bg_img.resize((card_size, card_size))
            img.alpha_composite(bg_img)
        except Exception as e:
            print(f"Warning: could not load background image '{bg_image_path}': {e}")

    # load fonts
    title_size = int(card_size * 0.08)
    year_size = int(card_size * 0.3)
    artists_size = int(card_size * 0.08) if len(track.get("artists", "")) < 30 else int(card_size * 0.06)
    try:
        title_font = ImageFont.truetype(font, size=title_size)
        year_font = ImageFont.truetype(font, size=year_size)
        artists_font = ImageFont.truetype(font, size=artists_size)
    except:
        title_font = ImageFont.load_default(size=title_size)
        year_font = ImageFont.load_default(size=year_size)
        artists_font = ImageFont.load_default(size=artists_size)
        print("Warning: could not load specified font, using default font.")

    # draw text elements
    name = track.get("name_cleaned", track.get("name_original", "Unknown Title"))
    max_text_width = card_size * 0.9
    center_x = card_size / 2
    center_y = card_size * 0.15
    draw_wrapped_text(draw, name, title_font, max_text_width, center_x, center_y, fill=font_color)
    
    year = str(track.get("release_year", ""))
    draw.text(
        (card_size / 2, card_size / 2),
        year,
        fill=font_color,
        font=year_font,
        anchor="mm"  
    )

    artists = track.get("artists", "Unknown Artist")
    center_y = card_size * 0.85
    draw_wrapped_text(draw, artists, artists_font, max_text_width, center_x, center_y, fill=font_color)

    return img


def generate_card_back(
        track: dict, design: dict, card_size: int = 800, qr_ratio: float = 0.5, qr_border_ratio: float = 0.01,
        ) -> Image.Image:
    """
    Generate the back side of a song card.
    
    Args:
        track (dict): Track metadata dictionary
        design (dict): Design configuration for the card back
        card_size (int): Size of the card image (pixels)
        qr_ratio (float): Ratio of QR code size to card size
        qr_border_ratio (float): Ratio of QR code border size to card size
    Returns:
        Image.Image: Generated card back image
    """
    # get design values
    design = design.get("back", {})
    background_color = choice(design.get("background_color", ["#000000"]))
    border_color = design.get("border_color", "#FFFFFF")
    qr_bg_image_path = resolve_asset_path(design.get("qr_background_image"))
    qr_icon_path = resolve_asset_path(design.get("qr_center_icon"))

    # create base image
    img = Image.new("RGBA", (card_size, card_size), background_color)

    # add QR background image (optional)
    if qr_bg_image_path:
        try:
            bg_img = Image.open(qr_bg_image_path).convert("RGBA")
            bg_img = bg_img.resize((card_size, card_size))
            img.alpha_composite(bg_img)
        except Exception as e:
            print(f"Warning: could not load background image '{qr_bg_image_path}': {e}")

    # generate QR code
    spotify_uri = track.get("spotify_uri", "")
    qr_size = int(card_size * qr_ratio)
    qr_img = generate_qr_code(spotify_uri, size=qr_size, border=0)

    # add white border around QR code
    border_size = int(card_size * qr_border_ratio)
    qr_with_border = Image.new("RGBA", (qr_size + 2 * border_size, qr_size + 2 * border_size), border_color)
    qr_with_border.paste(qr_img, (border_size, border_size))

    # paste QR code onto card back
    qr_x = (card_size - qr_with_border.width) // 2
    qr_y = (card_size - qr_with_border.height) // 2
    img.paste(qr_with_border, (qr_x, qr_y))

    # add center icon to QR code (optional)
    if qr_icon_path:
        try:
            icon_img = Image.open(qr_icon_path).convert("RGBA")
            icon_size = int(qr_size * 0.25)
            icon_img = icon_img.resize((icon_size, icon_size))
            icon_x = qr_x + (qr_with_border.width - icon_size) // 2
            icon_y = qr_y + (qr_with_border.height - icon_size) // 2
            img.paste(icon_img, (icon_x, icon_y), icon_img)
        except Exception as e:
            print(f"Warning: could not load QR center icon '{qr_icon_path}': {e}")

    return img


def generate_and_save_cards_for_track(
        track: dict, output_dir: Path, design: dict,
        ) -> Tuple[Image.Image, Image.Image]:
    """
    Generate and save both front and back card images for a given track.
    
    Args:
        track (dict): Track metadata dictionary
        output_dir (Path): Directory to save the generated card images
        design (dict): Design configuration for the card
    Returns:
        Tuple[Image.Image, Image.Image]: Generated card front and back images
    """
    year = track["release_year"]
    cleaned_name = track["name_cleaned"]
    filename_base = f"{year}_{cleaned_name}".replace(" ", "_")
    
    front_img = generate_card_front(track, design=design)
    back_img = generate_card_back(track, design=design)

    save_card_image(front_img, output_dir, f"{filename_base}_front")
    save_card_image(back_img, output_dir, f"{filename_base}_back")
    
    return front_img, back_img


def generate_and_save_cards_for_playlist(
        tracks: list[dict], output_dir: Path, design: dict,
        ) -> None:
    for track in tracks:
        generate_and_save_cards_for_track(track, output_dir, design)

    print(f"Generated cards saved to {output_dir}.")