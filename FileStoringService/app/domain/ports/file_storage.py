from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.models import FileModel

class AbstractFileStorage(ABC):
    @abstractmethod
    def save(self, file_id: UUID, content: bytes) -> str:
        """Save file to the storage service."""
        pass

    @abstractmethod
    def load(self, location: str) -> bytes:
        """Load a file from the storage service by its ID."""
        pass

    @abstractmethod
    def delete(self, location: str) -> None:
        """Delete a file from the storage service by its ID."""
        pass