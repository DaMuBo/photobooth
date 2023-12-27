import unittest
from pathlib import Path
import base64
from src.backend.functions.make_qr_code import make_qr_code


class TestMakeQRCode(unittest.TestCase):

    def test_make_qr_code_returns_string(self):
        link = Path("https://example.com")
        result = make_qr_code(link)
        self.assertIsInstance(result, str)

    def test_make_qr_code_returns_base64_encoded_png(self):
        link = Path("https://example.com")
        result = make_qr_code(link)

        # Check if the result is a valid base64 encoded string
        try:
            decoded = base64.b64decode(result.split(',')[1])
            self.assertTrue(isinstance(decoded, bytes))
        except Exception as e:
            self.fail(f"Result is not a valid base64 encoded string: {e}")


if __name__ == '__main__':
    unittest.main()
