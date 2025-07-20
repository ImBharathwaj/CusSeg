from hdfs import InsecureClient
from app.storage.base import StorageHandler

class HDFSStorageHandler(StorageHandler):
    def __init__(self, base_path: str, client: InsecureClient):
        self.base_path = base_path
        self.client = client
    
    def save(self, filename: str, data: bytes) -> None:
        hdfs_path = f"{self.base_path}/{filename}"
        with self.client.write(hdfs_path, overwrite=True) as writer:
            writer.write(data)