import pathlib

from PIL import Image
from pyzbar import pyzbar

def read_qr_code(image_path: str | pathlib.Path) -> str:
    """Read an QR Code from a data"""
    image = Image.open(image_path)
    barcodes = pyzbar.decode(image)
    
    if barcodes:
        return barcodes[0].data.decode("utf-8")
    else:
        return "Kein QR Code gefunden."
