from uuid import UUID
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from app.domain.exceptions.exceptions import FileNotFoundException
from app.use_cases.analyze_file import AnalyzeFileUseCase
from app.use_cases.get_results import GetAnalysisResultsUseCase
from app.infrastructure.storage.file_storage import LocalFileStorage
from app.infrastructure.repositories.postgres_repository import PostgresFileAnalysisRepository
from app.infrastructure.wordcloud.wordcloud_client import WordCloudClient
from app.presentation.api.dependencies import get_results_use_case
from app.config import settings
from io import BytesIO
import traceback

router = APIRouter()

@router.get("/download/{location}")
def download(location: str, service: GetAnalysisResultsUseCase = Depends(get_results_use_case)):
    try:
        content = service.execute(location)
        return StreamingResponse(BytesIO(content), 
                                 media_type="application/octet-stream", 
                                 headers={"Content-Disposition": f"attachment; filename={location}"})
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    