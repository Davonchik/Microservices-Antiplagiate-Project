from uuid import UUID
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from app.domain.exceptions.exceptions import StorageUnavailableException, FileNotFoundException, FileAlreadyExistsException, InvalidFileFormatException
#from app.domain.exceptions import FileNotFoundException, FileAlreadyExistsException, InvalidFileFormatException
from app.use_cases.analyze_file import AnalyzeFileUseCase
from app.infrastructure.storage.file_storage import LocalFileStorage
from app.infrastructure.repositories.postgres_repository import PostgresFileAnalysisRepository
from app.infrastructure.wordcloud.wordcloud_client import WordCloudClientImpl
from app.infrastructure.file_storage_client.file_storage_client import RemoteFileStorageClient
from app.use_cases.get_results import GetAnalysisResultsUseCase
from app.config import settings
from io import BytesIO

def get_analyze_file_use_case():
    storage = LocalFileStorage(settings.storage_path)
    repo = PostgresFileAnalysisRepository(settings.database_url)
    wordcloud_client = WordCloudClientImpl()
    remote_storage = RemoteFileStorageClient(settings.remote_storage_url)
    return AnalyzeFileUseCase(repo, storage, wordcloud_client, remote_storage)

def get_results_use_case():
    return GetAnalysisResultsUseCase()
