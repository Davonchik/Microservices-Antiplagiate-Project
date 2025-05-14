from uuid import uuid4
from datetime import datetime

def test_postgres_analysis_repo_crud(sqlite_analysis_repo):
    repo = sqlite_analysis_repo
    fid = uuid4()
    model = repo.get_by_id(fid)
    assert model is None

    mdl = repo.find_by_hash("h")
    assert mdl is None

    from app.domain.entities.models import FileAnalysisModel
    analysis = FileAnalysisModel(
        file_id=fid,
        paragraphs_count=1,
        words_count=2,
        symbols_count=3,
        content_hash="h1",
        wordcloud_location="p.svg"
    )
    repo.save(analysis)

    fetched = repo.get_by_id(fid)
    assert fetched.file_id == analysis.file_id
    assert fetched.content_hash == analysis.content_hash

    fetched2 = repo.find_by_hash("h1")
    assert fetched2.file_id == analysis.file_id