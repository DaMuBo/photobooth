import os
import logging

import boto3
from botocore.exceptions import NoCredentialsError

logger = logging.getLogger(__name__)


def upload_to_s3(file_path, bucket_name, object_name):
    """Upload a file to an S3 bucket and returns the download link."""
    region = os.getenv("AWS_DEFAULT_REGION")

    # Set up the S3 client
    s3 = boto3.client("s3", region_name=region, endpoint_url=f"https://s3.{region}.amazonaws.com")

    try:
        # Upload the file
        s3.upload_file(file_path, bucket_name, object_name)

        # Generate a pre-signed URL for the uploaded file
        download_link = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=3600,  # Gültigkeitsdauer der URL in Sekunden
        )

        return download_link

    except NoCredentialsError:
        logger.error("Credentials not available")
        return None
