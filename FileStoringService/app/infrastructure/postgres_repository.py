from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import UUID
from app.infrastructure.models.file_entity import FileEntity, Base
from app.domain.models import FileModel
from app.domain.ports.file_repository import AbstractFileRepository

class PostgresFileRepository(AbstractFileRepository):
    def __init__(self, db_url: str):
        """Initialize the PostgreSQL file repository."""
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def save(self, file: FileModel) -> FileModel:
        """Save a file to the PostgreSQL database."""
        session = self.Session()
        entity = FileEntity(
            id=file.id,
            name=file.name,
            hash=file.hash,
            location=file.location,
            uploaded_at=file.uploaded_at,
        )
        session.add(entity)
        session.commit()
        session.close()
        return file

    def get_by_id(self, file_id: UUID) -> FileModel:
        """Retrieve a file from the PostgreSQL database by its ID."""
        session = self.Session()
        entity = session.query(FileEntity).get(file_id)
        session.close()
        if not entity:
            return None
        return FileModel(**entity.__dict__)

    def get_by_hash(self, file_hash: str) -> FileModel:
        """Retrieve a file from the PostgreSQL database by its hash."""
        session = self.Session()
        entity = session.query(FileEntity).filter_by(hash=file_hash).first()
        session.close()
        if not entity:
            return None
        return FileModel(**entity.__dict__)

    def delete(self, file_id: UUID) -> None:
        """Delete a file from the PostgreSQL database by its ID."""
        session = self.Session()
        entity = session.query(FileEntity).get(file_id)
        if not entity:
            session.close()
            return
        session.delete(entity)
        session.commit()
        session.close()