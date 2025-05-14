import pytest
from uuid import UUID
from app.domain.exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
    InvalidFileFormatException,
)

def test_upload_and_download_roundtrip(file_service):
    name = "report.txt"
    data = b"hello world"
    model = file_service.upload_file(name, data)

    assert isinstance(model.id, UUID)
    assert model.name == name

    assert file_service.get_file(model.id) == data

def test_invalid_extension(file_service):
    with pytest.raises(InvalidFileFormatException):
        file_service.upload_file("bad.pdf", b"data")

def test_duplicate_hash(file_service):
    data = b"same"
    file_service.upload_file("a.txt", data)
    with pytest.raises(FileAlreadyExistsException):
        file_service.upload_file("b.txt", data)

def test_get_missing_file(file_service):
    fake = UUID("00000000-0000-0000-0000-000000000000")
    with pytest.raises(FileNotFoundException):
        file_service.get_file(fake)