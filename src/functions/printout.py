import os
import tempfile
import pathlib

import cups


def print_image_cups(image_path: pathlib.Path, printer_name: str = 'your_printer_name') -> bool:
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

    # Drucke das Bild
    job_id = conn.printFile(printer_name, str(image_path), "Python Image", {})
    if job_id is not None:
        return 200
    else:
        return 500
