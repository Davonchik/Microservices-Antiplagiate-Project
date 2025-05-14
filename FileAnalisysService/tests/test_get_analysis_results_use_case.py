import pytest
from uuid import uuid4

from app.use_cases.get_results import GetAnalysisResultsUseCase
from app.domain.exceptions.exceptions import FileNotFoundException

def test_get_results_success(tmp_path, monkeypatch):
    wc = tmp_path / "wordclouds"
    wc.mkdir()
    loc = f"{uuid4()}.svg"
    f = wc / loc
    f.write_bytes(b"IMG")
    
    monkeypatch.chdir(tmp_path)
    uc = GetAnalysisResultsUseCase()
    out = uc.execute(loc)
    assert out == b"IMG"

def test_get_results_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    uc = GetAnalysisResultsUseCase()
    with pytest.raises(FileNotFoundException):
        uc.execute("nope.svg")