from pathlib import Path
from random import choice
import logging

logger = logging.getLogger(__name__)

from PIL import Image


def get_layout_random(layout_path: Path) -> Image.Image:
    """Get a random Layout."""
    files = [
        file
        for file in layout_path.iterdir()
        if file.is_file() and file.suffix in [".png", ".jpg", ".jpeg"] and "general" in file.name
    ]
    if len(files) > 0:
        file = choice(files)
    else:
        logger.warn("No layout file found. Returning None")
        return None
    return Image.open(str(file))


def get_layout_random_numeric(layout_path: Path, number_layout: int = 1) -> Image.Image:
    """Get a random layout."""
    files = [
        file
        for file in layout_path.iterdir()
        if file.is_file() and file.suffix in [".png", ".jpg", ".jpeg"] and str(number_layout) in file.name
    ]
    if len(files) == 0:
        image = get_layout_random(layout_path)
        return image
    file = choice(files)

    return Image.open(str(file))
