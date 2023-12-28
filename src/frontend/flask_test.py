import os
from pathlib import Path

from flask import Flask, render_template

from src.frontend.routes.route_select import select_bp
from src.frontend.routes.route_result import result_bp
from src.frontend.routes.route_qr_code import qr_code_bp


ROOT = Path(__file__).resolve().parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"

# Verzeichnis für gespeicherte Bilder erstellen, wenn es nicht existiert
if not os.path.exists(str(static)):
    os.makedirs(str(static))

app = Flask(__name__,  static_url_path='/static')
app.register_blueprint(select_bp)
app.register_blueprint(result_bp)
app.register_blueprint(qr_code_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/preview/<int:num_images>')
def preview(num_images):
    return render_template('preview.html', num_images=num_images)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
