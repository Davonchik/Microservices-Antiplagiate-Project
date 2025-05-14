from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileEntity(Base):
    __tablename__ = "files"
    id = Column(UUID_PG(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    hash = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)