from pathlib import Path

import segno


def make_qr_code(link: Path) -> str:
    """Make a qr code."""
    code = segno.make_qr(str(link)).png_data_uri(scale=5)
    return code
