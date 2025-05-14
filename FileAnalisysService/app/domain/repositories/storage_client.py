from abc import ABC, abstractmethod
from uuid import UUID

class FileStorageClient(ABC):
    @abstractmethod
    def get_file(self, file_id: UUID) -> bytes:
        """Retrieve a file from storage using its ID."""
        ...