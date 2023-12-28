import time
import os
from pathlib import Path
import datetime

from flask import Flask, render_template, request, redirect, url_for, Response
from PIL import Image
from src.backend.functions.arrange_images import arrange_images
from src.backend.functions.upload_image import upload_to_s3
from src.backend.functions.make_qr_code import make_qr_code
from src.backend.functions.get_layout import get_layout_random_numeric


ROOT = Path(__file__).resolve().parent.parent.parent
static = ROOT / "src" / "frontend" / "static" / "images"

# Verzeichnis für gespeicherte Bilder erstellen, wenn es nicht existiert
if not os.path.exists(str(static)):
    os.makedirs(str(static))

app = Flask(__name__,  static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/select', methods=['GET', 'POST'])
def select():
    # Hier könntest du die Auswahl der Anzahl der Bilder implementieren
    if request.method == 'POST':
        selected_option = int(request.form.get('selected_option'))
        # Hier könnten Sie die Logik implementieren, um die Auswahl zu verarbeiten
        # und die erforderlichen Daten für die Preview-Seite vorzubereiten.
        return redirect(url_for("result", num_images=selected_option))
        # return redirect(url_for('preview', num_images=selected_option))
    return render_template('select.html')


@app.route('/preview/<int:num_images>')
def preview(num_images):
    return render_template('preview.html', num_images=num_images)


@app.route('/result/<int:num_images>',methods=['GET', 'POST'])
def result(num_images):
    save_path = static / "test_img_2.jpg"
    if request.method == 'POST':
        selected_option = str(request.form.get('upload-print'))
        return redirect(url_for("qr_code", filename=str(save_path)))

    # Hier könntest du die Bilder arrangieren und das Ergebnis anzeigen
    result_image_path = Path(__file__).resolve().parent.parent.parent / "samples" / "test_img.jpg"

    # get your layout
    layout_img = get_layout_random_numeric(ROOT / "samples" / "layouts", num_images)
    layout_text = os.getenv("LAYOUT_TEXT", None)
    list_image_path = []
    for i in range(num_images):
        list_image_path.append(Image.open(result_image_path))
    result_image = arrange_images(list_image_path,
                                  layout_image=layout_img,
                                  layout_text=layout_text
                                  )
    result_image = result_image.resize((800, 600))
    save_path = static / "test_img_2.jpg"
    result_image.save(str(save_path))

    return render_template('result.html',  result_image_path=str(save_path))


@app.route('/qr_code/<filename>', methods=["GET"])
def qr_code(filename):
    # upload the image to the s3 bucket
    print(filename)
    dtobj = datetime.datetime.now()
    image_date = f"{dtobj.year}{dtobj.month}{dtobj.day}_{dtobj.hour}{dtobj.minute}{dtobj.second}"
    new_filename = image_date + "img.jpg"
    download_url = upload_to_s3(filename,
                                os.getenv("S3_BUCKET_NAME"),
                                new_filename)
    qr_img = make_qr_code(download_url)
    # Hier könntest du den QR-Code anzeigen
    return render_template('qr_code.html', qr_code_data_uri=qr_img)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
