import os
from pathlib import Path

from flask import render_template, request, redirect, url_for, Blueprint
from PIL import Image
from src.functions.arrange_images import arrange_images
from src.functions.get_layout import get_layout_random_numeric


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"


result_bp = Blueprint('result_bp', __name__)


@result_bp.route('/result/<int:num_images>', methods=['GET', 'POST'])
def result(num_images):
    if request.method == 'POST':
        return redirect(url_for("qr_code_bp.qr_code"))

    result_image_path = ROOT / "samples" / "test_img.jpg"

    layout_img = get_layout_random_numeric(ROOT / "samples" / "layouts", num_images)
    layout_text = os.getenv("LAYOUT_TEXT", None)
    list_image_path = []
    for i in range(num_images):
        list_image_path.append(Image.open(result_image_path))
    result_image = arrange_images(list_image_path,
                                  layout_image=layout_img,
                                  layout_text=layout_text
                                  )
    result_image = result_image.resize((800, 600))
    save_path = static / "test_img_2.jpg"
    result_image.save(str(save_path))

    return render_template('result.html',  result_image_path=str(save_path))
