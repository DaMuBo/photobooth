import os
import logging

import boto3
from botocore.exceptions import NoCredentialsError

from src.functions import settings

logger = logging.getLogger(__name__)


def upload_to_s3(setting: settings.Settings, file_path, object_name):
    """Upload a file to an S3 bucket and returns the download link."""
    region = setting.get_setting("AWS_DEFAULT_REGION")
    bucket_name = setting.get_setting("S3_BUCKET_NAME")

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
