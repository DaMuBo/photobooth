import os
from pathlib import Path

from flask import Flask, render_template

from dotenv import load_dotenv

from src.frontend.routes.route_select import select_bp
from src.frontend.routes.route_result import result_bp
from src.frontend.routes.route_qr_code import qr_code_bp
from src.frontend.routes.route_print import print_bp
from src.frontend.routes.route_config import config_bp
from src.frontend.routes.route_preview import preview_bp

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"
text_dir = ROOT / "samples" / "texts"

if not text_dir.exists():
    text_dir.mkdir(exist_ok=True)


# Verzeichnis für gespeicherte Bilder erstellen, wenn es nicht existiert
if not os.path.exists(str(static)):
    os.makedirs(str(static))

app = Flask(__name__,  static_url_path='/static')
app.register_blueprint(select_bp)
app.register_blueprint(result_bp)
app.register_blueprint(qr_code_bp)
app.register_blueprint(print_bp)
app.register_blueprint(config_bp)
app.register_blueprint(preview_bp)


@app.route('/')
def index():
    welcome_header_path = text_dir / "welcome_header.txt"
    welcome_text_path = text_dir / "welcome_text.txt"
    if welcome_header_path.exists():
        with open(welcome_header_path, "r") as file:
            welcome_header = file.read().replace("\\n", "\n")
    else:
        welcome_header = "Welcome on this Application"
    if welcome_text_path.exists():
        with open(welcome_text_path, "r") as file:
            welcome_text = file.read().replace("\\n", "\n")
    else:
        welcome_text = "Start on Buzzer"
    return render_template('index.html', welcome_header=welcome_header,
                           welcome_text=welcome_text)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
