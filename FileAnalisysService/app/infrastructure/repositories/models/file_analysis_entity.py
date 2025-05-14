from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileAnalysisEntity(Base):
    __tablename__ = "file_analysis"
    file_id = Column(UUID_PG(as_uuid=True), primary_key=True)
    paragraphs_count = Column(Integer, nullable=False)
    words_count = Column(Integer, nullable=False)
    symbols_count = Column(Integer, nullable=False)
    content_hash = Column(String, unique=True, nullable=False)
    wordcloud_location = Column(String, nullable=False)