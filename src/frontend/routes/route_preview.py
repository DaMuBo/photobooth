"""
The route for making the picamera stuff -> still open to do
"""
import pathlib
import base64
from flask import Blueprint, render_template, redirect, url_for, request

preview_bp = Blueprint('preview_bp', __name__)

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent


@preview_bp.route('/preview/<int:num_images>')
def preview(num_images):
    return render_template('preview.html', num_images=num_images)


@preview_bp.route('/save_images', methods=['POST'])
def save_images():
    temp_path = ROOT / "temp"
    temp_path.mkdir(exist_ok=True)
    if 'image' in request.form:
        image_data = request.form['image']
        number = request.form['numInJavaScript']

        save_image(image_data, int(number))

    return redirect(url_for('preview_bp.nachste_seite',))


@preview_bp.route('/nachste_seite')
def nachste_seite():
    return "hi"
    # return redirect(url_for("result_bp.result", num_images=4))


def save_image(image_data, number: int):
    image_binary = base64.b64decode(image_data.split(',')[1])
    filename = ROOT / "temp" / f"image_{number}.png"
    with open(filename, 'wb') as f:
        f.write(image_binary)
