import unittest
from PIL import Image
from src.functions.arrange_images import arrange_images


class TestArrangeImagesFunction(unittest.TestCase):

    def setUp(self):
        # Set up any common objects or data needed for the tests
        pass

    def tearDown(self):
        # Clean up after each test (if necessary)
        pass

    def test_arrange_images_single_image(self):
        # Test case for a single image
        image = Image.new('RGB', (100, 100), (255, 0, 0))
        result = arrange_images([image])
        # Add assertions to verify the correctness of the result
        self.assertEqual(result.size, (1800, 1200))  # Adjust these assertions based on your expectations

    def test_arrange_images_two_images(self):
        # Test case for two images
        image1 = Image.new('RGB', (100, 100), (255, 0, 0))
        image2 = Image.new('RGB', (100, 100), (0, 255, 0))
        result = arrange_images([image1, image2])
        # Add assertions to verify the correctness of the result
        self.assertEqual(result.size, (1800, 1200))

    def test_arrange_too_much_images_(self):
        image1 = Image.new('RGB', (100, 100), (255, 0, 0))
        image2 = Image.new('RGB', (100, 100), (0, 255, 0))

        with self.assertRaises(ValueError):
            arrange_images([image1, image2, image1, image2, image1])


if __name__ == '__main__':
    unittest.main()
