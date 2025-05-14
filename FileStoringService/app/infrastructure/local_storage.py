from app.domain.ports.file_storage import AbstractFileStorage
from app.domain.exceptions import FileNotFoundException
from uuid import UUID
import os
from pathlib import Path

class LocalFileStorage(AbstractFileStorage):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def save(self, file_id: UUID, content: bytes) -> str:
        """Save file to the local storage."""
        file_path = self.base_path / f"{file_id}.txt"
        with open(file_path, 'wb') as file:
            file.write(content)
        return str(file_path)

    def load(self, location: str) -> bytes:
        """Load a file from the local storage by its ID."""
        path = Path(location)
        if not path.exists():
            raise FileNotFoundException
        return path.read_bytes()

    def delete(self, location: str) -> None:
        """Delete a file from the local storage by its ID."""
        path = Path(location)
        if path.exists():
            path.unlink()