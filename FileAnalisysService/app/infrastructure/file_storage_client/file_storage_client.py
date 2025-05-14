from app.domain.services.file_storage_client import FileStorageClient
from app.domain.exceptions.exceptions import FileNotFoundException
import requests
from uuid import UUID

class RemoteFileStorageClient(FileStorageClient):
    def __init__(self, base_url: str, path: str = "/files/download/"):
        self.path = path
        self.base_url = base_url.rstrip("/") + path

    def get_file(self, file_id: UUID) -> bytes:
        """Retrieve a file from remote storage using its ID."""
        response = requests.get(f"{self.base_url}{file_id}")
        if response.status_code != 200:
            raise FileNotFoundException
        return response.content