import pathlib

import PIL

from src.functions import arrange_images

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def integrate_arrange_images():
    """Test the arrange images function. - just a dummy."""
    images = []
    for i in range(4):
        # load the image 1
        images.append(PIL.Image.open(ROOT / "temp" / f"image_{i}.png"))

        # execute arrange images with 1 image
        result = arrange_images.arrange_images(images)

        # save created image
        result.save(str(ROOT / f"result_image_{i}.png"))


if __name__ == "__main__":
    integrate_arrange_images()
