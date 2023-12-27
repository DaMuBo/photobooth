import time
import os

from flask import Flask, render_template, request, redirect, url_for, Response


# Verzeichnis für gespeicherte Bilder erstellen, wenn es nicht existiert
if not os.path.exists('static/images'):
    os.makedirs('static/images')

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
        return redirect(url_for('preview', num_images=selected_option))
    return render_template('select.html')


@app.route('/preview/<int:num_images>')
def preview(num_images):
    return render_template('preview.html', num_images=num_images)


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
