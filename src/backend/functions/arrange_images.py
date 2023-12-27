from typing import List
from PIL import Image


def arrange_images(images: List[Image.Image],
                   layout_image: Image.Image = None,
                   background_width: int = 1800,
                   background_height: int = 1200,
                   background_color: tuple = (255, 255, 255),
                   padding: int = 40,
                   bottom_margin: int = 80) -> Image.Image:

    background = Image.new('RGB', (background_width, background_height), background_color)

    num_images = len(images)
    if num_images == 1:
        rows, cols = 1, 1
    elif num_images == 2:
        rows, cols = 1, 2
    elif num_images == 3:
        rows, cols = 2, 2
    elif num_images == 4:
        rows, cols = 2, 2
    else:
        raise ValueError("Number of images exceeds allowed limit.")

    # calculate resized image size and offsets
    image_width = int((background_width - (cols + 1) * padding) / cols)
    image_height = int((background_height - (rows + 1) * padding - bottom_margin) / rows)

    for i, image in enumerate(images):
        # calculate row and column indices
        row_idx = i // cols
        col_idx = i % cols

        # calculate offsets based on resized image size and padding
        offset_x = col_idx * (image_width + padding) + padding
        offset_y = row_idx * (image_height + padding) + padding

        # resize the image
        image = image.resize((image_width, image_height))

        # paste the resized image onto the background
        background.paste(image, (offset_x, offset_y))

    # insert the send layout
    if layout_image is not None:
        # get shape
        width, height = layout_image.size
        if width < height:
            layout_image = layout_image.rotate(90, expand=True)
        layout_image = layout_image.resize((background_width, background_height))
        background.paste(layout_image.convert(mode="RGBA"), mask=layout_image.convert("RGBA").split()[3])

    return background
