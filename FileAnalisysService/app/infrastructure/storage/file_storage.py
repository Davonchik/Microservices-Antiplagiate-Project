from app.domain.repositories.storage_client import FileStorageClient
from uuid import UUID
import os
from pathlib import Path

class LocalFileStorage(FileStorageClient):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def get_file(self, file_id: UUID) -> bytes:
        """Retrieve a file from local storage using its ID."""
        file_path = self.base_path / f"{file_id}.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_id} not found in local storage.")
        return file_path.read_bytes()