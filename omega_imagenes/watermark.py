from PIL import Image

def watermark(input_image, alpha_value):
    """
    Adds three semi-transparent logos in a vertical line through the center of the image,
    all the same size.
    Args:
        input_image (PIL.Image): The image to watermark.
        alpha_value (int): Alpha value for logo transparency (0-255).
    Returns:
        PIL.Image: The watermarked image.
    """
    logo_path = "assets/logotipo.png"
    logo = Image.open(logo_path).convert("RGBA")
    image = input_image.convert("RGBA")
    w, h = image.size

    # Size for all logos
    logo_height = int(h * 0.15)
    logo_aspect = logo.width / logo.height

    # Resize logo (keep aspect ratio)
    logo_resized = logo.resize((int(logo_height * logo_aspect), logo_height), Image.LANCZOS)

    # Adjust alpha channel for transparency
    if alpha_value < 255:
        # Split channels and apply new alpha
        r, g, b, a = logo_resized.split()
        a = a.point(lambda p: int(p * (alpha_value / 255)))
        logo_resized = Image.merge("RGBA", (r, g, b, a))

    # Y positions (equally spaced)
    total_logo_height = logo_resized.height * 3
    vertical_space = h - total_logo_height
    space_between = vertical_space // 4

    y_top = space_between
    y_center = y_top + logo_resized.height + space_between
    y_bottom = y_center + logo_resized.height + space_between

    # X position (centered)
    x_center = (w - logo_resized.width) // 2

    # Paste logos
    watermarked = image.copy()
    watermarked.paste(logo_resized, (x_center, y_top), logo_resized)
    watermarked.paste(logo_resized, (x_center, y_center), logo_resized)
    watermarked.paste(logo_resized, (x_center, y_bottom), logo_resized)

    return watermarked.convert(input_image.mode)