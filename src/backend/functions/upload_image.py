import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(file_path, bucket_name, object_name):
    """
    Uploads a file to an S3 bucket and returns the download link.

    Parameters:
    - file_path (str): The local path to the file to be uploaded.
    - bucket_name (str): The name of the S3 bucket.
    - object_name (str): The object name (key) in the S3 bucket.

    Returns:
    - download_link (str): The URL for downloading the uploaded file.
    """

    # Set up the S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(file_path, bucket_name, object_name)

        # Generate a pre-signed URL for the uploaded file
        download_link = s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name,
                                                          'Key': object_name},
                                                  ExpiresIn=42*3600)  # Link expires in 42 hours

        return download_link

    except NoCredentialsError:
        print("Credentials not available")
        return None
