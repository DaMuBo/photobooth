import io
import time
import picamera


def capture_image():
    # Initialisieren Sie die Kamera
    with picamera.PiCamera() as camera:
        # Legen Sie die Auflösung fest (Sie können dies nach Bedarf ändern)
        camera.resolution = (1024, 768)

        # Warten Sie, bis die Kamera bereit ist
        time.sleep(2)

        # Bild in einen Bytes-Buffer aufnehmen
        image_stream = io.BytesIO()
        camera.capture(image_stream, format='jpeg')

    # Bytes-Buffer zurücksetzen, um von Anfang an zu lesen
    image_stream.seek(0)

    # Das Bild als Bytes zurückgeben
    return image_stream.read()
