import unittest
from unittest.mock import MagicMock
from PIL import Image
from src.functions import print_image_cups


class TestPrintImageCups(unittest.TestCase):
    def setUp(self):
        # Erstellen Sie eine Mock-Verbindung für den Test
        self.mock_conn = MagicMock()

    def test_print_image_cups_success(self):
        # Mock-Printers für den Test
        self.mock_conn.getPrinters.return_value = {'your_printer_name': {}}

        # Mock-Image für den Test
        mock_image = MagicMock(spec=Image.Image)

        # Mock-PrintFile-Funktion
        def mock_print_file(printer_name, temp_file_path, job_name, options):
            self.assertEqual(printer_name, 'your_printer_name')
            self.assertTrue(temp_file_path.endswith('.png'))
            self.assertEqual(job_name, 'Python Image')
            self.assertDictEqual(options, {})
            return 1  # Simuliert einen erfolgreichen Druckjob

        self.mock_conn.printFile.side_effect = mock_print_file

        # Mock tempfile.mktemp
        with unittest.mock.patch('tempfile.mktemp', return_value='/tmp/mock_temp_file'):
            result = print_image_cups(mock_image, printer_name='your_printer_name')

        self.assertTrue(result)
        self.mock_conn.printFile.assert_called_once()

    def test_print_image_cups_printer_not_found(self):
        # Mock-Printers für den Test
        self.mock_conn.getPrinters.return_value = {'other_printer': {}}

        # Mock-Image für den Test
        mock_image = MagicMock(spec=Image.Image)

        with self.assertRaises(ValueError) as context:
            print_image_cups(mock_image, printer_name='your_printer_name')

        self.assertEqual(str(context.exception), "Drucker 'your_printer_name' nicht gefunden.")
        self.mock_conn.printFile.assert_not_called()


if __name__ == '__main__':
    unittest.main()
