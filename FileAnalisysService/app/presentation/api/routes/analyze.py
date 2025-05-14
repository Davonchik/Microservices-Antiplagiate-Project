from uuid import UUID
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from app.domain.exceptions.exceptions import StorageUnavailableException, FileNotFoundException, FileAlreadyExistsException, InvalidFileFormatException
from app.use_cases.analyze_file import AnalyzeFileUseCase
from app.infrastructure.storage.file_storage import LocalFileStorage
from app.infrastructure.repositories.postgres_repository import PostgresFileAnalysisRepository
from app.infrastructure.wordcloud.wordcloud_client import WordCloudClientImpl
from app.infrastructure.file_storage_client.file_storage_client import RemoteFileStorageClient
from app.config import settings
import traceback
from app.presentation.api.dependencies import get_analyze_file_use_case

router = APIRouter()

@router.post("/analyze")
async def analyze(file_id: str, service: AnalyzeFileUseCase = Depends(get_analyze_file_use_case)):
    try:
        uuid_obj = UUID(file_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid file ID format. Expected a UUID.")
    
    try:
        result = service.execute(uuid_obj)
        return result.dict()
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except StorageUnavailableException as e:
        raise HTTPException(status_code=503, detail=e.message)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")