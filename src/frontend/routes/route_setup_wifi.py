from pathlib import Path
import logging

from flask import Blueprint, request, jsonify, render_template
from src.frontend.routes import route_gst_pipes
from src.functions import settings, setup_wifi

setting = settings.Settings()

logger = logging.getLogger(__name__)

SUCCESS_REQUEST = 200

ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"

wifi_bp = Blueprint("wifi_bp", __name__)

@wifi_bp.route('/barcode_scanner')
def barcode_scanner():

    _response, status_code = route_gst_pipes.start_pipeline()
    if status_code != SUCCESS_REQUEST:
        route_gst_pipes.stop_pipeline()
        route_gst_pipes.start_pipeline()
    return render_template('setup_wifi.html')

@wifi_bp.route("/setup-wifi", methods=["POST"])
def wifi():
    """Set the Wifi up."""
    barcode = request.json['barcode']
    print(barcode)
    setup_wifi.setup_wifi(barcode)
    return jsonify({'message': 'WLAN erfolgreich eingerichtet', "status": 200})
