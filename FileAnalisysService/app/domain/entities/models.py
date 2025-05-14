from pydantic import BaseModel
from uuid import UUID

class FileAnalysisModel(BaseModel):
    file_id: UUID
    paragraphs_count: int
    words_count: int
    symbols_count: int
    content_hash: str
    wordcloud_location: str

