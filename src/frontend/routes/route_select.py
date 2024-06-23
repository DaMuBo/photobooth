from flask import render_template, request, redirect, url_for, Blueprint, jsonify

from src.frontend.routes import route_gst_pipes

select_bp = Blueprint('select_bp', __name__)


@select_bp.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        selected_option = int(request.form.get('selected_option'))
        # start the gst pipeline here
        response, status_code = route_gst_pipes.start_pipeline()
        if status_code != 200:
            return jsonify(response), status_code

        return redirect(url_for("preview_bp.preview", num_images=selected_option))
    return render_template('select.html')
