import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import pytest
from uuid import UUID

from app.domain.models import FileModel
from app.domain.exceptions import FileNotFoundException
from app.use_cases.file_service import FileService

# Dummy-repo for FileModel.
class DummyRepo:
    def __init__(self):
        self.by_id = {}
        self.by_hash = {}

    def save(self, model: FileModel):
        self.by_id[model.id] = model
        self.by_hash[model.hash] = model
        return model

    def get_by_id(self, file_id: UUID):
        return self.by_id.get(file_id)

    def get_by_hash(self, h: str):
        return self.by_hash.get(h)

    def delete(self, file_id: UUID):
        if file_id in self.by_id:
            del self.by_hash[self.by_id[file_id].hash]
            del self.by_id[file_id]


# This is a simple in-memory storage for testing purposes.
class DummyStorage:
    def __init__(self):
        self.store = {}

    def save(self, file_id, content: bytes) -> str:
        self.store[file_id] = content
        return str(file_id)

    def load(self, location: str) -> bytes:
        fid = UUID(location)
        if fid not in self.store:
            raise FileNotFoundException(f"{fid} not found")
        return self.store[fid]

    def delete(self, location: str):
        fid = UUID(location)
        self.store.pop(fid, None)

@pytest.fixture
def file_service():
    repo = DummyRepo()
    storage = DummyStorage()
    return FileService(repo, storage)