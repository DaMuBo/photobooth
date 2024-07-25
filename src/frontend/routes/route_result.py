import os
from pathlib import Path


from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from PIL import Image

from src.frontend.routes import route_gst_pipes

from src.functions.arrange_images import arrange_images
from src.functions.get_layout import get_layout_random_numeric
from src.functions import settings

setting = settings.Settings()


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"

SUCCESS_REQUEST = 200

result_bp = Blueprint("result_bp", __name__)


@result_bp.route("/result/<int:num_images>", methods=["GET", "POST"])
def result(num_images):
    """Show the result to users."""
    save_path = static / "test_img_2.jpg"
    if request.method == "POST":
        return render_template("result.html", result_image_path=str(save_path))

    response, status_code = route_gst_pipes.stop_pipeline()
    if status_code != SUCCESS_REQUEST:
        return jsonify(response), status_code

    layout_img = get_layout_random_numeric(ROOT / "samples" / "layouts", num_images)
    layout_text = ""
    if num_images == 2:
        layout_text = setting.get_setting("layout_text_2")
    elif num_images == 3:
        layout_text = setting.get_setting("layout_text_3")
    list_image_path = []
    for i in range(num_images):
        list_image_path.append(Image.open(ROOT / "temp" / f"image_{i}.png"))
    result_image = arrange_images(list_image_path, layout_image=layout_img, layout_text=layout_text)
    result_image.save(str(save_path))

    return render_template("result.html", result_image_path=str(save_path))
