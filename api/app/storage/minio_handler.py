import io
from minio import Minio
from app.storage.base import StorageHandler

class MinioStorageHandler(StorageHandler):
    def __init__(self, bucket: str, client: Minio):
        self.bucket = bucket
        self.client = client

    def save(self, filename: str, data: bytes) -> None:
        self.client.put_object(
            self.bucket,
            filename,
            data = io.BytesIO(data),
            length = len(data),
            content_type=None
        )