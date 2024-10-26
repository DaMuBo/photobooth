from pathlib import Path

import logging
from flask import render_template, Blueprint, abort
from src.functions import printout
from src.functions import settings

logger = logging.getLogger("print_logger")

setting = settings.Settings()

ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"

print_bp = Blueprint("print_bp", __name__)

@print_bp.route("/printout", methods=["GET"])
def printing():
    """Print the created img."""
    setting.load_settings()
    save_path = static / "test_img_2.jpg"
    
    try:
        status_code = printout.print_image_cups(save_path, setting.get_setting("printer_name"))
        logger.info("LOG: print status code : %s", status_code)
        
        if status_code != 200:
            error_messages = {
                400: "Drucker nicht gefunden",
                500: "Unbekannter Fehler",
                501: "Papierstau",
                502: "Kein Papier",
                503: "Wenig Toner/Tinte",
                504: "Drucker-Neustart fehlgeschlagen",
                505: "Druckauftrag fehlgeschlagen"
            }
            error_message = error_messages.get(status_code, "Ein Fehler ist aufgetreten")
            return render_template("error_print.html", error_message=error_message), status_code
        
        return render_template("result.html", result_image_path=str(save_path))
    
    except Exception as e:
        return render_template("error_print.html", error_message=str(e)), 500


@print_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Seite nicht gefunden"), 404