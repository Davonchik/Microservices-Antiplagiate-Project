from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FileModel(BaseModel):
    id: UUID
    name: str
    hash: str
    location: str
    uploaded_at: datetime
