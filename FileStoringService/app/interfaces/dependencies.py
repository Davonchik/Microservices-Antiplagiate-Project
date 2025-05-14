from app.use_cases.file_service import FileService
from app.infrastructure.local_storage import LocalFileStorage
from app.infrastructure.postgres_repository import PostgresFileRepository
from app.config import settings

def get_file_service():
    storage = LocalFileStorage(settings.storage_path)
    repo = PostgresFileRepository(settings.database_url)
    return FileService(repo, storage)