import logging
from flask import render_template, request, redirect, url_for, Blueprint

from src.frontend.routes import route_gst_pipes

select_bp = Blueprint("select_bp", __name__)

SUCCESS_REQUEST = 200

logger = logging.getLogger(__name__)


@select_bp.route("/select", methods=["GET", "POST"])
def select():
    """Select number of Images to make."""
    if request.method == "POST":
        selected_option = int(request.form.get("selected_option"))
        # start the gst pipeline here
        _response, status_code = route_gst_pipes.start_pipeline()
        if status_code != SUCCESS_REQUEST:
            route_gst_pipes.stop_pipeline()
            route_gst_pipes.start_pipeline()
            logger.error("Error in starting pipeline: %s", _response)

        return redirect(url_for("preview_bp.preview", num_images=selected_option))
    return render_template("select.html")
