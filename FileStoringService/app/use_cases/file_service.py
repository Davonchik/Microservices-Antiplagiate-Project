from app.domain.models import FileModel
import hashlib
from uuid import uuid4, UUID
from datetime import datetime
from app.domain.ports.file_repository import AbstractFileRepository
from app.domain.ports.file_storage import AbstractFileStorage
from app.domain.exceptions import FileNotFoundException, FileAlreadyExistsException, InvalidFileFormatException

class FileService:
    def __init__(self, file_repository: AbstractFileRepository, file_storage: AbstractFileStorage, extensions: set = {".txt"}):
        self.extensions = extensions
        self.file_repository = file_repository
        self.file_storage = file_storage

    def check_on_antiplagiate(self, file_hash: str) -> None:
        """Check on antiplagiat (100%)."""
        existing_file = self.file_repository.get_by_hash(file_hash)
        if existing_file:
            raise FileAlreadyExistsException(f"File with id {existing_file.id} already exists.")

    def upload_file(self, file_name: str, content: bytes) -> FileModel:
        """Upload a file to the storage service and save its metadata in the repository."""
        # Validate the file format
        if not any (file_name.endswith(ext) for ext in self.extensions):
            raise InvalidFileFormatException(f"File format not allowed. Allowed formats: {self.extensions}")
        
        file_hash = hashlib.sha256(content).hexdigest()

        # Check if the file already exists
        self.check_on_antiplagiate(file_hash)

        # Save the file to the storage
        location = self.file_storage.save(file_id=uuid4(), content=content)

        # Create a new FileModel instance
        file_model = FileModel(
            id=uuid4(),
            name=file_name,
            hash=file_hash,
            location=location,
            uploaded_at=datetime.utcnow()
        )

        # Save the file metadata in the repository
        self.file_repository.save(file_model)

        return file_model
    
    def get_file(self, file_id: UUID) -> bytes:
        """Retrieve a file from the storage service by its ID."""
        # Validate the file ID
        if not isinstance(file_id, UUID):
            raise ValueError("Invalid file ID format. Expected a UUID.")
        if file_id is None:
            raise ValueError("File ID cannot be None.")
        
        # Get the file metadata from the repository
        file_model = self.file_repository.get_by_id(file_id)
        if not file_model:
            raise FileNotFoundException(f"File with ID {file_id} not found.")

        # Load the file content from the storage
        content = self.file_storage.load(location=file_model.location)
        return content
    