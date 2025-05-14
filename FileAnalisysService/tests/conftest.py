import sys, os
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from uuid import UUID
from app.infrastructure.repositories.postgres_repository import PostgresFileAnalysisRepository
from app.use_cases.analyze_file import AnalyzeFileUseCase
from app.use_cases.get_results import GetAnalysisResultsUseCase
from app.domain.exceptions.exceptions import FileNotFoundException
from app.domain.entities.models import FileAnalysisModel

@pytest.fixture
def sqlite_analysis_repo():
    return PostgresFileAnalysisRepository("sqlite:///:memory:")

@pytest.fixture
def analyze_use_case(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "wordclouds").mkdir()

    class DummyAnalysisRepo:
        def __init__(self):
            self.by_hash = {}
            self.saved = []

        def get_by_id(self, file_id: UUID):
            return None

        def find_by_hash(self, content_hash: str):
            return self.by_hash.get(content_hash)

        def save(self, analysis: FileAnalysisModel):
            self.saved.append(analysis)
            self.by_hash[analysis.content_hash] = analysis

    class DummyFileStorageClient:
        def __init__(self, mapping: dict):
            self.map = mapping

        def get_file(self, file_id: UUID) -> bytes:
            if file_id not in self.map:
                raise FileNotFoundException(f"{file_id} not found")
            return self.map[file_id]

    class DummyWordCloudClient:
        def __init__(self, data: bytes = b"IMGBYTES", fail: bool = False):
            self.data = data
            self.fail = fail

        def generate(self, text: str) -> bytes:
            if self.fail:
                raise Exception("WC ERROR")
            return self.data

    dummy_repo = DummyAnalysisRepo()
    file_map = {}
    file_storage_client = DummyFileStorageClient(file_map)
    wordcloud_client = DummyWordCloudClient()
    use_case = AnalyzeFileUseCase(
        analysis_repo=dummy_repo,
        storage_client=None,
        wordcloud_client=wordcloud_client,
        file_storage_client=file_storage_client
    )

    return use_case, dummy_repo, file_map, tmp_path


@pytest.fixture
def results_use_case(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return GetAnalysisResultsUseCase()