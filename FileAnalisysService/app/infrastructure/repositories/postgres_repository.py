from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import UUID
from app.domain.entities.models import FileAnalysisModel
from app.domain.repositories.analysis_repository import FileAnalysisRepository
from app.infrastructure.repositories.models.file_analysis_entity import Base, FileAnalysisEntity


class PostgresFileAnalysisRepository(FileAnalysisRepository):
    def __init__(self, db_url: str):
        """Initialize the PostgreSQL file analysis repository."""
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def save(self, analysis: FileAnalysisModel) -> None:
        """Save the file analysis result to the PostgreSQL database."""
        session = self.Session()
        entity = FileAnalysisEntity(
            file_id=analysis.file_id,
            paragraphs_count=analysis.paragraphs_count,
            words_count=analysis.words_count,
            symbols_count=analysis.symbols_count,
            content_hash=analysis.content_hash,
            wordcloud_location=analysis.wordcloud_location,
        )
        session.add(entity)
        session.commit()
        session.close()
    
    def get_by_id(self, file_id: UUID) -> FileAnalysisModel:
        """Get the file analysis result by file ID."""
        session = self.Session()
        entity = session.query(FileAnalysisEntity).get(file_id)
        session.close()
        if not entity:
            return None
        return FileAnalysisModel(**entity.__dict__)
    
    def find_by_hash(self, content_hash: str) -> FileAnalysisModel:
        """Find the file analysis result by content hash."""
        session = self.Session()
        entity = session.query(FileAnalysisEntity).filter_by(content_hash=content_hash).first()
        session.close()
        if not entity:
            return None
        return FileAnalysisModel(**entity.__dict__)