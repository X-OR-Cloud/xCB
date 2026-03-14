"""
src/integrations/xor_storage.py — X-OR CLOUD (CEPH/S3) Client for xHR
"""
import aioboto3
import structlog
from botocore.exceptions import ClientError

from src.config import settings

log = structlog.get_logger(__name__)

class XORStorage:
    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket = settings.xor_bucket_name
        self.config = {
            "aws_access_key_id": settings.xor_access_key,
            "aws_secret_access_key": settings.xor_secret_key,
            "endpoint_url": settings.xor_endpoint_url,
        }

    async def upload_file(self, file_content: bytes, object_name: str, content_type: str = "application/pdf"):
        """Tải file lên CEPH Storage."""
        async with self.session.resource("s3", **self.config) as s3:
            try:
                obj = await s3.Object(self.bucket, object_name)
                await obj.put(Body=file_content, ContentType=content_type)
                log.info("xor_upload_success", bucket=self.bucket, object=object_name)
                return f"{settings.xor_endpoint_url}/{self.bucket}/{object_name}"
            except ClientError as exc:
                log.error("xor_upload_error", error=str(exc))
                raise

    async def download_file(self, object_name: str) -> bytes:
        """Tải file từ CEPH Storage về."""
        async with self.session.resource("s3", **self.config) as s3:
            try:
                obj = await s3.Object(self.bucket, object_name)
                resp = await obj.get()
                async with resp["Body"] as stream:
                    return await stream.read()
            except ClientError as exc:
                log.error("xor_download_error", error=str(exc))
                raise

    async def get_presigned_url(self, object_name: str, expiration: int = 3600):
        """Tạo link tạm thời để xem file."""
        async with self.session.client("s3", **self.config) as s3:
            try:
                url = await s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket, "Key": object_name},
                    ExpiresIn=expiration
                )
                return url
            except ClientError as exc:
                log.error("xor_presigned_url_error", error=str(exc))
                return None

storage = XORStorage()
