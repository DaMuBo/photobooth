from flask import render_template, request, redirect, url_for, Blueprint

select_bp = Blueprint('select_bp', __name__)


@select_bp.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        selected_option = int(request.form.get('selected_option'))
        return redirect(url_for("result_bp.result", num_images=selected_option))
    return render_template('select.html')
