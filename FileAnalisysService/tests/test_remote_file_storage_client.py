import pytest
from uuid import uuid4
import requests

from app.infrastructure.file_storage_client.file_storage_client import RemoteFileStorageClient
from app.domain.exceptions.exceptions import FileNotFoundException

class DummyResp:
    def __init__(self, status, content=b"X"):
        self.status_code = status
        self.content = content

def test_remote_client_success(monkeypatch):
    fid = uuid4()
    client = RemoteFileStorageClient("http://host/", path="/files/")
    
    monkeypatch.setattr(requests, "get", lambda url: DummyResp(200, b"OK"))
    data = client.get_file(fid)
    assert data == b"OK"

def test_remote_client_not_found(monkeypatch):
    fid = uuid4()
    client = RemoteFileStorageClient("http://host/", path="/files/")
    monkeypatch.setattr(requests, "get", lambda url: DummyResp(404))
    with pytest.raises(FileNotFoundException):
        client.get_file(fid)