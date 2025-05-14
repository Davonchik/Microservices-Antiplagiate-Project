from abc import ABC, abstractmethod
from app.domain.entities.models import FileAnalysisModel
from uuid import UUID

class FileAnalysisRepository(ABC):
    @abstractmethod
    def save(self, analysis: FileAnalysisModel) -> None:
        """Save the file analysis result."""
        ...
    
    @abstractmethod
    def get_by_id(self, file_id: UUID) -> FileAnalysisModel:
        """Get the file analysis result by file ID."""
        ...

    @abstractmethod
    def find_by_hash(self, content_hash: str) -> FileAnalysisModel:
        """Find the file analysis result by content hash."""
        ...