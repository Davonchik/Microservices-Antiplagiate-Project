from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.models import FileModel

class AbstractFileRepository(ABC):
    @abstractmethod
    def save(self, file: FileModel) -> FileModel:
        """Save a file to the repository."""
        pass

    @abstractmethod
    def get_by_id(self, file_id: UUID) -> FileModel:
        """Retrieve a file from the repository by its ID."""
        pass

    @abstractmethod
    def get_by_hash(self, file_hash: str) -> FileModel:
        """Retrieve a file from the repository by its hash."""
        pass

    @abstractmethod
    def delete(self, file_id: UUID) -> None:
        """Delete a file from the repository by its ID."""
        pass