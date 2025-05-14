import sys, os
from uuid import uuid4, UUID
from datetime import datetime

import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from app.infrastructure.postgres_repository import PostgresFileRepository
from app.domain.models import FileModel

@pytest.fixture
def repo():
    return PostgresFileRepository("sqlite:///:memory:")

def test_save_and_get_by_id(repo):
    fid = uuid4()
    model = FileModel(
        id=fid,
        name="test.txt",
        hash="abc123",
        location="/tmp/test.txt",
        uploaded_at=datetime.utcnow()
    )
    
    returned = repo.save(model)
    assert returned is model

    fetched = repo.get_by_id(fid)
    assert isinstance(fetched, FileModel)
    assert fetched.id == model.id
    assert fetched.name == model.name
    assert fetched.hash == model.hash
    assert fetched.location == model.location

def test_get_by_hash(repo):
    fid = uuid4()
    model = FileModel(
        id=fid,
        name="findme.txt",
        hash="def456",
        location="/tmp/findme.txt",
        uploaded_at=datetime.utcnow()
    )
    repo.save(model)

    fetched = repo.get_by_hash("def456")
    assert isinstance(fetched, FileModel)
    assert fetched.id == model.id
    assert fetched.name == model.name

def test_delete(repo):
    fid = uuid4()
    model = FileModel(
        id=fid,
        name="todelete.txt",
        hash="ghi789",
        location="/tmp/todelete.txt",
        uploaded_at=datetime.utcnow()
    )
    repo.save(model)
    assert repo.get_by_id(fid) is not None

    repo.delete(fid)
    assert repo.get_by_id(fid) is None

def test_get_missing_returns_none(repo):
    assert repo.get_by_id(uuid4()) is None
    assert repo.get_by_hash("no-such-hash") is None