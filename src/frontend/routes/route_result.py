import os
from pathlib import Path


from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from PIL import Image

from src.frontend.routes import route_gst_pipes

from src.functions.arrange_images import arrange_images
from src.functions.get_layout import get_layout_random_numeric


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"

SUCCESS_REQUEST = 200

result_bp = Blueprint("result_bp", __name__)


@result_bp.route("/result/<int:num_images>", methods=["GET", "POST"])
def result(num_images):
    """Show the result to users."""
    if request.method == "POST":
        return redirect(url_for("qr_code_bp.qr_code"))

    response, status_code = route_gst_pipes.stop_pipeline()
    if status_code != SUCCESS_REQUEST:
        return jsonify(response), status_code

    layout_img = get_layout_random_numeric(ROOT / "samples" / "layouts", num_images)
    text_file = ROOT / "samples" / "texts" / "config_text.txt"
    layout_text = os.getenv("LAYOUT_TEXT", None)
    if text_file.exists():
        with open(ROOT / "samples" / "texts" / "layout_text.txt", "r", encoding="utf-8") as file:
            layout_text = file.read().replace("\\n", "\n")
    list_image_path = []
    for i in range(num_images):
        list_image_path.append(Image.open(ROOT / "temp" / f"image_{i}.png"))
    result_image = arrange_images(list_image_path, layout_image=layout_img, layout_text=layout_text)
    save_path = static / "test_img_2.jpg"
    result_image.save(str(save_path))

    return render_template("result.html", result_image_path=str(save_path))
