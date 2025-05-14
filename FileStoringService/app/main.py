from fastapi import FastAPI
from app.interfaces.storage_router import router as storage_router

app = FastAPI(title="File Storing Service")
app.include_router(storage_router, prefix="/files", tags=["Files"])