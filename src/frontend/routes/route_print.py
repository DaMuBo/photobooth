from pathlib import Path

from flask import render_template, Blueprint
from src.functions import printout
from src.functions import settings

setting = settings.Settings()



ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"


print_bp = Blueprint("print_bp", __name__)


@print_bp.route("/printout", methods=["GET"])
def printing():
    """Print the created img."""
    setting.load_settings()
    save_path = static / "test_img_2.jpg"
    printout.print_image_cups(save_path, setting.get_setting("printer_name"))

    return render_template("result.html", result_image_path=str(save_path))
