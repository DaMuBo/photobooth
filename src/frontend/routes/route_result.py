import os
from pathlib import Path

import threading

from flask import render_template, request, redirect, url_for, Blueprint
from PIL import Image
from src.functions.arrange_images import arrange_images
from src.functions.get_layout import get_layout_random_numeric
# from src.functions.printout import print_image_cups # only for test on linux


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"


result_bp = Blueprint('result_bp', __name__)


@result_bp.route('/result/<int:num_images>', methods=['GET', 'POST'])
def result(num_images):
    result_image_path = ROOT / "samples" / "test_img.jpg"
    if request.method == 'POST':
        image = Image.open(result_image_path)
        # print_image_cups(image, os.getenv("PRINTER_NAME"))
        return redirect(url_for("qr_code_bp.qr_code"))

    layout_img = get_layout_random_numeric(ROOT / "samples" / "layouts", num_images)
    layout_text = os.getenv("LAYOUT_TEXT", None)
    list_image_path = []
    for i in range(num_images):
        list_image_path.append(Image.open(result_image_path))
    result_image = arrange_images(list_image_path,
                                  layout_image=layout_img,
                                  layout_text=layout_text
                                  )
    save_path = static / "test_img_2.jpg"
    result_image.save(str(save_path))

    return render_template('result.html',  result_image_path=str(save_path))
