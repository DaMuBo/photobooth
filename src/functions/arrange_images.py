from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

CONST_IMAGE_THREE = 3

MAX_IMAGE_NUMBER = 4


def arrange_images(
    images: List[Image.Image],
    layout_image: Optional[Image.Image] = None,
    layout_text: Optional[str] = None,
    background_width: int = 1800,
    background_height: int = 1200,
    background_color: Tuple[int, int, int] = (255, 255, 255),
    padding: int = 40,
    bottom_margin: int = 80,
    text_color: Tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    """Arrange a list of images on a background with optional layout image and text.

    Args:
    ----
        images (List[Image.Image]): List of images to arrange.
        layout_image (Optional[Image.Image]): An optional image to overlay on the background.
        layout_text (Optional[str]): Optional text to add to the layout.
        background_width (int): Width of the background canvas.
        background_height (int): Height of the background canvas.
        background_color (Tuple[int, int, int]): Background color in RGB.
        padding (int): Padding between images and edges of the background.
        bottom_margin (int): Margin at the bottom of the background for text.
        text_color (Tuple[int, int, int]): Text color in RGB.

    Returns:
    -------
        Image.Image: The composed image with arranged images, layout, and text.

    """
    # Create the background canvas
    background = Image.new("RGB", (background_width, background_height), background_color)

    num_images = len(images)
    if num_images > MAX_IMAGE_NUMBER:
        errmsg = "Number of images exceeds allowed limit."
        raise ValueError(errmsg)

    # Determine the grid layout based on the number of images
    rows, cols = (2, 2) if num_images > 1 else (1, 1)

    # Calculate resized image size and offsets
    image_width = (background_width - (cols + 1) * padding) // cols
    image_height = (background_height - (rows + 1) * padding - bottom_margin) // rows

    for i, image in enumerate(images):
        # Calculate row and column indices
        row_idx = i // cols
        col_idx = i % cols

        # Calculate offsets based on resized image size and padding
        offset_x = col_idx * (image_width + padding) + padding
        offset_y = row_idx * (image_height + padding) + padding

        # Resize the image and paste it onto the background
        resized_image = resize_image(image, image_width, image_height)
        background.paste(resized_image, (offset_x, offset_y))

    # Insert the layout image
    if layout_image:
        layout_image = resize_and_rotate_layout_image(layout_image, background_width, background_height)
        background.paste(layout_image, (0, 0), layout_image)

    # Place the layout text
    if layout_text and num_images == CONST_IMAGE_THREE:
        draw = ImageDraw.Draw(background)
        font = ImageFont.load_default()  # Default font
        offset_text_x = background_width - (image_width // 1.5) - (padding * 2)
        offset_text_y = background_height - (image_height // 2) - padding - bottom_margin
        draw.text((offset_text_x, offset_text_y), layout_text, font=font, fill=text_color)

    return background


def resize_image(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """Scale the image to the new width and height while preserving the aspect ratio. Crop overlapping parts.

    Args:
    ----
        image (Image.Image): The image to resize.
        target_width (int): The target width.
        target_height (int): The target height.

    Returns:
    -------
        Image.Image: The resized and cropped image.

    """
    original_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if original_ratio > target_ratio:
        new_height = target_height
        new_width = int(target_height * original_ratio)
    else:
        new_width = target_width
        new_height = int(target_width / original_ratio)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    return resized_image.crop((left, top, right, bottom))


def resize_and_rotate_layout_image(
    layout_image: Image.Image, background_width: int, background_height: int
) -> Image.Image:
    """Resize and rotate the layout image to fit the background dimensions.

    Args:
    ----
        layout_image (Image.Image): The layout image to resize and rotate.
        background_width (int): The width of the background.
        background_height (int): The height of the background.

    Returns:
    -------
        Image.Image: The resized and rotated layout image.

    """
    width, height = layout_image.size
    if width < height:
        layout_image = layout_image.rotate(90, expand=True)
    layout_image = layout_image.resize((background_width, background_height))
    return layout_image.convert("RGBA")
