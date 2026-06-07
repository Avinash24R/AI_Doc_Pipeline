import boto3
import uuid
import tempfile

from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
    region_name= settings.AWS_REGION

)

def upload_file_s3(file):
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    s3_key = f"uploads/{unique_name}"

    s3_client.upload_fileobj(
        file.file,
        settings.AWS_BUCKET_NAME,
        s3_key
    )

    s3_url = (
        f"https://{settings.AWS_BUCKET_NAME}.s3."
        f"{settings.AWS_REGION}.amazonaws.com/{s3_key}"
    )

    return {
        "s3_key": s3_key,
        "s3_url": s3_url
    }
    
def download_file_s3(s3_key: str):
    tmp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )
    s3_client.download_file(
        settings.AWS_BUCKET_NAME,
        s3_key,
        tmp_file.name
    )

    return tmp_file.name
def delete_file_s3(s3_key: str):
    s3_client.delete_object(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=s3_key
    )