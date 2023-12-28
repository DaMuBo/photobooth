import os
import tempfile

import cups
from PIL import Image


def print_image_cups(image: Image.Image, printer_name: str = 'your_printer_name') -> bool:
    """
    printing an image with printer and returning True after done
    :param image_path:
    :param printer_name:
    :return:
    """
    conn = cups.Connection()
    printers = conn.getPrinters()

    # Überprüfe, ob der Drucker vorhanden ist
    if printer_name not in printers:
        raise ValueError(f"Drucker '{printer_name}' nicht gefunden.")

    # Erstelle eine temporäre Datei und speichere das Bild
    temp_file_path = tempfile.mktemp(suffix='.png')
    image.save(temp_file_path, format='PNG')
    try:
        # Drucke das Bild
        job_id = conn.printFile(printer_name, temp_file_path, "Python Image", {})
        if job_id is not None:
            return True
        else:
            print("Fehler beim Drucken. Überprüfen Sie den Druckerstatus.")
            return False
    finally:
        os.remove(temp_file_path)

