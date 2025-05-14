from uuid import UUID
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from app.domain.exceptions import FileNotFoundException, FileAlreadyExistsException, InvalidFileFormatException
from app.use_cases.file_service import FileService
from app.infrastructure.local_storage import LocalFileStorage
from app.infrastructure.postgres_repository import PostgresFileRepository
from app.config import settings
from app.interfaces.dependencies import get_file_service
from io import BytesIO

router = APIRouter()

@router.post("/upload")
async def upload(service: FileService = Depends(get_file_service), file: UploadFile = File(...)):
    try:
        content = await file.read()
        model = service.upload_file(file.filename, content)
        return model.dict()
    except InvalidFileFormatException as e:
        raise HTTPException(status_code=415, detail=e.message)
    except FileAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@router.get("/download/{file_id}")
def download(file_id: str, service: FileService = Depends(get_file_service)):
    try:
        uuid_obj = UUID(file_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid file ID format. Expected a UUID.")
    
    try:
        content = service.get_file(UUID(file_id))
        return StreamingResponse(BytesIO(content), 
                                 media_type="application/octet-stream", 
                                 headers={"Content-Disposition": f"attachment; filename={file_id}.txt"})
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")