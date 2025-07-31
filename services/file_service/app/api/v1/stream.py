import os
from fastapi import APIRouter, HTTPException
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_REGION = os.getenv("S3_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")

session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    region_name=S3_REGION,
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

@router.get("/{slug}")
async def get_stream_url(slug: str):
    key = f"films/{slug}.mp4"
    try:
        s3_client.head_object(Bucket=S3_BUCKET, Key=key)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': key},
            ExpiresIn=3600  # 1 час
        )
        return {"video_url": url}
    except ClientError as e:
        raise HTTPException(status_code=404, detail="Video not found")
