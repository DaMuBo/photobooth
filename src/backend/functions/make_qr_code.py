from pathlib import Path

import segno


def make_qr_code(link: Path) -> str:
    """

    :param link:
    :return: string base64 encoded png of qr code
    """
    code = segno.make_qr(str(link)).png_data_uri(scale=10)
    return code
