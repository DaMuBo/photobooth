from pathlib import Path

from flask import render_template, Blueprint, request, redirect, url_for


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"


print_bp = Blueprint('print_bp', __name__)


@print_bp.route('/printout', methods=["GET"])
def printout():
    print("printprintprint")

    return render_template("error.html")
    # return redirect(request.referrer or url_for('index'))
