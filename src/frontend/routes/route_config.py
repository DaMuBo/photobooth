import os
from pathlib import Path

from flask import render_template, Blueprint, request, redirect, url_for


ROOT = Path(__file__).resolve().parent.parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"
upload_folder = ROOT / "samples"
layout_dir = upload_folder / "layouts"
text_dir = upload_folder / "texts"

if not layout_dir.exists():
    layout_dir.mkdir(exist_ok=True)
if not text_dir.exists():
    text_dir.mkdir(exist_ok=True)

layout_text_path = text_dir / "layout_text.txt"
welcome_header_path = text_dir / "welcome_header.txt"
welcome_text_path = text_dir / "welcome_text.txt"


config_bp = Blueprint("config_bp", __name__)


@config_bp.route("/config", methods=["GET", "POST"])
def config():
    """Show config to user."""
    if request.method == "POST":
        # Fileupload-Code hier einfügen
        if "upload_button" in request.form:
            if "photo" in request.files:
                photo = request.files["photo"]
                if photo.filename != "":
                    # Speichern Sie das hochgeladene Bild im Upload-Ordner
                    photo.save(str(layout_dir / photo.filename))
        elif "save_text_button" in request.form:
            layout_text = request.form.get("layout_text")
            with open(layout_text_path, "w") as text_file:
                text_file.write(layout_text)
            layout_text = request.form.get("welcome_header")
            with open(welcome_header_path, "w") as text_file:
                text_file.write(layout_text)
            layout_text = request.form.get("welcome_text")
            with open(welcome_text_path, "w") as text_file:
                text_file.write(layout_text)

    # Anzeige der hochgeladenen Dateien
    files = os.listdir(layout_dir)
    config_files = [layout_text_path, welcome_header_path, welcome_text_path]
    results = []
    for file in config_files:
        if file.exists():
            with open(file, "r") as text_file:
                tmp = text_file.read()
        else:
            tmp = "Default text"
        results.append(tmp)
    return render_template(
        "config.html",
        files=files,
        layout_cfg_txt=results[0],
        welcome_header_cfg_txt=results[1],
        welcome_text_cfg_txt=results[2],
    )


@config_bp.route("/config/delete/<filename>", methods=["GET"])
def delete_file(filename: str):
    """Delete a file."""
    file_path = upload_folder / filename
    if file_path.exists():
        file_path.unlink()
    return redirect(url_for("config_bp.config"))
