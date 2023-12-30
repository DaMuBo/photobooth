import os
from pathlib import Path

from flask import render_template, Blueprint, request, redirect, url_for


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"
upload_folder = ROOT / "samples" / "layouts"

if not upload_folder.exists():
    upload_folder.mkdir(exist_ok=True)

config_bp = Blueprint('config_bp', __name__)


@config_bp.route('/config', methods=["GET", "POST"])
def config():
    if request.method == "POST":
        # Fileupload-Code hier einfügen
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                # Speichern Sie das hochgeladene Bild im Upload-Ordner
                photo.save(os.path.join(upload_folder, photo.filename))

    # Anzeige der hochgeladenen Dateien
    files = os.listdir(upload_folder)
    return render_template("config.html", files=files)


@config_bp.route('/config/delete/<filename>', methods=['GET'])
def delete_file(filename):
    file_path = os.path.join(upload_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('config_bp.config'))
