from uuid import uuid4
import pytest

from app.infrastructure.storage.file_storage import LocalFileStorage

@pytest.fixture
def tmp_dir(tmp_path):
    return str(tmp_path)

def test_local_storage_save_load_delete(tmp_dir):
    stor = LocalFileStorage(tmp_dir)
    fid = uuid4()
    data = b"abc"

    path = stor.base_path / f"{fid}.txt"
    path.write_bytes(data)

    loaded = stor.get_file(fid)
    assert loaded == data

    path.unlink()
    with pytest.raises(FileNotFoundError):
        stor.get_file(fid)