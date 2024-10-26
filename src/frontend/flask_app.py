import pathlib
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from dotenv import load_dotenv

from src.functions import settings

from src.frontend.routes.route_select import select_bp
from src.frontend.routes.route_result import result_bp
from src.frontend.routes.route_qr_code import qr_code_bp
from src.frontend.routes.route_print import print_bp
from src.frontend.routes.route_config import config_bp
from src.frontend.routes.route_preview import preview_bp
from src.frontend.routes.route_gst_pipes import gst_pipe_bp
from src.frontend.routes.route_setup_wifi import wifi_bp

setting = settings.Settings()

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"
text_dir = ROOT / "samples" / "texts"

if not text_dir.exists():
    text_dir.mkdir(exist_ok=True)

if not static.exists():
    static.mkdir(parents=True)


app = Flask(__name__)

if not app.debug:
    app.logger.setLevel(logging.INFO)

app.logger.info('Flask app startup')

app.register_blueprint(select_bp)
app.register_blueprint(result_bp)
app.register_blueprint(qr_code_bp)
app.register_blueprint(print_bp)
app.register_blueprint(config_bp)
app.register_blueprint(preview_bp)
app.register_blueprint(gst_pipe_bp)
app.register_blueprint(wifi_bp)

@app.route("/")
def index():
    """Route to Main Page."""
    welcome_header = setting.get_setting("welcome_main_text")
    welcome_text = setting.get_setting("welcome_sub_text")
    return render_template("index.html", welcome_header=welcome_header, welcome_text=welcome_text)


def main():
    """Run the app."""
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
