import unittest
from unittest.mock import MagicMock, patch

from botocore.exceptions import NoCredentialsError

from src.functions.upload_image import upload_to_s3


class TestUploadToS3(unittest.TestCase):
    def setUp(self):
        # Mocking boto3.client
        self.s3_client_mock = MagicMock()
        patcher = patch('src.backend.functions.upload_image.boto3.client',
                        return_value=self.s3_client_mock)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_upload_to_s3_success(self):
        # Arrange
        file_path = 'local/path/to/file.txt'
        bucket_name = 'your_bucket'
        object_name = 'your_object_key'

        # Act
        download_link = upload_to_s3(file_path, bucket_name, object_name)

        # Assert
        self.assertIsNotNone(download_link)
        self.s3_client_mock.upload_file.assert_called_once_with(file_path, bucket_name, object_name)
        self.s3_client_mock.generate_presigned_url.assert_called_once_with(
            'get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=42*3600
        )

    def test_upload_to_s3_no_credentials(self):
        # Arrange
        file_path = 'local/path/to/file.txt'
        bucket_name = 'your_bucket'
        object_name = 'your_object_key'
        self.s3_client_mock.upload_file.side_effect = NoCredentialsError()

        # Act
        download_link = upload_to_s3(file_path, bucket_name, object_name)

        # Assert
        self.assertIsNone(download_link)
        self.s3_client_mock.upload_file.assert_called_once_with(file_path, bucket_name, object_name)


if __name__ == '__main__':
    unittest.main()