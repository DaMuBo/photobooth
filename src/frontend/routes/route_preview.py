"""
The route for making the picamera stuff -> still open to do
"""

import time
import io

from flask import Blueprint, render_template
from picamera import PiCamera

from PIL import Image

from src.functions.arrange_images import arrange_images

preview_bp = Blueprint('preview_bp', __name__)
camera = PiCamera()


@preview_bp.route('/preview/<int:num_images>')
def preview(num_images):
    return render_template('preview.html', num_images=num_images)


@preview_bp.route('/take_photo/<int:num_images>')
def take_photo(num_images):
    image_list = []
    for i in range(num_images):
        time.sleep(10)  # Warte 10 Sekunden
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg', use_video_port=True)
        image_data = stream.getvalue()
        stream.seek(0)
        stream.truncate()
        image_list.append(image_data)

    try:
        pillow_images = [Image.open(io.BytesIO(image)) for image in image_list]
        result_image: Image.Image = arrange_images(pillow_images)
        result_image_path = "tempo.jpeg"
        result_image.save(result_image_path)

    except Exception as e:
        return render_template('error.html', error_message=str(e))

    return render_template('result.html', result_image_path=result_image_path)
