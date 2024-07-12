from pathlib import Path

from flask import render_template, Blueprint
from src.functions import printout


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"


print_bp = Blueprint("print_bp", __name__)


@print_bp.route("/printout", methods=["GET"])
def printing():
    """Print the created img."""
    printout.print_image_cups(static / "test_img_2.jpg", "Canon_SELPHY_CP1500")

    return render_template("printing.html")
