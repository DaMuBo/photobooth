"""Start and Stop gst pipeline."""

import gi

gi.require_version('Gst', '1.0')

from gi.repository import Gst
import flask
from flask import Blueprint, jsonify
import time

app = flask.Flask(__name__)

gi.require_version('Gst', '1.0')

gst_pipe_bp = Blueprint('gst_pipe_bp', __name__)

# Initialisiere GStreamer
Gst.init(None)

# Globale Variable für die Pipeline
pipeline = None

@app.route('/start_pipeline', methods=['POST'])
def start_pipeline():
    global pipeline
    if pipeline is not None:
        return jsonify({"error": "Pipeline is already running"}), 400

    # Beispiel-Pipeline (hier muss deine spezifische Pipeline-Konfiguration rein)
    pipeline_description = "libcamerasrc ! video/x-raw,format=YUY2 ! queue ! videoconvert ! queue ! v4l2sink device=/dev/video1"

    pipeline = Gst.parse_launch(pipeline_description)
    pipeline.set_state(Gst.State.PLAYING)
    time.sleep(2)

    return jsonify({"status": "Pipeline started"}), 200

@gst_pipe_bp.route('/stop_pipeline', methods=['POST'])
def stop_pipeline():
    global pipeline
    if pipeline is None:
        return jsonify({"error": "No pipeline is running"}), 400

    pipeline.set_state(Gst.State.NULL)
    pipeline = None

    return jsonify({"status": "Pipeline stopped"}), 200

if __name__ == '__main__':
	start_pipeline()
