import os
from pathlib import Path
import datetime

from dotenv import load_dotenv

from flask import render_template, Blueprint
from src.functions.upload_image import upload_to_s3
from src.functions.make_qr_code import make_qr_code

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"


qr_code_bp = Blueprint("qr_code_bp", __name__)


@qr_code_bp.route("/qr_code", methods=["GET"])
def qr_code():
    """Show the QR Code to the users."""
    filename = static / "test_img_2.jpg"
    dtobj = datetime.datetime.now()
    image_date = f"{dtobj.year}{dtobj.month}{dtobj.day}_{dtobj.hour}{dtobj.minute}{dtobj.second}"
    new_filename = image_date + "img.jpg"
    download_url = upload_to_s3(filename, os.getenv("S3_BUCKET_NAME"), new_filename)
    qr_img = make_qr_code(download_url)
    return render_template("qr_code.html", qr_code_data_uri=qr_img)
