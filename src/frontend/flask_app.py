import time
import os

from flask import Flask, render_template, request, redirect, url_for, Response
from picamera import PiCamera


# Verzeichnis für gespeicherte Bilder erstellen, wenn es nicht existiert
if not os.path.exists('static/images'):
    os.makedirs('static/images')

app = Flask(__name__,  static_url_path='/static')
camera = PiCamera()


def generate():
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
        stream.seek(0)
        stream.truncate()


@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
        return redirect(url_for('preview', num_images=selected_option))
    return render_template('select.html')


@app.route('/preview/<int:num_images>')
def preview(num_images):
    return render_template('preview.html', num_images=num_images)


@app.route('/take_photo/<int:num_images>')
def take_photo(num_images):
    image_list = []
    for i in range(num_images):
        time.sleep(10)  # Warte 10 Sekunden
        image_name = f'image_{i + 1}.jpg'
        image_path = f'static/images/{image_name}'
        camera.capture(image_path)
        image_list.append(image_path)

    return render_template('result.html', image_list=image_list)


@app.route('/result')
def result():
    # Hier könntest du die Bilder arrangieren und das Ergebnis anzeigen
    return render_template('result.html')


@app.route('/qr_code')
def qr_code():
    # Hier könntest du den QR-Code anzeigen
    return render_template('qr_code.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
