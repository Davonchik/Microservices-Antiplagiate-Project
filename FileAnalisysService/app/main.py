from fastapi import FastAPI
from app.presentation.api.routes.analyze import router as analyze_router
from app.presentation.api.routes.results import router as results_router

app = FastAPI(title="File Analysys Service")
app.include_router(analyze_router, prefix="/analyze_file", tags=["Files"])
app.include_router(results_router, prefix="/results", tags=["Results"])