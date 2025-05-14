import shutil
import tempfile
from uuid import uuid4
import pytest
from pathlib import Path

from app.infrastructure.local_storage import LocalFileStorage
from app.domain.exceptions import FileNotFoundException

@pytest.fixture
def tmp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

def test_save_and_load_and_delete(tmp_dir):
    storage = LocalFileStorage(tmp_dir)
    fid = uuid4()
    data = b"abc123"

    loc = storage.save(fid, data)
    p = Path(loc)
    assert p.exists()
    assert storage.load(loc) == data

    storage.delete(loc)
    assert not p.exists()

def test_load_missing(tmp_dir):
    storage = LocalFileStorage(tmp_dir)
    with pytest.raises(FileNotFoundException):
        storage.load(str(uuid4()))